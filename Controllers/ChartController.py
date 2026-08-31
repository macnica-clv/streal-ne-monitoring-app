import os, time, datetime
import sys

from decimal import Decimal

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject

from Controllers import RegisterController, RegisterControllerSR300
from Models.Config import Config, ConfigDataChartSensorSettings, ConfigSampling, ConfigDataChartFilter, \
    ConfigDataChartSensorDataDisplay
from Models.Register_Item_SR300 import RegisterItemSR300
from Models.Sensor import SensorConnectionStatusKind
from Models.Hizmil_Driver import HizmilDriver, ModeKind, ResultKind, MeasureData
from Models.Log import MeasureLog, SingleMeasData, SingleSensorData, Log
from Models.Register_Item_SR500 import RegisterItemSR500, ItemKind
from Models.Board import BoardKind
from Views import ChartView
from Views.ChartView import SensorDataTableColumnKind


class ChartController(QObject):
    measurementStarted = Signal()
    measurementStopped = Signal()
    BUFFER_TRANSFER_OFF = 0x01
    BUFFER_TRANSFER_ON = 0x02
    BUFFER_CAPACITY = 4096

    def __init__(self, config:Config, parent=None):
        super(ChartController, self).__init__(parent)
        self.chart_page = ChartView.ChartPage(parent=parent)
        self.register_controller = RegisterController.RegisterController(parent=parent)
        self.register_controller_sr300 = RegisterControllerSR300.RegisterControllerSR300(parent=parent)
        self._driver: HizmilDriver = HizmilDriver()
        self._config: Config = config

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.chart_page.chart_tabs.update_graph)
        self.buffer_pickup_timer = QtCore.QTimer()
        self.buffer_pickup_timer.timeout.connect(self.request_buffer_data)
        self._buffer_mode_active = False
        self._buffer_request_in_progress = False

        # ヘッダ行数＝レジスタ部のヘッダ＋レジスタの項目数＋空行＋測定値のヘッダ
        self.chart_page.set_log_header_row(ItemKind.item_num.value + 3)
        self.meas_log: dict[BoardKind, MeasureLog] = {}

        # 起動直後に無効なボタンをDisableにする
        self.chart_page.ui.meas_start_button.setEnabled(False)
        self.chart_page.ui.meas_stop_button.setEnabled(False)
        self.chart_page.ui.save_log_button.setEnabled(False)
        self.chart_page.ui.auto_range_button.setEnabled(False)
        self.chart_page.ui.auto_balance_button.setEnabled(False)
        self.chart_page.ui.register_settings_button.setEnabled(False)

        self.chart_page.ui.meas_start_button.clicked.connect(self.measure_start)
        self.chart_page.ui.meas_stop_button.clicked.connect(self.measure_stop)
        self.chart_page.ui.auto_range_button.clicked.connect(self.auto_range)
        self.chart_page.ui.save_log_button.clicked.connect(self.save_log)
        self.chart_page.ui.x_zoom_in_button.clicked.connect(self.x_zoom_in)
        self.chart_page.ui.x_zoom_out_button.clicked.connect(self.x_zoom_out)
        self.chart_page.ui.strain_zoom_in_button.clicked.connect(self.strain_zoom_in)
        self.chart_page.ui.strain_zoom_out_button.clicked.connect(self.strain_zoom_out)
        self.chart_page.ui.temp_zoom_in_button.clicked.connect(self.temp_zoom_in)
        self.chart_page.ui.temp_zoom_out_button.clicked.connect(self.temp_zoom_out)
        self.chart_page.ui.capture_button.clicked.connect(self.capture_graph)
        self.chart_page.ui.register_settings_button.clicked.connect(self.show_register_page)
        self.chart_page.ui.csv_calc_button.clicked.connect(self.csv_calc_exec)
        self.chart_page.autoBalanceRequested.connect(self.auto_balance)

        self.load_config()

    def show(self):
        self.chart_page.setVisible(True)

    def hide(self):
        self.chart_page.setVisible(False)

    def show_register_page(self):
        theme = self._config.load_config_theme().window_theme

        if self._driver._is_sr300_connected():
            self.register_controller_sr300.apply_theme(theme)
            self.register_controller_sr300.show()
        else:
            self.register_controller.apply_theme(theme)
            self.register_controller.show()

    def set_driver(self, driver: HizmilDriver):
        self._driver = driver
        self._driver.on_notify_measure(self.measure_callback)
        self.register_controller.set_driver(driver)
        self.register_controller_sr300.set_driver(driver)

    def set_shortcuts(self):
        sc_config = self._config.load_config_shortcut()
        self.chart_page.ui.meas_start_button.setShortcut(sc_config.meas_start.replace("Cmd","Ctrl").replace("Opt","Alt"))
        self.chart_page.ui.meas_stop_button.setShortcut(sc_config.meas_stop.replace("Cmd","Ctrl").replace("Opt","Alt"))
        self.chart_page.ui.auto_range_button.setShortcut(sc_config.auto_range.replace("Cmd","Ctrl").replace("Opt","Alt"))
        self.chart_page.ui.save_log_button.setShortcut(sc_config.save_log.replace("Cmd","Ctrl").replace("Opt","Alt"))
        self.chart_page.ui.capture_button.setShortcut(sc_config.capture.replace("Cmd","Ctrl").replace("Opt","Alt"))

    def get_log_header(self, ch_offset: int):
        # センサ名（設定値のヘッダ）
        ch_num = self._driver.sensor_ch_max
        header = "," + ",".join(self.chart_page.sensor_name[ch + ch_offset] for ch in range(ch_num)) + "\n"

        if self._driver._is_sr300_connected():
            registers = [RegisterItemSR300(self._driver, ch + ch_offset) for ch in range(ch_num)]
        else:
            registers = [RegisterItemSR500(self._driver, ch + ch_offset) for ch in range(ch_num)]

        item_names = [name for name in registers[0].get_item_names() if name != ""]
        item_values = []
        for register in registers:
            register.read_item()
            values = [val_str.replace(",", " ") for val_str in register.get_all_value_str()]
            item_values.append(values)
        item_conv = [item for item in zip(item_names, *item_values)]
        header += "\n".join([",".join(item) for item in item_conv]) + "\n\n"

        # 測定値のヘッダ
        header += "Time," + ",".join([f"Ch{i+1} Status,Ch{i+1} Temp(℃), Ch{i+1} Strain, Ch{i+1} Strain Value(με)" for i in range(ch_offset, ch_num + ch_offset)]) + "\n"
        return header

    def enable_buttons(self):
        # 接続が確立したら有効になるボタンをEnableにする
        self.chart_page.ui.meas_start_button.setEnabled(True)
        self.chart_page.ui.save_log_button.setEnabled(True)
        self.chart_page.ui.auto_range_button.setEnabled(True)
        self.chart_page.ui.auto_balance_button.setEnabled(True)
        self.chart_page.ui.register_settings_button.setEnabled(True)

    def disable_buttons(self):
        self.chart_page.ui.meas_start_button.setEnabled(False)
        self.chart_page.ui.meas_stop_button.setEnabled(False)
        self.chart_page.ui.save_log_button.setEnabled(False)
        self.chart_page.ui.auto_range_button.setEnabled(False)
        self.chart_page.ui.auto_balance_button.setEnabled(False)
        self.chart_page.ui.register_settings_button.setEnabled(False)

    def measure_start(self):
        if self.chart_page.validate_sample_rate() <= 0:
            return ResultKind.parameter_error

        buffer_mode = self.chart_page.is_buffer_mode_enabled()
        buffer_interval_ms = self.chart_page.validate_buffer_interval_ms() if buffer_mode else 0
        if buffer_mode:
            if buffer_interval_ms <= 0:
                return ResultKind.parameter_error
            if not self.validate_buffer_pickup_interval(buffer_interval_ms):
                return ResultKind.parameter_error

        for i in range(self._driver.ch_max):
            self.chart_page.set_chart_view_only_connected(i, self._driver.is_sensor_enable(i))
        self._driver.init_status_all()

        connected_boards = [board for board in BoardKind if self._driver.get_board_connection_status(board)]
        connected_channels = [ch for ch, status in enumerate(self.chart_page.connection_status) if status == SensorConnectionStatusKind.connected]
        offsets = [self._driver.get_ch(board, 0) for board in connected_boards]
        sensor_nums = [self._driver.sensor_ch_max for _ in connected_boards]
        self.chart_page.chart_tabs.clear_meas_data(connected_boards, offsets, sensor_nums)

        log_config = self._config.load_config_log()
        max_row = log_config.log_sampling_num
        dst = log_config.log_save_dst
        prefix = log_config.log_filename_prefix
        if log_config.log_auto_save:
            self.meas_log.clear()
            for board in connected_boards:
                meas_log = MeasureLog(max_row=max_row, name=f"Board{board.value}", prefix=prefix)
                meas_log.set_header(self.get_log_header(self._driver.get_ch(board, 0)))
                dst = meas_log.make_dst_dir(dst)
                meas_log.start()
                self.meas_log[board] = meas_log

        if log_config.log_auto_save and log_config.log_save_ma:
            ma_logs = {}
            for board in connected_boards:
                ma_log = MeasureLog(max_row=max_row, name=f"MA_Board{board.value}", prefix=prefix)
                ma_log.set_header(self.get_log_header(self._driver.get_ch(board, 0)))
                ma_log.set_dst_dir(dst)
                ma_log.start()
                ma_logs[board] = ma_log
            self.chart_page.chart_tabs.set_ma_log(ma_logs)

        if log_config.log_auto_save and log_config.log_save_fft:
            self.chart_page.chart_tabs.make_fft_log(max_row, dst, prefix, connected_channels)

        interval = self.calc_interval()
        rate = self.calc_sampling_rate()
        if not buffer_mode:
            self.chart_page.chart_tabs.ma_start(connected_channels, offsets, sensor_nums)
            self.chart_page.chart_tabs.fft_start(rate, connected_channels)

        transfer_result = self._driver.set_transfer_mode(self.BUFFER_TRANSFER_ON if buffer_mode else self.BUFFER_TRANSFER_OFF)
        if transfer_result != ResultKind.ok:
            print(f"Set Transfer Mode Result: {transfer_result}", flush=True)
            return transfer_result

        measure_mode = self.chart_page.get_buffer_transfer_mode() if buffer_mode else ModeKind.all
        result = self._driver.start_measure(interval, measure_mode)
        print(f"Measure Start Result: {result}", flush=True)
        if result == ResultKind.ok:
            self._buffer_mode_active = buffer_mode
            self.measurementStarted.emit()
            self.chart_page.ui.meas_start_button.setEnabled(False)
            self.chart_page.ui.meas_stop_button.setEnabled(True)
            self.chart_page.ui.auto_balance_button.setEnabled(False)
            if buffer_mode:
                self.buffer_pickup_timer.start(buffer_interval_ms)
            else:
                self.update_timer.start(25)
        elif buffer_mode:
            self._driver.set_transfer_mode(self.BUFFER_TRANSFER_OFF)
        return result

    def validate_buffer_pickup_interval(self, interval_ms: int) -> bool:
        rate = self.calc_sampling_rate()
        samples_per_pickup = rate * interval_ms / 1000.0
        if samples_per_pickup < self.BUFFER_CAPACITY:
            self.chart_page.buffer_interval_edit.setStyleSheet("")
            return True

        max_interval = int((self.BUFFER_CAPACITY - 1) * 1000 // rate)
        self.chart_page.buffer_interval_edit.setStyleSheet("border: 1px solid red;")
        print(
            f"Buffer pickup interval {interval_ms}ms may exceed FIFO capacity. "
            f"Use {max_interval}ms or less at {rate}Hz.",
            flush=True,
        )
        return False

    def request_buffer_data(self):
        if not self._buffer_mode_active or self._buffer_request_in_progress:
            return

        self._buffer_request_in_progress = True
        try:
            result, count = self._driver.get_sampling_data()
            if result != ResultKind.ok:
                print(f"Get Sampling Data Result: {result}", flush=True)
            else:
                print(f"Get Sampling Data Count: {count}", flush=True)
        finally:
            self._buffer_request_in_progress = False

    def calc_sampling_rate(self) -> float:
        sampling_rate = self.chart_page.validate_sample_rate()
        selected_unit = self.chart_page.get_rate_unit()
        if selected_unit == "Hz" or selected_unit == "sps":
            return sampling_rate
        elif selected_unit == "ms":
            return 1000 / sampling_rate
        else:
            return 1000

    def calc_interval(self) -> int:
        sampling_rate = Decimal(str(self.chart_page.validate_sample_rate()))
        selected_unit = self.chart_page.get_rate_unit()
        if selected_unit == "Hz" or selected_unit == "sps":
            interval = 1000000 // sampling_rate
        elif selected_unit == "ms":
            interval = sampling_rate * 1000
        else:
            interval = 1000
        return int(interval)

    def measure_callback(self, board: BoardKind, meas_data: list[MeasureData]):
        if not self._buffer_mode_active:
            self.chart_page.chart_tabs.add_meas_data(board, meas_data)

        log = self.meas_log.get(board, None)
        if log is None:
            return
        for data in meas_data:
            single_data = SingleMeasData(data.seconds, data.nanoseconds, [])
            for i in range(self._driver.sensor_ch_max):
                if (i < len(data.sensor_data)) and (i < len(data.strain_value)) and self._driver.is_board_sensor_enable(board, i):
                    strain = data.sensor_data[i].strain
                    temp = data.sensor_data[i].temp
                    status = data.sensor_data[i].status
                    strain_value = data.strain_value[i]
                    single_data.sensor_data.append(SingleSensorData(True, status, temp, strain, strain_value))
                else:
                    single_data.sensor_data.append(SingleSensorData(False, 0, 0, 0, 0))
            log.add_data(single_data)

    def measure_stop(self):
        buffer_mode = self._buffer_mode_active
        if buffer_mode:
            self.buffer_pickup_timer.stop()
            self.request_buffer_data()

        result = self._driver.stop_measure()
        print(f"Measure Stop Result: {result}", flush=True)
        if buffer_mode:
            self.request_buffer_data()
            transfer_result = self._driver.set_transfer_mode(self.BUFFER_TRANSFER_OFF)
            print(f"Set Transfer Mode Result: {transfer_result}", flush=True)
            self._buffer_mode_active = False

        if result == ResultKind.ok:
            self.measurementStopped.emit()
            self.chart_page.ui.meas_start_button.setEnabled(True)
            self.chart_page.ui.meas_stop_button.setEnabled(False)
            self.chart_page.ui.auto_balance_button.setEnabled(True)

        # 測定停止後に最新のグラフに更新する
        self.update_timer.stop()
        if not buffer_mode:
            while self.chart_page.chart_tabs.is_drawing:
                pass
            self.chart_page.chart_tabs.update_graph()

        for log in self.meas_log.values():
            log.stop()
        self.chart_page.chart_tabs.ma_stop()
        self.chart_page.chart_tabs.fft_stop()
        return result

    def auto_range(self):
        self.chart_page.chart_tabs.main_plot_area.reset_range()

    def auto_balance(self):
        ret = self.offset_calibration_all()
        ret = self.temp_calibration_all()
        self._driver.init_status_all()

    def offset_calibration_all(self) -> bool:
        for i in range(self._driver.ch_max):
            result = self._driver.offset_calibration(i, 0, False)
            if result != ResultKind.ok:
                return False
        return True

    def temp_calibration_all(self) -> bool:
        for i in range(self._driver.ch_max):
            result = self._driver.temp_calibration(i, 0, False)
            if result != ResultKind.ok:
                return False
        return True

    def save_log(self):
        log_config = self._config.load_config_log()
        dst = log_config.log_save_dst
        for board, graph_data in self.chart_page.chart_tabs.graph_data.items():
            log = MeasureLog(name=f"Board{board.value}", prefix=log_config.log_filename_prefix, max_row=log_config.log_sampling_num)
            dst = log.make_dst_dir(dst)
            log.set_header(self.get_log_header(self._driver.get_ch(board, 0)))
            log.start()

            seconds = graph_data.get_seconds()
            nanoseconds = graph_data.get_nanoseconds()
            sensor_num = graph_data.get_sensor_num()

            status_list = [graph_data.get_status(i) for i in range(sensor_num)]
            temp_list = [graph_data.get_temps(i) for i in range(sensor_num)]
            strain_list = [graph_data.get_strains(i) for i in range(sensor_num)]
            strain_value_list = [graph_data.get_strain_values(i) for i in range(sensor_num)]

            for i, (sec, ns) in enumerate(zip(seconds, nanoseconds)):
                meas_data = SingleMeasData(sec, ns, [])
                for ch in range(sensor_num):
                    if i >= min(len(status_list[ch]), len(temp_list[ch]), len(strain_list[ch]), len(strain_value_list[ch])):
                        meas_data.sensor_data.append(SingleSensorData(False, 0, 0, 0, 0))
                    elif not self._driver.is_board_sensor_enable(board, ch):
                        meas_data.sensor_data.append(SingleSensorData(False, 0, 0, 0, 0))
                    else:
                        meas_data.sensor_data.append(SingleSensorData(True, status_list[ch][i], temp_list[ch][i], strain_list[ch][i], strain_value_list[ch][i]))
                log.add_data(meas_data)
            log.stop()

    def csv_calc_exec(self):
        self.chart_page.csv_calc_exec()

        config_log = self._config.load_config_log()
        if not config_log.log_save_std:
            return
        log = Log(max_row=config_log.log_sampling_num, prefix=config_log.log_filename_prefix, name="SD", use_count=False)
        log.make_dst_dir(config_log.log_save_dst)
        log.start()
        log.save(self.tr("CSV Path") + f",{self.chart_page.ui.csv_browse_edit.text()}\n")
        log.save(self.tr("Select CH") + f",{self.chart_page.ui.ch_select_combobox.currentText()}\n")
        log.save(self.tr("Start Point") + f",{self.chart_page.ui.startpoint_edit.text()}\n")
        log.save(self.tr("End Point") + f",{self.chart_page.ui.endpoint_edit.text()}\n")
        log.save(self.tr("Max") + f",{self.chart_page.ui.max_output.text()}\n")
        log.save(self.tr("Min") + f",{self.chart_page.ui.min_output.text()}\n")
        log.save(self.tr("Ave") + f",{self.chart_page.ui.ave_output.text()}\n")
        log.save(self.tr("σ") + f",{self.chart_page.ui.sigma_output.text()}\n")
        log.save(self.tr("2σ") + f",{self.chart_page.ui.sigma2_output.text()}\n")
        log.save(self.tr("3σ") + f",{self.chart_page.ui.sigma3_output.text()}\n")
        log.save(self.tr("3.3σ") + f",{self.chart_page.ui.sigma33_output.text()}\n")
        log.stop()

    def x_zoom_in(self):
        self.chart_page.chart_tabs.zoom_x(0.5)

    def strain_zoom_in(self):
        self.chart_page.chart_tabs.zoom_strain(0.5)

    def temp_zoom_in(self):
        self.chart_page.chart_tabs.zoom_temp(0.5)

    def x_zoom_out(self):
        self.chart_page.chart_tabs.zoom_x(2.0)

    def strain_zoom_out(self):
        self.chart_page.chart_tabs.zoom_strain(2.0)

    def temp_zoom_out(self):
        self.chart_page.chart_tabs.zoom_temp(2.0)

    def capture_graph(self):
        config_log = self._config.load_config_log()
        save_dst = config_log.capture_save_dst
        dir_name = config_log.log_filename_prefix + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if (save_dst is not None) and os.path.isdir(save_dst):
            path = os.path.join(save_dst, dir_name)
        else:
            path = dir_name
        os.makedirs(path, exist_ok=True)

        # file_name = f"{time.time()}.png"
        file_name = config_log.log_filename_prefix + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + f".png"
        pixmap = self.chart_page.chart_tabs.main_plot_area.grab()
        pixmap.save(os.path.join(path, file_name))

    def load_config(self):
        param = self._config.load_config_sampling()
        self.chart_page.ui.sampling_rate_edit.setText(param.sampling_rate)
        self.chart_page.ui.sampling_rate_unit.setCurrentIndex(param.sampling_unit)
        self.chart_page.set_buffer_mode_enabled(param.buffer_mode)
        self.chart_page.buffer_interval_edit.setText(param.buffer_interval_ms)
        self.chart_page.set_buffer_transfer_mode_index(param.buffer_transfer_mode)

        param = self._config.load_config_filter()
        self.chart_page.fs_bridge.update_moving_average(param.filter_moving_average)
        self.chart_page.fs_bridge.update_moving_average_window_size(param.filter_moving_average_window)
        self.chart_page.fs_bridge.update_fft(param.filter_fft)
        self.chart_page.fs_bridge.update_fft_resolution(param.filter_fft_resolution)
        self.chart_page.fs_bridge.update_fft_window(param.filter_fft_window)
        self.chart_page.fs_bridge.update_standard_deviation(param.filter_standard_deviation)
        self.chart_page.fs_bridge.update_standard_deviation_window_size(param.filter_standard_deviation_window)
        self.chart_page.apply_filter_settings()

        param = self._config.load_config_sensor_settings()
        for i in range(4):
            self.chart_page.ss_bridges[i].update_strain_line_color_index(param.sensor_strain_line_color[i])
            self.chart_page.ss_bridges[i].update_temp_line_color_index(param.sensor_temp_line_color[i])
            self.chart_page.ss_bridges[i].update_line_width_index(param.sensor_line_width[i])
            self.chart_page.ss_bridges[i].update_line_offset_index(param.sensor_line_offset[i])

        param = self._config.load_config_chart_display()
        self.chart_page.update_unit(param.chart_unit)
        self.chart_page.update_column(SensorDataTableColumnKind.name.value, param.show_sensor_name)
        self.chart_page.update_column(SensorDataTableColumnKind.temp.value, param.show_temperature)
        self.chart_page.update_column(SensorDataTableColumnKind.current.value, param.show_current_value)
        self.chart_page.update_column(SensorDataTableColumnKind.init.value, param.show_init_value)
        self.chart_page.update_column(SensorDataTableColumnKind.delta.value, param.show_delta_value)
        self.chart_page.update_column(SensorDataTableColumnKind.status.value, param.show_status)

        for index, value in enumerate(param.sensor_name):
            self.chart_page.update_sensor_name(index, value)
        for index, value in enumerate(param.strain_line_view):
            self.chart_page.update_chart_view(index, 0, value)
        for index, value in enumerate(param.temp_line_view):
            self.chart_page.update_chart_view(index, 1, value)

    def handle_app_closing(self):
        param = ConfigSampling()
        param.sampling_rate = self.chart_page.ui.sampling_rate_edit.text()
        param.sampling_unit = self.chart_page.ui.sampling_rate_unit.currentIndex()
        param.buffer_mode = self.chart_page.is_buffer_mode_enabled()
        param.buffer_interval_ms = self.chart_page.buffer_interval_edit.text()
        param.buffer_transfer_mode = self.chart_page.get_buffer_transfer_mode_index()
        self._config.save_config_sampling(param)

        param = ConfigDataChartFilter()
        param.filter_moving_average = self.chart_page.fs_bridge.moving_average
        param.filter_moving_average_window = self.chart_page.fs_bridge.moving_average_window_size
        param.filter_fft = self.chart_page.fs_bridge.fft
        param.filter_fft_resolution = self.chart_page.fs_bridge.fft_resolution
        param.filter_fft_window = self.chart_page.fs_bridge.get_fft_window()
        param.filter_standard_deviation = self.chart_page.fs_bridge.standard_deviation
        param.filter_standard_deviation_window = self.chart_page.fs_bridge.standard_deviation_window_size
        self._config.save_config_filter(param)

        param = ConfigDataChartSensorSettings()
        name_list = []
        for name in self.chart_page.sensor_name:
            name_list.append(name)
        param.sensor_name = name_list
        for i in range(4):
            strain_color, temp_color, width, offset = self.chart_page.ss_bridges[i].get_settings()
            param.sensor_strain_line_color.append(strain_color)
            param.sensor_temp_line_color.append(temp_color)
            param.sensor_line_width.append(width)
            param.sensor_line_offset.append(offset)
        self._config.save_config_sensor_settings(param)

        param = ConfigDataChartSensorDataDisplay()
        param.chart_unit = self.chart_page.chart_unit
        param.show_sensor_name = self.chart_page.column_show_settings[SensorDataTableColumnKind.name.value]
        param.show_temperature = self.chart_page.column_show_settings[SensorDataTableColumnKind.temp.value]
        param.show_current_value = self.chart_page.column_show_settings[SensorDataTableColumnKind.current.value]
        param.show_init_value = self.chart_page.column_show_settings[SensorDataTableColumnKind.init.value]
        param.show_delta_value = self.chart_page.column_show_settings[SensorDataTableColumnKind.delta.value]
        param.show_status = self.chart_page.column_show_settings[SensorDataTableColumnKind.status.value]
        param.sensor_name = self.chart_page.sensor_name
        param.strain_line_view = self.chart_page.strain_line_view
        param.temp_line_view = self.chart_page.temp_line_view
        self._config.save_config_chart_display(param)

    def update_language(self):
        self.chart_page.ui.retranslateUi(self.chart_page)
        self.chart_page.update_language()
        is_japanese = self._config.load_config_language().language == 1
        self.chart_page.update_buffer_language(is_japanese)
        self.register_controller.update_language()

