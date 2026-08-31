import dataclasses, math, os
import numpy as np
import pandas as pd
import pyqtgraph as pg

try:
    import bottleneck
except ImportError:
    pass

try:
    import numexpr
except ImportError:
    pass
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Deque, Callable, Optional
from functools import partial
from scipy import signal as scipy_signal
from scipy.fftpack import fft

from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer, Signal, Property, Slot, QObject, QSize, QRegularExpression
from PySide6.QtGui import QAction, QActionGroup, QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QDockWidget, QFileDialog, \
    QGraphicsWidget, QGraphicsGridLayout, QCheckBox, QHBoxLayout, QLineEdit, QLabel, QMenu, QHeaderView, QMessageBox, \
    QComboBox, QFrame, \
    QApplication

from Utils.MessageBox import ConfirmDialog
from Utils.Photo_Viewer import PhotoViewer
from Models.Sensor import SensorStatus, ErrorStatusKind, SensorConnectionStatusKind
from Models.Board import BoardKind
from Models.GraphData import GraphData
from Models.Hizmil_Driver import MeasureData
from Models.Hizmil_Driver import ModeKind
from Models.Log import Log, MeasureLog
from Models.Log import SingleMeasData
from Views import Chart_Page
from Views.MainView import tinted_qicon, DummyAppBridge


class ChartUnitKind(Enum):
    strain = 0
    lsb = 1
    num = 2


class YAxisWidget(QGraphicsWidget):
    def __init__(self, label, orientation):
        super().__init__()

        layout = QGraphicsGridLayout()
        layout.setContentsMargins(0, 0, 5, 21)
        self.setLayout(layout)

        self.y_axis = pg.AxisItem(orientation=orientation)
        self.y_axis.setLabel(label)
        layout.addItem(self.y_axis, 0, 0)

    def axis(self) -> pg.AxisItem:
        return self.y_axis
    def range(self):
        return self.y_axis.range

class TimeAxis(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overwrite_values: list[float] = []
        self.thresholds = [1000, 100, 10, 1]
        self.timer = QTimer()
        self.timer.timeout.connect(self.redraw)
        self.timer.start(200)

    def set_overwrite_values(self, values: list[float]):
        self.overwrite_values = values

    def redraw(self):
        # TBD：再描画方法は改善の余地あり
        self.setRange(self.range[0], self.range[1] + 1)
        self.setRange(self.range[0], self.range[1] - 1)

    def calc_sec(self, val, spacing):
        if len(self.overwrite_values) < 1:
            dt = datetime.now() + timedelta(seconds=val / 1000)
        else:
            step = (self.overwrite_values[-1] - self.overwrite_values[0]) / len(self.overwrite_values)
            f, i = math.modf(val)

            if val < 0:
                prev_val = self.overwrite_values[0] + step * val
            elif int(i) < len(self.overwrite_values):
                prev_val = self.overwrite_values[int(i)] + step * f
            else:
                diff = int(i) - len(self.overwrite_values)
                prev_val = self.overwrite_values[-1] + step * (diff + f)
            dt = datetime.fromtimestamp(prev_val)

        sec_str = dt.strftime("%H:%M:%S")

        digit = next((i for i, th in enumerate(self.thresholds) if spacing >= th), len(self.thresholds))
        us_str = f".{str(int(dt.microsecond / 10 ** (6 - digit))).zfill(digit)}" if digit > 0 else ""

        return f"{sec_str}{us_str}"

    def tickStrings(self, values, scale, spacing):
        return [f"{self.calc_sec(v, spacing)}" for v in values]

class DoubleAxisWidget(pg.GraphicsLayoutWidget):
    X_LIMIT = (-700, 30700)
    Y_LIMIT_STRAIN = (-40000, 40000)
    Y_LIMIT_TEMP = (-150, 150)

    def __init__(self, channels, x_axis: TimeAxis = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._channels = channels
        self._strain_colors:list[str] = [""] * channels
        self._temp_colors:list[str] = [""] * channels
        self._widths:list[float] = [0] * channels
        self._offset:list[int] = [0] * channels

        self.x_axis: TimeAxis = x_axis
        if self.x_axis is not None:
            self.plot = pg.PlotItem(axisItems={"bottom": self.x_axis})
        else:
            self.plot = pg.PlotItem()
        self.plot.hideAxis("left")
        self.plot.hideButtons()
        self.plot.vb.setLimits(xMin=self.X_LIMIT[0], xMax=self.X_LIMIT[1], minXRange=1, maxXRange=self.X_LIMIT[1]-self.X_LIMIT[0])
        self.plot.vb.setMenuEnabled(False)
        self.y_axis_strain = YAxisWidget("strain", "left")
        self.y_axis_temp = YAxisWidget("temperature", "right")

        self.addItem(self.y_axis_strain, 0, 0)
        self.addItem(self.plot, 0, 1)
        self.addItem(self.y_axis_temp, 0, 2)

        self.strain_area = pg.ViewBox()
        self.strain_area.setXLink(self.plot)
        self.strain_area.setRange(yRange=range(-100, 100), disableAutoRange=True)
        self.strain_area.setLimits(yMin=self.Y_LIMIT_STRAIN[0], yMax=self.Y_LIMIT_STRAIN[1], minYRange=0.1, maxYRange=self.Y_LIMIT_STRAIN[1] - self.Y_LIMIT_STRAIN[0])
        self.strain_area.setMenuEnabled(False)
        self.y_axis_strain.axis().linkToView(self.strain_area)
        self.plot.scene().addItem(self.strain_area)

        self.temp_area = pg.ViewBox()
        self.temp_area.setXLink(self.plot)
        self.temp_area.setRange(yRange=range(-10, 40), disableAutoRange=True)
        self.temp_area.setLimits(yMin=self.Y_LIMIT_TEMP[0], yMax=self.Y_LIMIT_TEMP[1], minYRange=0.1, maxYRange=self.Y_LIMIT_TEMP[1] - self.Y_LIMIT_TEMP[0])
        self.temp_area.setMenuEnabled(False)
        self.y_axis_temp.axis().linkToView(self.temp_area)
        self.plot.scene().addItem(self.temp_area)

        self.plot.vb.setRange(xRange=range(self.X_LIMIT[0], self.X_LIMIT[1]))

        self.strain_plots: list[pg.PlotDataItem] = []
        self.temp_plots: list[pg.PlotDataItem] = []
        for i in range(channels):
            strain_plot = pg.PlotDataItem()
            self.strain_area.addItem(strain_plot)
            self.strain_plots.append(strain_plot)

            temp_plot = pg.PlotDataItem()
            self.temp_area.addItem(temp_plot)
            self.temp_plots.append(temp_plot)

        self.plot.vb.sigResized.connect(self.update_views)
        self.plot.autoBtn.clicked.connect(self.reset_range)
        self.update_views()

    def reset_range(self):
        strain_mins, strain_maxes = [], []
        for plot in self.strain_plots:
            plot_range = plot.dataBounds(1)
            plot_visible = plot.isVisible() and (plot_range[0] != 0 or plot_range[1] != 0)
            strain_mins.append(plot_range[0] if plot_visible else None)
            strain_maxes.append(plot_range[1] if plot_visible else None)
        strain_mins = [data + offset for data, offset in zip(strain_mins, self._offset) if data]
        strain_maxes = [data + offset for data, offset in zip(strain_maxes, self._offset) if data]
        if (len(strain_mins) > 0) and (len(strain_maxes) > 0):
            self.strain_area.setRange(yRange=(min(strain_mins), max(strain_maxes)), disableAutoRange=True)

        temp_mins, temp_maxes = [], []
        for plot in self.temp_plots:
            plot_range = plot.dataBounds(1)
            plot_visible = plot.isVisible() and (plot_range[0] != 0 or plot_range[1] != 0)
            temp_mins.append(plot_range[0] if plot_visible else None)
            temp_maxes.append(plot_range[1] if plot_visible else None)
        temp_mins = [data + offset for data, offset in zip(temp_mins, self._offset) if data]
        temp_maxes = [data + offset for data, offset in zip(temp_maxes, self._offset) if data]
        if (len(temp_mins) > 0) and (len(temp_maxes) > 0):
            self.temp_area.setRange(yRange=(min(temp_mins), max(temp_maxes)), disableAutoRange=True)

    def update_views(self):
        plot_vb = self.plot.vb
        self.strain_area.setGeometry(plot_vb.sceneBoundingRect())
        self.temp_area.setGeometry(plot_vb.sceneBoundingRect())

    def update_strain_graph(self, index, y_data, x_data: list = None):
        if index >= self._channels:
            return
        if x_data is None:
            x_data = range(0, len(y_data))
        self.strain_plots[index].setData(x_data, y_data)

    def update_temp_graph(self, index, y_data, x_data: list = None):
        if index >= self._channels:
            return
        if x_data is None:
            x_data = range(0, len(y_data))
        self.temp_plots[index].setData(x_data, y_data)

    def update_x_limit(self, range_min, range_max):
        self.plot.vb.setLimits(xMin=range_min, xMax=range_max, minXRange=0.1, maxXRange=range_max - range_min)
        self.strain_area.setLimits(xMin=range_min, xMax=range_max, minXRange=0.1, maxXRange=range_max - range_min)
        self.temp_area.setLimits(xMin=range_min, xMax=range_max, minYRange=0.1, maxYRange=range_max - range_min)

    def update_x_data(self, x_data: list):
        if self.x_axis is not None:
            self.x_axis.set_overwrite_values(x_data)

    def update_strain_graph_line(self, index):
        if index >= self._channels:
            return
        self.strain_plots[index].setPen(pg.mkPen(color=self._strain_colors[index], width=self._widths[index]))

    def update_temp_graph_line(self, index):
        if index >= self._channels:
            return
        self.temp_plots[index].setPen(pg.mkPen(color=self._temp_colors[index], width=self._widths[index]))

    def set_strain_visible(self, index: int, visible: bool):
        if index < len(self.strain_plots):
            self.strain_plots[index].setVisible(visible)

    def set_temp_visible(self, index: int, visible: bool):
        if index < len(self.temp_plots):
            self.temp_plots[index].setVisible(visible)

    def set_strain_graph_color(self, index, color: str):
        if index >= self._channels:
            return
        self._strain_colors[index] = color
        self.update_strain_graph_line(index)

    def set_temp_graph_color(self, index, color: str):
        if index >= self._channels:
            return
        self._temp_colors[index] = color
        self.update_temp_graph_line(index)

    def set_graph_line_width(self, index:int, width: float):
        if index >= self._channels:
            return
        self._widths[index] = width
        self.update_strain_graph_line(index)
        self.update_temp_graph_line(index)

    def set_graph_offset(self, index, offset:int):
        if index >= self._channels:
            return
        self._offset[index] = offset
        self.strain_plots[index].setPos(0, offset)
        self.temp_plots[index].setPos(0, offset)

    def zoom_x(self, magnification: float):
        x_range = self.plot.getAxis("bottom").range
        new_min, new_max = zoom_range(x_range[0], x_range[1], magnification)
        self.plot.vb.setXRange(new_min, new_max, padding=0)

    def zoom_strain(self, magnification: float):
        strain_range = self.y_axis_strain.range()
        new_min, new_max = zoom_range(strain_range[0], strain_range[1], magnification)
        self.strain_area.setYRange(new_min, new_max, padding=0)

    def zoom_temp(self, magnification: float):
        temp_range = self.y_axis_temp.range()
        new_min, new_max = zoom_range(temp_range[0], temp_range[1], magnification)
        self.temp_area.setYRange(new_min, new_max, padding=0)

def zoom_range(range_min, range_max, magnification):
    range_mid = (range_min + range_max) / 2
    new_max = range_max + (range_max - range_mid) * (magnification - 1.0)
    new_min = range_min - (range_mid - range_min) * (magnification - 1.0)
    return new_min, new_max


class MovingAverageWidget(pg.GraphicsLayoutWidget):
    X_LIMIT = (-700, 30700)
    Y_LIMIT_STRAIN = (-40000, 40000)

    def __init__(self, channels: int, *args, **kargs):
        super().__init__(*args, **kargs)
        self.window_size: int = 2
        self.unit = 0
        self.is_measuring = False
        self.is_plotting = False

        self.logs: dict[BoardKind, MeasureLog] = {}
        self.board_sensors: dict[int, list[int]] = {}
        self.board_time: dict[BoardKind, list] = {}
        self.board_prev_count: dict[BoardKind, int] = {}

        self.strains: dict[int, Deque[float]] = {}
        self.strain_values: dict[int, Deque[float]] = {}
        self.strain_means: dict[int, list] = {}
        self.strain_value_means: dict[int, list] = {}

        self.x_axis = TimeAxis(orientation="bottom")
        self.plot = pg.PlotItem(axisItems={"bottom": self.x_axis})
        self.plot.setLabel("left", "strain")
        self.plot.vb.setLimits(xMin=self.X_LIMIT[0], xMax=self.X_LIMIT[1], minXRange=1, maxXRange=self.X_LIMIT[1]-self.X_LIMIT[0])
        self.plot.vb.setRange(xRange=range(self.X_LIMIT[0], self.X_LIMIT[1]))
        self.plot.vb.setMenuEnabled(False)
        self.addItem(self.plot)

        self.ma_plots: list[pg.PlotDataItem] = []
        for i in range(channels):
            ma_plot = pg.PlotDataItem()
            self.plot.addItem(ma_plot)
            self.ma_plots.append(ma_plot)

    def set_window_size(self, size: int):
        # 測定中は変更を受け付けない
        if not self.is_measuring:
            self.window_size = size

    def set_graph_color(self, index: int, color):
        if index < len(self.ma_plots):
            self.ma_plots[index].setPen(color=color)

    def set_graph_offset(self, index: int, offset: int):
        if index < len(self.ma_plots):
            self.ma_plots[index].setPos(0, offset)

    def set_visible(self, index: int, is_visible: bool):
        if index < len(self.ma_plots):
            self.ma_plots[index].setVisible(is_visible)

    def set_log(self, logs: dict[BoardKind, MeasureLog]):
        self.logs = logs

    def start(self, channels: list[int], offsets: list[int], sensor_num: list[int]):
        self.board_time = {board: [] for board in BoardKind}
        self.board_sensors = {board: [ch + offset for ch in range(num)] for board, (offset, num) in enumerate(zip(offsets, sensor_num))}
        self.board_prev_count = {board: 0 for board in BoardKind}

        self.strains = {ch: Deque([], maxlen=30000) for ch in channels}
        self.strain_values = {ch: Deque([], maxlen=30000) for ch in channels}
        for plot in self.ma_plots:
            plot.clear()
        self.is_measuring = True

    def stop(self):
        # 測定停止後に最新のグラフに更新する
        self.is_measuring = False
        while self.is_plotting:
            pass
        self.update_graph()
        for log in self.logs.values():
            log.stop()
        self.logs.clear()

    def add_data(self, channel: int, strain: float, strain_value: float):
        if not self.is_measuring:
            return
        strains = self.strains.get(channel, None)
        strain_values = self.strain_values.get(channel, None)
        if strains is None or strain_values is None:
            return

        strains.append(strain)
        strain_values.append(strain_value)

    def increment_prev_count(self, board: BoardKind):
        if board in self.board_prev_count:
            self.board_prev_count[board] += 1

    def update_time(self, board: BoardKind, times: list):
        self.board_time[board] = times
        self.x_axis.set_overwrite_values(times)

    def update_unit(self, unit: int):
        self.unit = unit
        self.update_graph()

    def calc_means(self, index: int) -> list:
        if index not in self.strains or index not in self.strain_values:
            return []
        df = pd.DataFrame(data={"strain": list(self.strains[index])})
        strain_means = df["strain"].rolling(self.window_size, min_periods=1).mean().to_list()
        self.strain_means[index] = strain_means

        df = pd.DataFrame(data={"strain": list(self.strain_values[index])})
        strain_value_means = df["strain"].rolling(self.window_size, min_periods=1).mean().to_list()
        self.strain_value_means[index] = strain_value_means

        return strain_means if self.unit == ChartUnitKind.lsb.value else strain_value_means

    def append_log(self, board: BoardKind):
        times = self.board_time.get(board, [])
        sensors = self.board_sensors.get(board.value, [])
        prev_count = self.board_prev_count.get(board, 0)
        if board not in self.logs or len(times) == 0 or prev_count == 0:
            return

        times = times[-prev_count:]
        strain_means: list[list] = []
        strain_value_means: list[list] = []
        for ch in sensors:
            strain_means.append(self.strain_means.get(ch, [])[-prev_count:])
            strain_value_means.append(self.strain_value_means.get(ch, [])[-prev_count:])
        for i in range(len(times)):
            sec, ns = str(times[i]).split(".")
            try:
                log = f"{self.logs[board].time_to_str(int(sec), int(ns))}"
            except ValueError:
                log = f"-"
            for strain_mean, strain_value_mean in zip(strain_means, strain_value_means):
                log += ",-,-"
                log += f",{strain_mean[i]:.3f}" if i < len(strain_mean) else ",-"
                log += f",{strain_value_mean[i]:.3f}" if i < len(strain_value_mean) else ",-"
            self.logs[board].save(log + ",\n")

    def update_graph(self):
        if self.is_plotting:
            return
        self.is_plotting = True
        for index, ma_plot in enumerate(self.ma_plots):
            ma_plot.setData(self.calc_means(index))
        for board in self.logs.keys():
            self.append_log(board)
        for board in self.board_prev_count.keys():
            self.board_prev_count[board] = 0
        self.is_plotting = False


@dataclasses.dataclass
class FftWindows(Enum):
    Rectangular = 1
    Hanning = 2
    Hamming = 3
    BlackMan = 4
    BlackMan_Harris = 5
    Flat_top = 6

@dataclasses.dataclass
class FftSettings:
    enable: bool = False
    resolution: int = 0
    window: int = 0
    use_schedule_setting: bool = False
    start_day: str = ""
    start_time: str = ""
    start_datetime: datetime = None
    interval: int = 0

class FFTWidget(pg.GraphicsLayoutWidget):
    X_LIMIT = (-10, 550)
    Y_LIMIT = (-5, 100)

    def __init__(self, channels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_measuring = False
        self.is_drawing = False
        self.last_update: datetime = datetime.now()
        self.delay_timer = QtCore.QTimer()
        self.update_timer = QtCore.QTimer()
        self.delay_timer.timeout.connect(self.delay_update_start)
        self.update_timer.timeout.connect(self.update_graph)

        self._fft_settings: FftSettings = FftSettings()
        self._sampling_rate: int = 1000
        self.logs: dict[int, Log] = {}
        self._channels = channels

        self.plot = pg.PlotItem()
        self.plot.setLabel("left", "Amplitude")
        self.plot.setLabel("bottom", "Frequency")
        self.addItem(self.plot)

        self.fft_plots: list[pg.PlotDataItem] = []
        self.fft_data: dict[int, Deque[float]] = {}
        for i in range(channels):
            fft_plot = pg.PlotDataItem()
            self.plot.addItem(fft_plot)
            self.fft_plots.append(fft_plot)

        self.plot.vb.setLimits(xMin=self.X_LIMIT[0], xMax=self.X_LIMIT[1], minXRange=0.1, maxXRange=self.X_LIMIT[1] - self.X_LIMIT[0],
                               yMin=self.Y_LIMIT[0], yMax=self.Y_LIMIT[1], minYRange=0.1, maxYRange=self.Y_LIMIT[1] - self.Y_LIMIT[0])
        self.plot.vb.setMenuEnabled(False)
        self.plot.vb.setXRange(self.X_LIMIT[0], self.X_LIMIT[1])

    def set_fft_settings(self, settings: FftSettings):
        # 測定中は変更を受け付けない
        if not self.is_measuring:
            self._fft_settings = settings
            if self._fft_settings.interval < 1:
                self._fft_settings.interval = 1

    def set_log(self, dst: str, prefix: str, max_row: int, channels: list[int]):
        self.logs.clear()
        for i in channels:
            log = Log(prefix=prefix, max_row=max_row, name=f"FFT_ch{i+1}")
            log.set_dst_dir(dst)
            self.logs[i] = log

    def start(self, sampling_rate: int, channels: list[int]):
        # TBD：X軸の下限は上限に応じて変える
        self._sampling_rate = sampling_rate
        x_max = 1 if sampling_rate < 2 else sampling_rate // 2
        self.plot.vb.setLimits(xMin=self.X_LIMIT[0], xMax=x_max, minXRange=0.1, maxXRange=x_max - self.X_LIMIT[0],
                               yMin=self.Y_LIMIT[0], yMax=self.Y_LIMIT[1], minYRange=0.1, maxYRange=self.Y_LIMIT[1] - self.Y_LIMIT[0])

        # データは解像度の倍必要になる
        data_num = self._fft_settings.resolution * 2
        self.fft_data.clear()
        for ch in channels:
            self.fft_data[ch] = Deque([], data_num)

        for fft_plot in self.fft_plots:
            fft_plot.clear()

        # ログのヘッダに周波数を書きこむ
        freq = np.fft.fftfreq(data_num, 1 / self._sampling_rate)
        header = ",".join([str(f) for f in freq[:data_num // 2].tolist()]) + "\n"
        for log in self.logs.values():
            log.set_header(header)
            log.start()

        self.is_measuring = True
        self.delay_timer.start(1000)
        self.delay_update_start()

    def add_data(self, index: int, value: float):
        data = self.fft_data.get(index, None)
        if data is not None:
            data.append(value)

    def delay_update_start(self):
        if datetime.now() >= self._fft_settings.start_datetime:
            self.last_update = self._fft_settings.start_datetime
            self.update_timer.start(1000)
            self.update_graph()
            self.delay_timer.stop()

    def update_graph(self):
        if self.is_drawing:
            return
        # 更新時刻 = 開始時刻 + 更新頻度 * n
        diff = Decimal(str((datetime.now() - self.last_update).total_seconds())).quantize(Decimal("0"), ROUND_HALF_UP)
        if int(diff) % self._fft_settings.interval != 0:
            return
        self.last_update = datetime.now()

        self.is_drawing = True
        for ch, data in self.fft_data.items():
            if len(data) > 0:
                freq, amp = self.calc_fft(list(data))
                if len(freq) < 1:
                    continue
                self.fft_plots[ch].setData(freq, amp)

                # ログがあれば記録する
                log = self.logs.get(ch, None)
                if log is not None:
                    log.save(",".join([str(val) for val in amp]) + "\n")
        self.is_drawing = False

    def calc_fft(self, data: list[float]) -> tuple[list[float], list[float]]:
        data_num = self._fft_settings.resolution * 2
        if len(data) < data_num:
            return [], []

        try:
            n_array = np.array(data)
            n_array.resize(data_num)
        except ValueError:
            print("Make Array Error")
            return [], []

        window = get_window(self._fft_settings.window, data_num)
        fft_result = fft(n_array * window, data_num)

        # 振幅はサンプル数で正規化する。また、FFTにより振幅が半分になるので倍化する
        freq = np.fft.fftfreq(data_num, 1 / self._sampling_rate)
        amp = np.abs(fft_result) / data_num * 2
        # ナイキスト周波数（サンプリング周波数の半分）までが正確なデータになる
        return freq[:data_num // 2].tolist(), amp[:data_num // 2].tolist()

    def stop(self):
        # 描画終了を待ってからログを閉じる
        self.delay_timer.stop()
        self.update_timer.stop()
        while self.is_drawing:
            pass

        for log in self.logs.values():
            log.stop()
        self.logs.clear()

        self.is_measuring = False

    def set_graph_color(self, index: int, color):
        if index < len(self.fft_plots):
            self.fft_plots[index].setPen(color=color)

    def set_visible(self, index: int, is_visible: bool):
        if index < len(self.fft_plots):
            self.fft_plots[index].setVisible(is_visible)


def get_window(window: int, data_num: int):
    if window == FftWindows.Hanning.value:
        return scipy_signal.windows.hann(data_num)
    elif window == FftWindows.Hamming.value:
        return scipy_signal.windows.hamming(data_num)
    elif window == FftWindows.BlackMan.value:
        return scipy_signal.windows.blackman(data_num)
    elif window == FftWindows.BlackMan_Harris.value:
        return scipy_signal.windows.blackmanharris(data_num)
    elif window == FftWindows.Flat_top.value:
        return scipy_signal.windows.flattop(data_num)
    elif window == FftWindows.Rectangular.value:
        return np.ones(data_num)
    else:
        return np.ones(data_num)


class CsvPreviewWidget(DoubleAxisWidget):
    thresholdMinChanged = Signal(int)
    thresholdMinDateChanged = Signal(str)
    thresholdMaxChanged = Signal(int)
    thresholdMaxDateChanged = Signal(str)

    def __init__(self, channels: int, x_axis: TimeAxis, parent=None):
        super().__init__(channels=channels, x_axis=x_axis, parent=parent)
        self.min_th = 0
        self.max_th = 30000
        self.range_selector = pg.LinearRegionItem(values=(0, 30000), swapMode="block", pen=pg.mkPen(color="w", width=2))
        self.range_selector.sigRegionChanged.connect(self.verify_region)
        # 本来であればsigRegionChangedのみで問題ないはずだが、端が消える問題が発生したためその対策でsigRegionChangeFinishedでも同じ処理を行う
        self.range_selector.sigRegionChangeFinished.connect(self.verify_region)
        self.plot.addItem(self.range_selector)

    def set_threshold(self, min_th: int, max_th: int):
        self.min_th = min_th
        self.max_th = max_th
        self.set_start_val(min_th)
        self.set_end_val(max_th)
        self.plot.vb.setRange(xRange=range(min_th, max_th))

    def set_start_val(self, start_val: int):
        now_region = self.range_selector.getRegion()
        self.range_selector.setRegion((int(start_val), now_region[1]))
        self.verify_start_val()

    def set_end_val(self, end_val: int):
        now_region = self.range_selector.getRegion()
        self.range_selector.setRegion((now_region[0], int(end_val)))
        self.verify_end_val()

    def get_start_str(self):
        return self.x_axis.calc_sec(self.range_selector.getRegion()[0], 1000)

    def get_end_str(self):
        return self.x_axis.calc_sec(self.range_selector.getRegion()[1], 1000)

    def verify_region(self):
        self.verify_start_val()
        self.verify_end_val()

    def verify_start_val(self):
        start_val, end_val = self.range_selector.getRegion()
        new_start_val = max(min(start_val, end_val - 1), self.min_th)
        self.range_selector.setRegion((new_start_val, end_val))
        self.thresholdMinChanged.emit(new_start_val)
        self.thresholdMinDateChanged.emit(self.get_start_str())

    def verify_end_val(self):
        start_val, end_val = self.range_selector.getRegion()
        new_end_val = min(max(start_val + 1, end_val), self.max_th)
        self.range_selector.setRegion((start_val, new_end_val))
        self.thresholdMaxChanged.emit(new_end_val)
        self.thresholdMaxDateChanged.emit(self.get_end_str())

    def get_strains(self, channel: int) -> list[float]:
        if channel > len(self.strain_plots):
            return []
        _, strain_data = self.strain_plots[channel].getData()
        if strain_data is None:
            return []
        return strain_data.tolist()

    def calc_min_max_mean(self, channel: int) -> tuple[bool, tuple | None]:
        strains = self.get_strains(channel)
        start_val, end_val = self.range_selector.getRegion()
        new_list = strains[int(start_val):int(end_val) + 1]

        if len(new_list) < 1:
            return False, None
        else:
            return True, (min(new_list), max(new_list), float(np.mean(new_list)))

    def calc_std(self, channel: int) -> tuple[bool, float | None]:
        strains = self.get_strains(channel)
        start_val, end_val = self.range_selector.getRegion()
        new_list = strains[int(start_val):int(end_val) + 1]

        if len(new_list) < 2:
            return False, None
        else:
            return True, float(np.std(new_list))


class ChartTabs(QMainWindow):
    dockTabMoved = Signal()

    def __init__(self, parent=None):
        super(ChartTabs, self).__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.graph_data: dict[BoardKind, GraphData] = {}
        self.is_drawing = False

        # グラフ用の固定タブ
        self.main_tab = self.add_tab(title="Main")
        self.main_tab.setFeatures(self.main_tab.features() ^ QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.main_plot_area = DoubleAxisWidget(channels=8, x_axis=TimeAxis(orientation="bottom"))
        self.main_tab.setWidget(self.main_plot_area)

        # 移動平均用の固定タブ
        self.ma_tab = self.add_tab(title="Moving Average")
        self.ma_plot_area = MovingAverageWidget(channels=8)
        self.ma_tab.setWidget(self.ma_plot_area)

        # FFT用の固定タブ
        self.fft_tab = self.add_tab(title="FFT")
        self.fft_plot_area = FFTWidget(channels=8)
        self.fft_tab.setWidget(self.fft_plot_area)

        # CSVプレビュー用の固定タブ
        self.csv_tab = self.add_tab(title="CSV Preview")
        self.csv_tab.setObjectName("csv_prev_tab")
        self.csv_tab.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.csv_plot_area = CsvPreviewWidget(channels=8, x_axis=TimeAxis(orientation="bottom"), parent=self)
        self.csv_tab.setWidget(self.csv_plot_area)

        self.unit = ChartUnitKind.strain.value

    def add_tab(self, title="", is_temp=False):
        dock_tab = QDockWidget(self, windowTitle=title)
        if is_temp:
            dock_tab.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        dock_tab.dockLocationChanged.connect(lambda: self.dockTabMoved.emit())
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock_tab, QtCore.Qt.Orientation.Horizontal)
        return dock_tab

    def clear_meas_data(self, boards: list[BoardKind], offsets: list[int], sensor_num: list[int]):
        self.graph_data.clear()
        for board, offset, sensor_num in zip(boards, offsets, sensor_num):
            self.graph_data[board] = GraphData()
            self.graph_data[board].init_sensors(sensor_num, offset)

    def add_meas_data(self, board: BoardKind, meas_data: list[MeasureData]):
        graph_data = self.graph_data.get(board, None)
        if graph_data is None:
            return

        ch_offset = graph_data.get_ch_offset()
        for m_data in meas_data:
            graph_data.add_time(m_data.seconds, m_data.nanoseconds)

            # ストリーム内のセンサー順に対応（通常は sensor_data と同じ長さ）
            strain_values = list(m_data.strain_value)
            for ch, data in enumerate(m_data.sensor_data):
                if ch >= len(strain_values):
                    # TBD：必要なら警告ログや継続／中断の方針を決める
                    continue

                graph_data.add_data(ch, data.strain, data.temp, data.status, strain_values[ch])
                self.ma_plot_area.add_data(ch + ch_offset, data.strain, strain_values[ch])
                self.fft_plot_area.add_data(ch + ch_offset, data.strain)
            self.ma_plot_area.increment_prev_count(board)

    def set_unit(self, unit:int):
        self.unit = unit
        self.ma_plot_area.update_unit(unit)
        self.update_graph()

    def update_graph(self):
        if self.is_drawing:
            return

        self.is_drawing = True
        for board, graph_data in self.graph_data.items():
            self.main_plot_area.update_x_data(graph_data.get_time())
            self.ma_plot_area.update_time(board, graph_data.get_time())

            ch_offset = graph_data.get_ch_offset()
            for i in range(0, graph_data.get_sensor_num()):
                if self.unit == ChartUnitKind.strain.value:
                    strains = graph_data.get_strain_values(i)
                else:
                    strains = graph_data.get_strains(i)
                temps = graph_data.get_temps(i)
                self.main_plot_area.update_strain_graph(i + ch_offset, strains)
                self.main_plot_area.update_temp_graph(i + ch_offset, temps)
        self.ma_plot_area.update_graph()
        self.is_drawing = False

    def rebalance_docks(self):
        docks = self.findChildren(QDockWidget)
        target_docks = [d for d in docks if not d.isFloating() and d.isVisible()]
        if not target_docks:
            return
        width_per_dock = self.width() // len(target_docks)
        sizes = [width_per_dock] * len(target_docks)
        self.resizeDocks(target_docks, sizes, QtCore.Qt.Orientation.Horizontal)

    def toggle_ma_tab(self, prev: bool):
        self.ma_tab.setVisible(prev)
        if prev:
            self.rebalance_docks()

    def set_ma_log(self, logs: dict[BoardKind, MeasureLog]):
        if self.ma_tab.isVisible():
            self.ma_plot_area.set_log(logs)

    def ma_start(self, channels: list[int], offsets: list[int], sensor_num: list[int]):
        if self.ma_tab.isVisible():
            self.ma_plot_area.start(channels, offsets, sensor_num)

    def ma_stop(self):
        self.ma_plot_area.stop()

    def toggle_fft_tab(self, prev: bool):
        self.fft_tab.setVisible(prev)
        if prev:
            self.rebalance_docks()

    def make_fft_log(self, max_row, dst, prefix, channels: list[int]):
        if self.fft_tab.isVisible():
            self.fft_plot_area.set_log(dst, prefix, max_row, channels)

    def fft_start(self, sampling_rate, channels: list[int]):
        if self.fft_tab.isVisible():
            self.fft_plot_area.start(sampling_rate, channels)

    def fft_stop(self):
        self.fft_plot_area.stop()

    def toggle_csv_tab(self, prev: bool):
        self.csv_tab.setVisible(prev)
        if prev:
            self.rebalance_docks()

    def zoom_x(self, magnification: float):
        self.main_plot_area.zoom_x(magnification)
    def zoom_strain(self, magnification: float):
        self.main_plot_area.zoom_strain(magnification)
    def zoom_temp(self, magnification: float):
        self.main_plot_area.zoom_temp(magnification)

class SensorSetting(QObject):
    channelChanged = Signal()
    strainLineColorChanged = Signal()
    tempLineColorChanged = Signal()
    lineWidthChanged = Signal()
    lineOffsetChanged = Signal()
    changeStrainLineColor = Signal(int, str)
    changeTempLineColor = Signal(int, str)
    changeLineWidth = Signal(int, int)
    changeLineOffset = Signal(int, int)

    # TBD：QML側からでもcolor/widthを参照可能（Propertyが必要）
    def __init__(self, ch:int):
        super(SensorSetting, self).__init__()
        self.colors = ["#e53935", "#fb8c00", "#fdd835", "#43a047", "#00acc1", "#1e88e5", "#8e24aa", "#9e9e9e", "#212121", "#ffffff"]
        self.widths = [1.0, 1.5, 2.0, 3.0, 10.0]
        self._ch = ch
        self._strain_line_color:int = -1
        self._temp_line_color:int = -1
        self._line_width:int = -1
        self._line_offset:int = 0

    def get_color(self, index):
        return self.colors[index]

    def get_width(self, index):
        return self.widths[index]

    @Property(int, notify=channelChanged)
    def ch(self):
        return self._ch

    @Property(int, notify=strainLineColorChanged)
    def strain_line_color(self):
        return self._strain_line_color

    @Property(int, notify=tempLineColorChanged)
    def temp_line_color(self):
        return self._temp_line_color

    @Property(int, notify=lineWidthChanged)
    def line_width(self):
        return self._line_width

    @Property(int, notify=lineOffsetChanged)
    def line_offset(self):
        return self._line_offset

    @Slot(int)
    def change_strain_line_color_index(self, color_index):
        self._strain_line_color = color_index
        self.changeStrainLineColor.emit(self._ch, self.get_color(color_index))
    @Slot(int)
    def change_temp_line_color_index(self, color_index):
        self._temp_line_color = color_index
        self.changeTempLineColor.emit(self._ch, self.get_color(color_index))
    @Slot(int)
    def change_line_width_index(self, line_width):
        self._line_width = line_width
        self.changeLineWidth.emit(self._ch, self.get_width(line_width))
    @Slot(int)
    def change_line_offset_value(self, offset):
        self._line_offset = offset
        self.changeLineOffset.emit(self._ch, offset)

    def update_strain_line_color_index(self, color_index):
        self._strain_line_color = color_index
        self.strainLineColorChanged.emit()

    def update_temp_line_color_index(self, color_index):
        self._temp_line_color = color_index
        self.tempLineColorChanged.emit()

    def update_line_width_index(self, width_index):
        self._line_width = width_index
        self.lineWidthChanged.emit()

    def update_line_offset_index(self, offset_index):
        self._line_offset = offset_index
        self.lineOffsetChanged.emit()
        # 他のプロパティはQML側で値の変更を検出してSignalが発行されるが
        # オフセットはTextFieldであり、編集完了時にしかSignalが発行されないようにしてある。
        # (1桁入力するごとにグラフが変化しないように)
        # そのため、ここで直接オフセット変更のSignalを発行する
        self.changeLineOffset.emit(self._ch, offset_index)

    def get_settings(self):
        return self._strain_line_color, self._temp_line_color, self._line_width, self._line_offset


class FilterSetting(QObject):
    movingAverageChanged = Signal()
    movingAverageWindowSizeChanged = Signal()
    fftChanged = Signal()
    fftResolutionChanged = Signal()
    fftWindowChanged = Signal()
    fftErrorChanged = Signal()
    standardDeviationChanged = Signal()
    standardDeviationWindowSizeChanged = Signal()

    changeMovingAverage = Signal(bool)
    changeMovingAverageWindowSize = Signal(int)
    changeFft = Signal(bool)
    changeFftResolution = Signal(int)
    changeFftWindow = Signal(int)
    changeStandardDeviation = Signal(bool)
    changeStandardDeviationWindowSize = Signal(int)

    def __init__(self):
        super(FilterSetting, self).__init__()
        self._moving_average = False
        self._moving_average_window_size = 1
        self._fft_settings = FftSettings()
        self._fft_start_time_error = False
        self._standard_deviation = False
        self._standard_deviation_window_size = 1

        self._fft_windows = ["-", "Rectangular", "Hanning", "Hamming", "Blackman", "Blackman-Harris", "Flat-top"]

    @Property(bool, notify=movingAverageChanged)
    def moving_average(self):
        return self._moving_average
    @Property(int, notify=movingAverageWindowSizeChanged)
    def moving_average_window_size(self):
        return self._moving_average_window_size
    @Property(bool, notify=fftChanged)
    def fft(self):
        return self._fft_settings.enable
    @Property(int, notify=fftResolutionChanged)
    def fft_resolution(self):
        return self._fft_settings.resolution
    @Property(int, notify=fftWindowChanged)
    def fft_window(self):
        return self._fft_settings.window
    @Property(bool, notify=fftErrorChanged)
    def fft_start_time_error(self):
        return self._fft_start_time_error
    @Property(bool, notify=standardDeviationChanged)
    def standard_deviation(self):
        return self._standard_deviation
    @Property(int, notify=standardDeviationWindowSizeChanged)
    def standard_deviation_window_size(self):
        return self._standard_deviation_window_size

    @Slot(bool)
    def change_moving_average(self, on_off):
        self._moving_average = on_off
        self.changeMovingAverage.emit(self._moving_average)
    @Slot(int)
    def change_moving_average_window_size(self, size):
        self._moving_average_window_size = size
        self.changeMovingAverageWindowSize.emit(self._moving_average_window_size)
    @Slot(bool)
    def change_fft(self, on_off):
        self._fft_settings.enable = on_off
        self.changeFft.emit(on_off)
    @Slot(int)
    def change_fft_resolution(self, size):
        self._fft_settings.resolution = size
        self.changeFftResolution.emit(size)
    @Slot(int)
    def change_fft_window(self, window):
        self._fft_settings.window = window
        self.changeFftWindow.emit(window)
    @Slot(bool)
    def change_fft_use_schedule(self, value):
        self._fft_settings.use_schedule_setting = value
    @Slot(str)
    def change_fft_start_day(self, day):
        self._fft_settings.start_day = day
    @Slot(str)
    def change_fft_start_time(self, time):
        self._fft_settings.start_time = time
    @Slot(int)
    def change_fft_interval(self, interval):
        self._fft_settings.interval = interval
    @Slot(bool)
    def change_standard_deviation(self, on_off):
        self._standard_deviation = on_off
        self.changeStandardDeviation.emit(self._standard_deviation)
    @Slot(int)
    def change_standard_deviation_window_size(self, size):
        self._standard_deviation_window_size = size
        self.changeStandardDeviationWindowSize.emit(self._standard_deviation_window_size)

    def update_moving_average(self, on_off:bool):
        self._moving_average = on_off
        self.movingAverageChanged.emit()
    def update_moving_average_window_size(self, size):
        self._moving_average_window_size = size
        self.movingAverageWindowSizeChanged.emit()
    def update_fft(self, on_off):
        self._fft_settings.enable = on_off
        self.fftChanged.emit()
    def update_fft_resolution(self, size):
        self._fft_settings.resolution = size
        self.fftResolutionChanged.emit()
    def update_fft_window(self, window: str):
        try:
            self._fft_settings.window = self._fft_windows.index(window)
        except ValueError:
            self._fft_settings.window = 0
        self.fftWindowChanged.emit()
    def update_fft_start_date_error(self, value: bool):
        self._fft_start_time_error = value
        self.fftErrorChanged.emit()
    def update_standard_deviation(self, on_off):
        self._standard_deviation = on_off
        self.standardDeviationChanged.emit()
    def update_standard_deviation_window_size(self, size):
        self._standard_deviation_window_size = size
        self.standardDeviationWindowSizeChanged.emit()

    def get_ma_settings(self) -> tuple[bool, int]:
        return self._moving_average, self._moving_average_window_size
    def get_fft_window(self) -> str:
        return self._fft_windows[self._fft_settings.window]
    def get_fft_settings(self) -> FftSettings:
        return self._fft_settings


class SensorDataTableColumnKind(Enum):
    view = 0
    name = 1
    temp = 2
    current = 3
    init = 4
    delta = 5
    status = 6
    num = 7

class ChartPage(QWidget):
    autoBalanceRequested = Signal()

    def __init__(self, parent=None):
        super(ChartPage, self).__init__(parent)
        # QML色変え用
        self.app_bridge = DummyAppBridge(initial_theme=0)
        self.ui = Chart_Page.Ui_chart_page()
        self.ui.setupUi(self)

        #計測画面QML色変え用
        if self.app_bridge is not None:
            self.ui.ma_settings.rootContext().setContextProperty("appBridge", self.app_bridge)
            self.ui.fft_settings.rootContext().setContextProperty("appBridge", self.app_bridge)
            self.ui.graph_settings_ch1.rootContext().setContextProperty("appBridge", self.app_bridge)
            self.ui.graph_settings_ch2.rootContext().setContextProperty("appBridge", self.app_bridge)
            self.ui.graph_settings_ch3.rootContext().setContextProperty("appBridge", self.app_bridge)
            self.ui.graph_settings_ch4.rootContext().setContextProperty("appBridge", self.app_bridge)

        self.log: MeasureLog = MeasureLog()

        self._sensor_info_label_list = []
        self.chart_unit:int = ChartUnitKind.strain.value
        self.column_show_settings = [True] * SensorDataTableColumnKind.num.value
        self.sensor_name = [f"#{i+1}" for i in range(8)]
        self.strain_line_view = [False for _ in range(8)]
        self.temp_line_view = [False for _ in range(8)]
        self.init_sensor_table()
        self.update_sensor_table_headers()
        self.connection_status = [SensorConnectionStatusKind.no_connect] * 8

        self.strain_action = QAction(self.tr("Strain Value(με)"), self, checked=True, checkable=True)
        self.lsb_action = QAction(self.tr("LSB"), self, checked=False, checkable=True)
        self.strain_action.toggled.connect(lambda checked: self.switch_unit(self.strain_action) if checked else None)
        self.lsb_action.toggled.connect(lambda checked: self.switch_unit(self.lsb_action) if checked else None)

        # QActionGroupで排他設定
        self.unit_group = QActionGroup(self)
        self.unit_group.setExclusive(True)
        self.unit_group.addAction(self.strain_action)
        self.unit_group.addAction(self.lsb_action)

        self.column_actions = []
        for i, name in enumerate(self.get_action_names(), start=1):
            action = QAction(name, self, checked=True, checkable=True)
            action.toggled.connect(partial(self.toggle_column, i))
            self.column_actions.append(action)
        self.ui.table_setting_button.clicked.connect(self.show_table_menu)

        # グラフ部分は動的に変化するので、コード上で生成する
        self.chart_tabs = ChartTabs(parent=self)
        self.chart_tabs.setObjectName("chart_tabs")
        # タブをドロップすると枠線が消えるので、リサイズして直している
        self.chart_tabs.dockTabMoved.connect(lambda : self.resize(QSize(self.width(), self.height() + 5)))
        self.chart_layout = QVBoxLayout()
        self.chart_layout.addWidget(self.chart_tabs)
        self.ui.chart_area.setLayout(self.chart_layout)
        self.prev_csv_enable = False

        self.ui.auto_balance_button.clicked.connect(self.auto_balance)
        self.ui.open_button.clicked.connect(lambda: self.open_file(self.tr("LogFile(*.csv);;ImageFile(*.png)"), self.add_log_tab))
        self.ui.csv_browse_button.clicked.connect(lambda: self.open_file(self.tr("LogFile(*.csv)"), self.add_csv_preview))
        self.ui.filter_config_button.clicked.connect(self.toggle_filter_settings)
        self.ui.sensor_config_button.clicked.connect(self.toggle_sensor_settings)
        self.ui.filter_settings_close_button.clicked.connect(self.close_filter_settings)
        self.ui.sensor_settings_close_button.clicked.connect(self.close_sensor_settings)
        self.ui.apply_filter_button.clicked.connect(self.apply_filter_settings)
        self.close_filter_settings()
        self.close_sensor_settings()

        re_pattern = QRegularExpression(r"^-?\d*(\.\d{0,2})?$")
        validator = QRegularExpressionValidator(re_pattern)
        self.ui.sampling_rate_edit.setValidator(validator)
        self.ui.sampling_rate_edit.editingFinished.connect(self.check_range)
        self.ui.sampling_rate_unit.currentIndexChanged.connect(self.check_range)
        self.ui.sampling_rate_unit.addItems(["Hz", "sps", "ms"])
        self._init_buffer_controls()

        self.fs_bridge = FilterSetting()
        self.ui.ma_settings.rootContext().setContextProperty("bridge", self.fs_bridge)
        self.ui.fft_settings.rootContext().setContextProperty("bridge", self.fs_bridge)
        #self.ui.sd_settings.rootContext().setContextProperty("bridge", self.fs_bridge)



        self.ui.filter_setting_tabs.currentChanged.connect(self.filter_settings_tab_changed)
        self.ui.csv_browse_edit.editingFinished.connect(self.csv_path_reload)

        self.ui.startpoint_edit.valueChanged.connect(self.chart_tabs.csv_plot_area.set_start_val)
        self.ui.endpoint_edit.valueChanged.connect(self.chart_tabs.csv_plot_area.set_end_val)
        self.chart_tabs.csv_plot_area.thresholdMinChanged.connect(self.ui.startpoint_edit.setValue)
        self.chart_tabs.csv_plot_area.thresholdMaxChanged.connect(self.ui.endpoint_edit.setValue)
        self.chart_tabs.csv_plot_area.thresholdMinDateChanged.connect(self.ui.startpoint_date_label.setText)
        self.chart_tabs.csv_plot_area.thresholdMaxDateChanged.connect(self.ui.endpoint_date_label.setText)

        self.ss_bridges: list[SensorSetting] = []
        for i in range(4):
            ss_bridge = SensorSetting(i)
            ss_bridge.changeStrainLineColor.connect(self.chart_tabs.main_plot_area.set_strain_graph_color)
            ss_bridge.changeStrainLineColor.connect(self.chart_tabs.ma_plot_area.set_graph_color)
            ss_bridge.changeStrainLineColor.connect(self.chart_tabs.fft_plot_area.set_graph_color)
            ss_bridge.changeTempLineColor.connect(self.chart_tabs.main_plot_area.set_temp_graph_color)
            ss_bridge.changeLineWidth.connect(self.chart_tabs.main_plot_area.set_graph_line_width)
            ss_bridge.changeLineOffset.connect(self.chart_tabs.main_plot_area.set_graph_offset)
            ss_bridge.changeLineOffset.connect(self.chart_tabs.ma_plot_area.set_graph_offset)
            self.ss_bridges.append(ss_bridge)
        self.ui.graph_settings_ch1.rootContext().setContextProperty("bridge", self.ss_bridges[0])
        self.ui.graph_settings_ch2.rootContext().setContextProperty("bridge", self.ss_bridges[1])
        self.ui.graph_settings_ch3.rootContext().setContextProperty("bridge", self.ss_bridges[2])
        self.ui.graph_settings_ch4.rootContext().setContextProperty("bridge", self.ss_bridges[3])
        self.reset_stylesheet()

    def _init_buffer_controls(self):
        validator = QRegularExpressionValidator(QRegularExpression(r"^\d{1,6}$"))

        self.buffer_label = QLabel(self.tr("Buffer"), self.ui.sampling_settings)
        self.buffer_label.setObjectName("buffer_label")
        self.buffer_label.setFont(self.ui.sampling_label.font())

        self.buffer_mode_check = QCheckBox(self.ui.sampling_settings)
        self.buffer_mode_check.setObjectName("buffer_mode_check")

        self.buffer_interval_label = QLabel(self.tr("Interval(ms)"), self.ui.sampling_settings)
        self.buffer_interval_label.setObjectName("buffer_interval_label")
        self.buffer_interval_label.setFont(self.ui.sampling_label.font())

        self.buffer_interval_edit = QLineEdit(self.ui.sampling_settings)
        self.buffer_interval_edit.setObjectName("buffer_interval_edit")
        self.buffer_interval_edit.setText("100")
        self.buffer_interval_edit.setValidator(validator)
        self.buffer_interval_edit.setFixedWidth(70)
        self.buffer_interval_edit.editingFinished.connect(self.check_buffer_interval)
        self.buffer_mode_check.toggled.connect(self.update_buffer_interval_visible)
        self.buffer_mode_check.stateChanged.connect(
            lambda state: self.update_buffer_interval_visible(state == Qt.CheckState.Checked.value)
        )

        self.buffer_transfer_mode_label = QLabel(self.tr("Transfer Mode"), self.ui.sampling_settings)
        self.buffer_transfer_mode_label.setObjectName("buffer_transfer_mode_label")
        self.buffer_transfer_mode_label.setFont(self.ui.sampling_label.font())

        self.buffer_transfer_mode_combo = QComboBox(self.ui.sampling_settings)
        self.buffer_transfer_mode_combo.setObjectName("buffer_transfer_mode_combo")
        self.buffer_transfer_mode_combo.addItem(self.tr("Strain + Temp + Status"), ModeKind.all)
        self.buffer_transfer_mode_combo.addItem(self.tr("Strain + Temp"), ModeKind.no_status)
        self.buffer_transfer_mode_combo.addItem(self.tr("Strain"), ModeKind.strain_only)
        self.buffer_transfer_mode_combo.setCurrentIndex(2)

        self.buffer_separator = QFrame(self.ui.sampling_settings)
        self.buffer_separator.setObjectName("buffer_separator")
        self.buffer_separator.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.buffer_separator.setFrameShape(QFrame.Shape.VLine)
        self.buffer_separator.setFrameShadow(QFrame.Shadow.Sunken)

        self.ui.gridLayout.setColumnMinimumWidth(2, 18)
        self.ui.gridLayout.addWidget(self.buffer_separator, 0, 2, 2, 1)
        self.ui.gridLayout.addWidget(self.buffer_label, 0, 3, 1, 1)
        self.ui.gridLayout.addWidget(self.buffer_mode_check, 1, 3, 1, 1)
        self.ui.gridLayout.addWidget(self.buffer_interval_label, 0, 4, 1, 1)
        self.ui.gridLayout.addWidget(self.buffer_interval_edit, 1, 4, 1, 1)
        self.ui.gridLayout.addWidget(self.buffer_transfer_mode_label, 0, 5, 1, 1)
        self.ui.gridLayout.addWidget(self.buffer_transfer_mode_combo, 1, 5, 1, 1)
        self.update_buffer_interval_visible(self.buffer_mode_check.isChecked())

    def set_log_header_row(self, row: int):
        self.log.set_header_row(row)

    def make_cell_widget(self, widgets: list[QWidget]) -> tuple[QWidget, QHBoxLayout]:
        cell_widget = QWidget(self)
        cell_layout = QHBoxLayout(cell_widget)
        cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell_layout.setContentsMargins(0, 0, 0, 0)
        for widget in widgets:
            cell_layout.addWidget(widget)
        return cell_widget, cell_layout

    def init_sensor_table(self):
        self._sensor_info_label_list.clear()
        table = self.ui.sensor_info  # Qt Designerで配置したQTableWidget
        for row in range(table.rowCount()):
            info_labels = []

            # --- 1列目：チェックボックス ---
            checkbox = QCheckBox()
            checkbox2 = QCheckBox()
            checkbox.stateChanged.connect(partial(self.set_chart_view, row, 0))
            checkbox2.stateChanged.connect(partial(self.set_chart_view, row, 1))
            info_labels.append((checkbox, checkbox2))
            cb_widget, cb_layout = self.make_cell_widget([checkbox, QLabel("｜"), checkbox2])
            cb_layout.setSpacing(6)
            table.setCellWidget(row, 0, cb_widget)

            # --- 2列目：QLineEdit（連番 #1, #2, ...） ---
            line_edit = QLineEdit(text=self.sensor_name[row], alignment=Qt.AlignmentFlag.AlignCenter)
            line_edit.editingFinished.connect(partial(self.set_sensor_name, row))
            info_labels.append(line_edit)
            le_widget, _ = self.make_cell_widget([line_edit])
            table.setCellWidget(row, 1, le_widget)

            # --- 3～7列目：QLabel（初期値 "-"） ---
            for col in range(2, 7):
                label = QLabel("-", alignment=Qt.AlignmentFlag.AlignCenter)
                info_labels.append(label)
                lw_widget, _ = self.make_cell_widget([label])
                table.setCellWidget(row, col, lw_widget)

            self._sensor_info_label_list.append(info_labels)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def update_sensor_table_headers(self):
        current_header = self.tr("Current Value")
        init_header = self.tr("Initial Value")
        if self.chart_unit == ChartUnitKind.strain.value:
            current_header += "(με)"
            init_header += "(με)"

        headers = {
            SensorDataTableColumnKind.temp.value: f"{self.tr('Temperature')}(℃)",
            SensorDataTableColumnKind.current.value: current_header,
            SensorDataTableColumnKind.init.value: init_header,
        }
        for col, text in headers.items():
            item = self.ui.sensor_info.horizontalHeaderItem(col)
            if item is not None:
                item.setText(text)

    def show_table_menu(self):
        menu = QMenu(self)
        # Display Mode
        menu.addSection("Display Mode")
        menu.addAction(self.strain_action)
        menu.addAction(self.lsb_action)

        # Column Settings
        menu.addSection("Column Settings")
        for action in self.column_actions:
            menu.addAction(action)

        pos = self.ui.table_setting_button.mapToGlobal(self.ui.table_setting_button.rect().bottomLeft())
        menu.exec(pos)

    def toggle_column(self, col, checked):
        self.column_show_settings[col] = checked
        self.ui.sensor_info.setColumnHidden(col, not checked)

    def update_column(self, col, checked):
        self.column_actions[col-1].setChecked(checked)
        self.toggle_column(col, checked)

    def switch_unit(self, action):
        if action == self.strain_action:
            self.chart_unit = ChartUnitKind.strain.value
        else:
            self.chart_unit = ChartUnitKind.lsb.value
        self.chart_tabs.set_unit(self.chart_unit)
        self.update_sensor_table_headers()

    def update_unit(self, mode:int):
        if mode == ChartUnitKind.strain.value:
            action = self.strain_action
            self.strain_action.setChecked(True)
            self.lsb_action.setChecked(False)
        else:
            action = self.lsb_action
            self.strain_action.setChecked(False)
            self.lsb_action.setChecked(True)
        self.switch_unit(action)

    def set_chart_view(self, ch:int, which: int, state):
        if ch < self.ui.sensor_info.rowCount():
            is_checked = state == Qt.CheckState.Checked.value
            if which == 0:  # strain
                self.strain_line_view[ch] = is_checked
            else:  # temp
                self.temp_line_view[ch] = is_checked
            if self.connection_status[ch] == SensorConnectionStatusKind.connected:
                self.set_graph_visible(ch, which, is_checked)

    def set_chart_view_only_connected(self, ch:int, connected:bool):
        if ch < self.ui.sensor_info.rowCount():
            # センサが接続されているChのみ線を描画するよう、計測開始時にコールする
            self.set_graph_visible(ch, 0, self.strain_line_view[ch] and connected)
            self.set_graph_visible(ch, 1, self.temp_line_view[ch] and connected)

    def set_graph_visible(self, ch: int, which: int, state: bool):
        if which == 0:   # Strain
            self.chart_tabs.main_plot_area.set_strain_visible(ch, state)
            self.chart_tabs.ma_plot_area.set_visible(ch, state)
            self.chart_tabs.fft_plot_area.set_visible(ch, state)
        else:   # Temp
            self.chart_tabs.main_plot_area.set_temp_visible(ch, state)

    def update_chart_view(self, ch:int, which: int, state:bool):
        if ch < self.ui.sensor_info.rowCount():
            cbs = self._sensor_info_label_list[ch][SensorDataTableColumnKind.view.value]
            cb = cbs[which]
            cb.blockSignals(True)
            cb.setChecked(state)
            cb.blockSignals(False)

            view = Qt.CheckState.Checked.value if state else Qt.CheckState.Unchecked.value
            self.set_chart_view(ch, which, view)

    def set_sensor_name(self, ch:int):
        if ch < self.ui.sensor_info.rowCount():
            self.sensor_name[ch] = self._sensor_info_label_list[ch][SensorDataTableColumnKind.name.value].text()

    def update_sensor_name(self, ch:int, name:str):
        if ch < self.ui.sensor_info.rowCount():
            self._sensor_info_label_list[ch][SensorDataTableColumnKind.name.value].setText(name)
            self.set_sensor_name(ch)

    def update_sensor_data(self, statuses:list[SensorStatus]):
        for i, status in enumerate(statuses):
            if i >= self.ui.sensor_info.rowCount():
                break
            self.connection_status[i] = status.connection_status
            if status.connection_status == SensorConnectionStatusKind.connected:
                temp_str = f"{status.temp:.2f}"
                self._sensor_info_label_list[i][SensorDataTableColumnKind.temp.value].setText(temp_str)
                if self.chart_unit == ChartUnitKind.strain.value:
                    current_str = f"{status.current_strain_value:.3f}"
                    self._sensor_info_label_list[i][SensorDataTableColumnKind.current.value].setText(current_str)
                    init_str =  f"{status.init_strain_value:.3f}"
                    self._sensor_info_label_list[i][SensorDataTableColumnKind.init.value].setText(init_str)
                    delta = status.current_strain_value - status.init_strain_value
                    delta_str = f"{delta:.3f}"
                    self._sensor_info_label_list[i][SensorDataTableColumnKind.delta.value].setText(delta_str)
                else:
                    self._sensor_info_label_list[i][SensorDataTableColumnKind.current.value].setText(str(status.current_strain))
                    self._sensor_info_label_list[i][SensorDataTableColumnKind.init.value].setText(str(status.init_strain))
                    delta = status.current_strain - status.init_strain
                    self._sensor_info_label_list[i][SensorDataTableColumnKind.delta.value].setText(str(delta))
                if status.status == ErrorStatusKind.tmp_error:
                    err = "TMPERR"
                elif status.status == ErrorStatusKind.cal_error:
                    err = "CALERR"
                elif status.status == ErrorStatusKind.mem_error:
                    err = "MEMERR"
                elif status.status == ErrorStatusKind.rom_error:
                    err = "ROMERR"
                elif status.status == ErrorStatusKind.sec_error:
                    err = "SECERR"
                else:
                    err = "NO_ERROR"
                self._sensor_info_label_list[i][SensorDataTableColumnKind.status.value].setText(err)
            else:
                self._sensor_info_label_list[i][SensorDataTableColumnKind.temp.value].setText("-")
                self._sensor_info_label_list[i][SensorDataTableColumnKind.current.value].setText("-")
                self._sensor_info_label_list[i][SensorDataTableColumnKind.init.value].setText("-")
                self._sensor_info_label_list[i][SensorDataTableColumnKind.delta.value].setText("-")
                self._sensor_info_label_list[i][SensorDataTableColumnKind.status.value].setText("-")

    def auto_balance(self):
        main_text = self.tr("This will modify the register values.\nDo you want to continue?")
        sub_text = self.tr("Note: The values may not necessarily become 0.")
        dialog = ConfirmDialog("Confirm", main_text + "\n\n" + sub_text)
        ret = dialog.exec_()
        if ret == QMessageBox.StandardButton.Ok:
            self.autoBalanceRequested.emit()

    def close_filter_settings(self):
        self.ui.filter_settings.setVisible(False)
        self.filter_settings_tab_changed()

    def close_sensor_settings(self):
        self.ui.sensor_settings.setVisible(False)

    def toggle_filter_settings(self):
        self.ui.filter_settings.setVisible(not self.ui.filter_settings.isVisible())
        self.filter_settings_tab_changed()

    def toggle_sensor_settings(self):
        self.ui.sensor_settings.setVisible(not self.ui.sensor_settings.isVisible())

    def apply_filter_settings(self):
        # 移動平均の設定の反映
        ma_enable, ma_window_size = self.fs_bridge.get_ma_settings()
        ma_prev = ma_enable and (2 <= ma_window_size <= 1000)
        self.chart_tabs.ma_plot_area.set_window_size(ma_window_size)
        self.chart_tabs.toggle_ma_tab(ma_prev)

        # FFT設定の反映
        fft_settings = self.fs_bridge.get_fft_settings()
        if fft_settings.enable and fft_settings.use_schedule_setting:
            try:
                start_date = datetime.strptime(f"{fft_settings.start_day} {fft_settings.start_time}", "%Y/%m/%d %H:%M")
                if start_date <= datetime.now():
                    self.fs_bridge.update_fft_start_date_error(True)
            except ValueError:
                start_date = datetime.now()
                self.fs_bridge.update_fft_start_date_error(False)
            fft_settings.start_datetime = start_date
        else:
            fft_settings.start_datetime = datetime.now()
            fft_settings.interval = 1
            self.fs_bridge.update_fft_start_date_error(False)

        fft_prev = fft_settings.enable and (256 <= fft_settings.resolution <= 16384)
        self.chart_tabs.fft_plot_area.set_fft_settings(fft_settings)
        self.chart_tabs.toggle_fft_tab(fft_prev)

    def filter_settings_tab_changed(self):
        visible = self.ui.filter_settings.isVisible()
        visible &= self.ui.filter_setting_tabs.currentIndex() == 1
        visible &= self.prev_csv_enable

        self.chart_tabs.toggle_csv_tab(visible)

    def csv_calc_exec(self):
        channel = self.ui.ch_select_combobox.currentIndex()
        targets = [channel] if channel < 4 else [i for i in range(4)]

        res_min, res_max, res_mean, res_std = 0.0, 0.0, 0.0, 0.0
        success_count = 0
        for ch in targets:
            result_minmax, value_minmax = self.chart_tabs.csv_plot_area.calc_min_max_mean(ch)
            if result_minmax:
                res_min += value_minmax[0]
                res_max += value_minmax[1]
                res_mean += value_minmax[2]
            result_std, value_std = self.chart_tabs.csv_plot_area.calc_std(ch)
            if result_std:
                res_std += value_std
            if result_minmax or result_std:
                success_count += 1

        self.ui.min_output.setText(f"{(res_min / success_count):.2f}" if success_count else "-")
        self.ui.max_output.setText(f"{(res_max / success_count):.2f}" if success_count else "-")
        self.ui.ave_output.setText(f"{(res_mean / success_count):.2f}" if success_count else "-")
        self.ui.sigma_output.setText(f"{(res_std / success_count):.2f}" if success_count else "-")
        self.ui.sigma2_output.setText(f"{(res_std * 2.0 / success_count):.2f}" if success_count else "-")
        self.ui.sigma3_output.setText(f"{(res_std * 3.0 / success_count):.2f}" if success_count else "-")
        self.ui.sigma33_output.setText(f"{(res_std * 3.3 / success_count):.2f}" if success_count else "-")

    def csv_path_reload(self):
        file_path = self.ui.csv_browse_edit.text()
        self.add_csv_preview(file_path, self.log.load_log(file_path))

    def open_file(self, filter_str: str, csv_callback: Callable[[str, list[SingleMeasData]], None]):
        file_path, _ = QFileDialog.getOpenFileName(self,"Open File","", filter_str)

        if file_path:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            base_name, extension = os.path.splitext(file_path)
            if extension.lower() == '.png':
                self.add_image_tab(file_path)
            elif extension.lower() == '.csv':
                csv_callback(file_path, self.log.load_log(file_path))
            QApplication.restoreOverrideCursor()

    def add_tab_callback(self, tab: QDockWidget):
        tab.setVisible(True)
        self.chart_tabs.rebalance_docks()

    def add_image_tab(self, file_path):
        dock_widget_contents = QWidget()
        dock_layout = QVBoxLayout(dock_widget_contents)
        image_viewer = PhotoViewer(dock_widget_contents)

        dock_layout.addWidget(image_viewer)
        image_viewer.set_image(file_path)
        dock_widget_contents.setLayout(dock_layout)

        tab = self.chart_tabs.add_tab(file_path, is_temp=True)
        tab.setVisible(False)
        tab.setWidget(dock_widget_contents)
        # setWidget()はGUIへの反映に時間がかかり、それまで横幅が最小で固定されるため、サイズ調整・表示を遅延する
        QTimer.singleShot(100, lambda: self.add_tab_callback(tab))
        QTimer.singleShot(150, image_viewer.fit_image)

    def add_log_tab(self, file_path, meas_data: list[SingleMeasData]):
        prev_widget = DoubleAxisWidget(x_axis=TimeAxis(orientation="bottom"), channels=8)
        if self.show_meas_data(meas_data, prev_widget) > 0:
            tab = self.chart_tabs.add_tab(file_path, is_temp=True)
            tab.setWidget(prev_widget)
            tab.setVisible(False)
            # setWidget()はGUIへの反映に時間がかかり、それまで横幅が最小で固定されるため、サイズ調整・表示を遅延する
            QTimer.singleShot(100, lambda: self.add_tab_callback(tab))
        else:
            print("No data in csv file.")

    def add_csv_preview(self, file_path, meas_data: list[SingleMeasData]):
        # 始点と終点を指定するため、データが最低でも2件必要
        csv_count = self.show_meas_data(meas_data, self.chart_tabs.csv_plot_area)
        self.prev_csv_enable = csv_count > 2
        self.ui.csv_browse_edit.setText(file_path)
        self.filter_settings_tab_changed()

        self.ui.startpoint_edit.setRange(0, csv_count - 1)
        self.ui.endpoint_edit.setRange(0, csv_count - 1)
        self.chart_tabs.csv_plot_area.set_threshold(0, csv_count - 1)

    def show_meas_data(self, meas_data: list[SingleMeasData], prev_widget: DoubleAxisWidget) -> int:
        if len(meas_data) < 1:
            return 0
        channels = max([len(m_data.sensor_data) for m_data in meas_data])
        strain_list, temp_list = [[] for _ in range(channels)], [[] for _ in range(channels)]

        times = []
        for m_data in meas_data:
            times.append(m_data.second + m_data.nanosecond / (10**9))
            for ch, data in enumerate(m_data.sensor_data):
                if data.is_valid:
                    if self.chart_tabs.unit == ChartUnitKind.strain.value:
                        strain_list[ch].append(data.strain_value)
                    else:
                        strain_list[ch].append(data.strain)
                    temp_list[ch].append(data.temp)

        for ch in range(channels):
            str_color, temp_color, width, offset = self.ss_bridges[ch].get_settings()
            prev_widget.set_strain_graph_color(ch, self.ss_bridges[ch].get_color(str_color))
            prev_widget.set_temp_graph_color(ch, self.ss_bridges[ch].get_color(temp_color))
            prev_widget.set_graph_line_width(ch, width)
            prev_widget.set_graph_offset(ch, offset)

        prev_widget.update_x_data(times)
        for ch, (s_data, t_data) in enumerate(zip(strain_list, temp_list)):
            prev_widget.update_strain_graph(ch, s_data)
            prev_widget.update_temp_graph(ch, t_data)
        prev_widget.update_x_limit(0, max([len(data) for data in strain_list]))
        prev_widget.reset_range()
        return len(meas_data)

    # 親要素のStyleSheetを引き継ぐため、子要素のStyleSheetを削除する
    def reset_stylesheet(self):
        self.setStyleSheet("")

        # 1行目
        self.ui.main_menu.setStyleSheet("")
        self.ui.meas_start_button.setStyleSheet("")
        self.ui.meas_stop_button.setStyleSheet("")
        self.ui.main_split_line_1.setStyleSheet("")
        self.ui.auto_range_button.setStyleSheet("")
        self.ui.auto_balance_button.setStyleSheet("")
        self.ui.main_split_line_2.setStyleSheet("")
        self.ui.save_log_button.setStyleSheet("")

        # 2行目
        self.ui.sub_menu.setStyleSheet("")
        self.ui.open_button.setStyleSheet("")
        self.ui.sub_line1.setStyleSheet("")
        self.ui.x_zoom_area.setStyleSheet("")
        self.ui.strain_zoom_area.setStyleSheet("")
        self.ui.temp_zoom_area.setStyleSheet("")
        self.ui.capture_button.setStyleSheet("")
        self.ui.sub_line2.setStyleSheet("")
        self.ui.sampling_label.setStyleSheet("")
        self.ui.sampling_rate_edit.setStyleSheet("")
        self.ui.sampling_rate_unit.setStyleSheet("")
        self.buffer_label.setStyleSheet("")
        self.buffer_mode_check.setStyleSheet("")
        self.buffer_interval_label.setStyleSheet("")
        self.buffer_interval_edit.setStyleSheet("")
        self.buffer_transfer_mode_label.setStyleSheet("")
        self.buffer_transfer_mode_combo.setStyleSheet("")
        self.buffer_separator.setStyleSheet("")
        self.ui.filter_config_button.setStyleSheet("")
        self.ui.sensor_config_button.setStyleSheet("")

        self.ui.chart_area.setStyleSheet("")
        self.ui.table_area.setStyleSheet("")

    def check_range(self):
        text = self.ui.sampling_rate_edit.text()
        if not text:
            return

        if self.ui.sampling_rate_unit.currentText() == "ms":
            val_min = 0.1
            val_max = 100000.0
        else:
            val_min = 0.01
            val_max = 10000.0

        try:
            val = float(text)
            new_val = min(val_max, max(val_min, val))
            self.ui.sampling_rate_edit.setText(f"{new_val}")
        except ValueError:
            self.ui.sampling_rate_edit.setText("1000")

    def check_buffer_interval(self):
        text = self.buffer_interval_edit.text()
        if not text:
            self.buffer_interval_edit.setText("100")
            return

        try:
            val = int(text)
            new_val = min(60000, max(10, val))
            self.buffer_interval_edit.setText(f"{new_val}")
        except ValueError:
            self.buffer_interval_edit.setText("100")

    def update_buffer_interval_visible(self, visible: bool):
        self.buffer_interval_label.setVisible(visible)
        self.buffer_interval_edit.setVisible(visible)
        self.buffer_transfer_mode_label.setVisible(visible)
        self.buffer_transfer_mode_combo.setVisible(visible)
        self.ui.sampling_settings.updateGeometry()
        self.ui.sub_menu.updateGeometry()
        self.ui.sampling_settings.adjustSize()

    def is_buffer_mode_enabled(self) -> bool:
        return self.buffer_mode_check.isChecked()

    def set_buffer_mode_enabled(self, enabled: bool):
        self.buffer_mode_check.setChecked(enabled)
        self.update_buffer_interval_visible(enabled)

    def validate_buffer_interval_ms(self) -> int:
        try:
            self.buffer_interval_edit.setStyleSheet("")
            interval_ms = int(self.buffer_interval_edit.text())
        except ValueError:
            self.buffer_interval_edit.setStyleSheet("border: 1px solid red;")
            return -1

        if interval_ms < 10:
            self.buffer_interval_edit.setStyleSheet("border: 1px solid red;")
            return -1
        return interval_ms

    def get_buffer_transfer_mode(self) -> ModeKind:
        mode = self.buffer_transfer_mode_combo.currentData()
        return mode if isinstance(mode, ModeKind) else ModeKind.strain_only

    def set_buffer_transfer_mode_index(self, index: int):
        if 0 <= index < self.buffer_transfer_mode_combo.count():
            self.buffer_transfer_mode_combo.setCurrentIndex(index)

    def get_buffer_transfer_mode_index(self) -> int:
        return self.buffer_transfer_mode_combo.currentIndex()

    def validate_sample_rate(self) -> float:
        rate_txt = self.ui.sampling_rate_edit.text()
        try:
            self.ui.sampling_rate_edit.setStyleSheet("")
            return float(rate_txt)
        except ValueError:
            self.ui.sampling_rate_edit.setStyleSheet("border: 1px solid red;")
            return -1

    def get_rate_unit(self) -> str:
        return self.ui.sampling_rate_unit.currentText()

    def get_action_names(self) -> list[str]:
        return [self.tr("Sensor Name"), self.tr("Temperature"), self.tr("Current Value"),
                self.tr("Initial Value"), self.tr("Delta"), self.tr("Status")]

    def update_buffer_language(self, is_japanese: bool):
        if is_japanese:
            self.buffer_label.setText("バッファ")
            self.buffer_interval_label.setText("取得間隔(ms)")
            self.buffer_transfer_mode_label.setText("転送モード")
            mode_texts = ["ひずみ + 温度 + ステータス", "ひずみ + 温度", "ひずみ"]
        else:
            self.buffer_label.setText("Buffer")
            self.buffer_interval_label.setText("Interval(ms)")
            self.buffer_transfer_mode_label.setText("Transfer Mode")
            mode_texts = ["Strain + Temp + Status", "Strain + Temp", "Strain"]

        current_index = self.buffer_transfer_mode_combo.currentIndex()
        for index, text in enumerate(mode_texts):
            self.buffer_transfer_mode_combo.setItemText(index, text)
        self.buffer_transfer_mode_combo.setCurrentIndex(current_index)

    def update_language(self):
        self.update_buffer_language(False)
        self.buffer_label.setText(self.tr("Buffer"))
        self.buffer_interval_label.setText(self.tr("Interval(ms)"))
        self.buffer_transfer_mode_label.setText(self.tr("Transfer Mode"))
        current_index = self.buffer_transfer_mode_combo.currentIndex()
        self.buffer_transfer_mode_combo.setItemText(0, self.tr("Strain + Temp + Status"))
        self.buffer_transfer_mode_combo.setItemText(1, self.tr("Strain + Temp"))
        self.buffer_transfer_mode_combo.setItemText(2, self.tr("Strain"))
        self.buffer_transfer_mode_combo.setCurrentIndex(current_index)
        self.strain_action.setText(self.tr("Strain Value(με)"))
        self.lsb_action.setText(self.tr("LSB"))
        for i, name in enumerate(self.get_action_names()):
            self.column_actions[i].setText(name)
        self.update_sensor_table_headers()



    def apply_theme(self, theme: int):
        if theme == 0:      # Normal
            icon_color = "#2D3282"
        elif theme == 1:    # Light
            icon_color = "#21272A"
        else:                     # Dark
            icon_color = "#FFFFFF"
        sz20 = QSize(20, 20)

        self.ui.open_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/add-folder.png", icon_color, sz20))
        self.ui.capture_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/camera.png", icon_color, sz20))
        self.ui.filter_config_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/filter.png", icon_color, sz20))
        self.ui.sensor_config_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/options-outline.png", icon_color, sz20))
        self.ui.table_setting_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/table-options.png", icon_color, sz20))
        self.ui.x_zoom_in_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/zoom-in.png", icon_color, sz20))
        self.ui.x_zoom_out_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/zoom-out.png", icon_color, sz20))
        self.ui.save_log_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/save-floppy-disk.png", icon_color, sz20))
        self.ui.auto_range_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/ruler-measure.png", icon_color, sz20))
        self.ui.strain_zoom_in_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/zoom-in.png", icon_color, sz20))
        self.ui.strain_zoom_out_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/zoom-out.png", icon_color, sz20))
        self.ui.temp_zoom_in_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/zoom-in.png", icon_color, sz20))
        self.ui.temp_zoom_out_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/zoom-out.png", icon_color, sz20))
        self.ui.meas_start_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/play-outline.png", icon_color, sz20))
        self.ui.meas_stop_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/pause.png", icon_color, sz20))
        self.ui.filter_settings_close_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/close-sharp.png", icon_color, sz20))
        self.ui.sensor_settings_close_button.setIcon(tinted_qicon(":/ChartPages/Images/Pages/ChartPage/close-sharp.png", icon_color, sz20))


