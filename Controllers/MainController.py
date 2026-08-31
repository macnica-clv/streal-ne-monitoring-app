import os, sys, threading
import platform
import shutil
import subprocess
import webbrowser

# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

# import PySide6
from PySide6 import QtCore
from PySide6.QtCore import QTranslator, QUrl
from PySide6.QtGui import QFontDatabase, QDesktopServices
from PySide6.QtWidgets import QApplication

from Controllers.RegisterControllerSR300 import RegisterControllerSR300
from Controllers.RegisterController import RegisterController
from Models.Hizmil_Driver_SR300_LAN import HizmilDriverLANSR300
from Models.Hizmil_Driver_SR300_USB import HizmilDriverUSBSR300
# if getattr(sys, 'frozen', False):
#     basedir = os.path.dirname(sys.executable)
#     pyside_dir = os.path.dirname(PySide6.__file__)
#     plugin_path = os.path.join(pyside_dir, 'Qt', 'plugins')
#     os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
#     os.environ['QT_PLUGIN_PATH'] = plugin_path

from Utils.ResourceLoader import rel_to_abs
from Controllers import HomeController, ChartController, SettingController
from Controllers.CuiController import CuiController
from Models.Config import Config, ConnectionMethodKind
from Models.Board import BoardKind
from Models.Hizmil_Driver import ResultKind
from Models.Register_Item_SR500 import RegisterItemSR500
from Models.Register_Item_SR300 import RegisterItemSR300
from Models.Hizmil_Driver_USB import HizmilDriverUSB, ConnectionStatus
from Models.Hizmil_Driver_LAN import HizmilDriverLAN
from Views.MainView import MainWindow


class MainController:
    def __init__(self, enable_console: bool = False):
        self.app = QApplication(sys.argv)
        if sys.platform == "darwin":
            self.app.setQuitOnLastWindowClosed(True)
            self.app.activeWindow()
            self.app.setProperty("darkMode", False)
        self.translator = QTranslator()

        self.load_font(self.app)

        self.board_type = None
        self.driver = HizmilDriverUSB()
        self.config = Config()

        self.window = MainWindow()
        self.window.ui.home_button.clicked.connect(self.show_home_page)
        self.window.ui.chart_button.clicked.connect(self.show_chart_page)
        self.window.ui.manual_button.clicked.connect(self.show_manual_page)
        self.window.ui.setting_button.clicked.connect(self.show_setting_page)
        self.window.closing_application.connect(self.handle_app_closing)

        self.home_controller = HomeController.HomeController(self.config, parent=self.window)
        self.chart_controller = ChartController.ChartController(self.config, parent=self.window)
        self.register_controller = None
        self.chart_controller.measurementStarted.connect(self.start_measure)
        self.chart_controller.measurementStopped.connect(self.stop_measure)
        self.window.add_page(self.home_controller.home_page)
        self.window.add_page(self.chart_controller.chart_page)

        #QML色変え　QMLに渡す
        self.chart_controller.chart_page.app_bridge = self.window.status_bridge
        chartpage = self.chart_controller.chart_page
        chartpage.ui.ma_settings.rootContext().setContextProperty("appBridge", chartpage.app_bridge)
        chartpage.ui.fft_settings.rootContext().setContextProperty("appBridge", chartpage.app_bridge)
        chartpage.ui.graph_settings_ch1.rootContext().setContextProperty("appBridge", chartpage.app_bridge)
        chartpage.ui.graph_settings_ch2.rootContext().setContextProperty("appBridge", chartpage.app_bridge)
        chartpage.ui.graph_settings_ch3.rootContext().setContextProperty("appBridge", chartpage.app_bridge)
        chartpage.ui.graph_settings_ch4.rootContext().setContextProperty("appBridge", chartpage.app_bridge)
        self.home_controller.home_page.app_bridge2 = self.window.status_bridge
        self.home_controller.home_page.app_bridge3 = self.window.status_bridge
        homepage = self.home_controller.home_page
        homepage.ui.connect_settings.rootContext().setContextProperty("appBridge2", homepage.app_bridge2)
        homepage.ui.connect_status.rootContext().setContextProperty("appBridge3", homepage.app_bridge3)

        self.setting_controller = SettingController.SettingController(self.config, self.driver, parent=self.window)
        self.setting_controller.themeChanged.connect(self.load_theme)
        self.setting_controller.scChanged.connect(self.update_shortcuts)
        self.setting_controller.langChanged.connect(self.update_language)

        self.setting_controller.setting_page.app_bridge = self.window.status_bridge
        settingpage = self.setting_controller.setting_page
        settingpage.log_setting.ui.autosave_area.rootContext().setContextProperty("appBridge", settingpage.app_bridge)

        self.cui_controller = CuiController(self, enable_console=enable_console)

        self._com = [""] * 2
        self.home_controller.request_signal().connect(self.init_driver)
        self.home_controller.disconnect_signal().connect(self.disconnect_driver)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(500)

        self.show_home_page()
        self.load_theme()
        self.update_shortcuts()
        self.update_language()
        self.cui_controller.start()
        self.window.show()
        self.app.exec()

    def load_font(self,app):
        qrc_path = ":/fonts/fonts/Roboto-VariableFont_wdth,wght.ttf"

        font_id = QFontDatabase.addApplicationFont(qrc_path)
        if font_id == -1:
            print(f"Error: Failed to load font from QRC path: {qrc_path}")
            return

        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if len(font_families) == 0:
            print(f"Error: Failed to load font families from id: {font_id}")
            return

        roboto_family_name = font_families[0]
        if roboto_family_name:
            style_sheet = f"""
                    QWidget {{
                        font-family: '{roboto_family_name}', sans-serif; 
                    }}
                """
            self.app.setStyleSheet(style_sheet)

    def load_theme(self):
        config_theme = self.config.load_config_theme()
        theme = config_theme.window_theme
        try:
            if theme == 1:
                filename = "./qss/Light.qss"
            elif theme == 2:
                filename = "./qss/Dark.qss"
            else:
                filename = "./qss/Normal.qss"
            with open(rel_to_abs(filename), "r") as file:
                self.app.setStyleSheet("".join(file.readlines()))
            # MainWindow（Qt Widgets）のアイコンを tint 更新
            self.window.apply_theme_icons(theme)
            self.home_controller.home_page.apply_theme(theme)  # Home
            self.chart_controller.chart_page.apply_theme(theme)  # Char
            self.update_qml_theme(theme)
        except FileNotFoundError:
            print("No QSS file found")

    def update_shortcuts(self):
        self.chart_controller.set_shortcuts()

    def update_language(self):
        config_lang = self.config.load_config_language()
        language = config_lang.language
        try:
            self.app.removeTranslator(self.translator)
            if language == 1:
                filename = "./Lang/lang_jp.qm"
                self.translator.load(rel_to_abs(filename))
                self.app.installTranslator(self.translator)

            self.home_controller.update_language()
            self.chart_controller.update_language()
            self.setting_controller.update_language()
        except FileNotFoundError:
            print("No language file found")

    def close_all_page(self):
        self.home_controller.hide()
        self.chart_controller.hide()
        self.setting_controller.hide()

    def show_home_page(self):
        self.close_all_page()
        self.home_controller.show()

    def show_chart_page(self):
        self.close_all_page()
        self.chart_controller.show()

    def show_manual_page(self):
        relative_path = rel_to_abs("Manuals/manual.pdf")

        if platform.system() == "Linux":
            # 絶対パスを確実に取得
            if hasattr(sys, "_MEIPASS"):
                manual_path = os.path.join(sys._MEIPASS, relative_path)
            else:
                manual_path = os.path.abspath(relative_path)

            # 環境変数のクリーニング
            env = os.environ.copy()
            # LD_LIBRARY_PATH　が悪さをしているので、これを除去した状態で実行する
            env.pop("LD_LIBRARY_PATH", None)

            try:
                # shell=Trueを使い、OSのシェル経由で　xdg-open を叩く
                cmd = f'xdg-open "{manual_path}"'
                # start_new_sessioでアプリと切り離す
                subprocess.Popen(cmd,
                                 shell=True,
                                 env=env,
                                 start_new_session=True,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"Open error:{e}")
        else:
            manual_path = rel_to_abs(relative_path)

        if os.path.exists(manual_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(manual_path))
        else:
            print("マニュアルが見つかりません:", manual_path)

    def show_setting_page(self):
        # TBD：SR300対応時にクラスを変更する
        # レジスタ部分の文字数 ＝ 名前＋ヘッダ（3文字、センサ数）＋設定値（センサ数）＋セパレータ（項目数＊センサ数）＋改行文字（項目数＋末尾の2行）
        if self.board_type == "SR300":
            reg = RegisterItemSR300(self.driver, 0)
        elif self.board_type == "SR500":
            reg = RegisterItemSR500(self.driver, 0)
        else:
            reg = RegisterItemSR500(self.driver, 0)
        name_lengths = [len(name) for name in reg.get_item_names()]
        item_lengths = reg.get_all_value_max_len()
        reg_header_len = sum(name_lengths) + (3 + sum(item_lengths)) * self.driver.sensor_ch_max + len(item_lengths) * (self.driver.sensor_ch_max + 1) + 2

        # 測定値のヘッダ
        meas_header_len = len("Time," + ",".join([f"Ch{i} Status,Ch{i} Temp(℃), Ch{i} Strain, Ch{i} Strain Value(με)" for i in range(self.driver.sensor_ch_max)]) + "\n")

        # 測定ログ1行当たりの文字数
        # status: 4文字、temp: 6文字、strain: 6文字、strain_value: 9文字、区切り文字: 4文字、末尾に2文字
        meas_log_len = 29 + (4 + 6 + 6 + 9 + 4) * self.driver.sensor_ch_max + 2
        self.setting_controller.set_file_size(reg_header_len + meas_header_len, meas_log_len)

        rate = self.chart_controller.calc_sampling_rate()
        rate = 1000 if rate <= 0 else rate
        self.setting_controller.set_sampling_rate(rate)
        self.setting_controller.show()

    def init_driver(self, method: int, targets: list[str]):
        if self.driver.is_connected():
            print("Already connected.")
            return ConnectionStatus.other_error

        # まず候補を並べる（USB時だけ二段階にする例）
        if method == 0:
            candidates = [
                HizmilDriverUSB(),  # SR500想定（既存）
                HizmilDriverUSBSR300(),    # SR300専用Driverがあるなら追加
            ]
        elif method == 1:
            # LANは基本1種類（必要なら同様に候補化）
            candidates = [HizmilDriverLAN(targets, "1024"),
                          HizmilDriverLANSR300(targets, "1024")]
        else:
            print("Invalid method.")
            return ConnectionStatus.other_error

        last_result = None

        for cand in candidates:
            # 切替時にCUI側参照を更新
            self.driver = cand
            self.cui_controller.refresh_driver()

            result = self.driver.connect(targets)
            last_result = result
            print(
                f"[{threading.current_thread().name}] TryConnect driver={type(cand).__name__} targets={targets} -> {result}",
                flush=True)

            if result != ConnectionStatus.success:
                continue

            # ★Connect成功後に種別取得で確定
            self._com = targets
            self.driver.init_status_all()
            board_type = self._hizmil_get_sensor_type_all()

            # 混在NG
            if board_type == "MIX":
                self.home_controller.update_log(ConnectionStatus.mixed_sensor)
                self.driver.disconnect(self._com)
                return ConnectionStatus.mixed_sensor

            # ここで期待する種別かを判定（例：candがSR500系ならSR500であること）
            # ※ candがSR300専用Driverなら "SR300" を期待
            expected = None
            if type(cand).__name__ in ("HizmilDriverUSB","HizmilDriverLAN"):
                expected = "SR500"
            elif type(cand).__name__ in ("HizmilDriverUSBSR300","HizmilDriverLANSR300"):
                expected = "SR300"

            if expected is not None and board_type != expected:
                print(f"[WARN] Sensor type mismatch. expected={expected}, actual={board_type}. retry another driver.",
                      flush=True)
                self.home_controller.update_log(ConnectionStatus.sensor_not_detected)
                self.driver.disconnect(self._com)
                continue

            # ★ここまで通れば正式採用
            self.board_type = board_type
            self.home_controller.update_log(ConnectionStatus.success)

            version = self.driver.get_version_value()
            self.home_controller.update_board_status(version, self.board_type, self._com)

            if self.board_type == "SR300":
                self.register_controller = RegisterControllerSR300(parent=self.window)
            elif self.board_type == "SR500":
                self.register_controller = RegisterController(parent=self.window)
            else:
                print("Unsupported board type")
                self.driver.disconnect(self._com)
                return ConnectionStatus.other_error

            self.register_controller.set_driver(self.driver)
            self.home_controller.set_driver(self.driver)
            self.chart_controller.set_driver(self.driver)
            self.setting_controller.set_driver(self.driver)
            self.chart_controller.enable_buttons()
            return ConnectionStatus.success

        # 全候補失敗
        self.home_controller.update_log(last_result)
        return last_result if last_result is not None else ConnectionStatus.other_error

    def disconnect_driver(self):
        was_connected = self.driver.is_connected()

        if self.driver.is_measuring:
            self.chart_controller.measure_stop()
        elif was_connected:
            self.chart_controller.chart_page.ui.meas_stop_button.setEnabled(False)

        if was_connected:
            self.driver.disconnect(self._com)

        self.board_type = None
        self._com = [""] * 2
        self.chart_controller.disable_buttons()
        self.window.ui.setting_button.setEnabled(True)

        empty_statuses = [0] * self.driver.ch_max
        empty_ids = ["-"] * self.driver.ch_max
        self.window.status_bridge.update_sensor_status(empty_statuses)
        self.home_controller.update_board_status([], "-----", [])
        self.home_controller.update_sensor_status(empty_statuses)
        self.home_controller.update_sensor_ids(empty_ids)

        if was_connected:
            self.home_controller.notify_disconnected()
        return was_connected


    def _hizmil_get_sensor_type_all(self) -> str:
        """
        Connect直後にセンサー種別を取得してdriverへ保持し、
        Home画面に表示するボード種別文字列を返す。
        """
        found_types = set()

        for board in BoardKind:
            # 接続中ボードのみ対象
            if not self.driver.get_board_connection_status(board):
                continue

            ret, ch1_type, ch2_type = self.driver.get_sensor_type(board)

            if ret != ResultKind.ok:
                print(f"[WARN] get_sensor_type failed: board={board}, ret={ret}", flush=True)
                return "NO_SENSOR"

            # driverにキャッシュ（driver側で更新しているなら不要だが、確実にするため保持）
            self.driver.sensor_type_ch1[board.value] = ch1_type
            self.driver.sensor_type_ch2[board.value] = ch2_type

            # 有効値だけ集計
            for t in (ch1_type, ch2_type):
                if t != self.driver.SENSOR_TYPE_INVALID:
                    found_types.add(t)

        # 表示用の種別文字列
        if not found_types:
            return "UNKNOWN"
        if found_types == {self.driver.SENSOR_TYPE_SR300}:
            return "SR300"
        if found_types == {self.driver.SENSOR_TYPE_SR500}:
            return "SR500"
        return "MIX"  # SR300/SR500混在

    def update_status(self):
        if self.driver.is_connected():
            sensor_status = self.driver.get_sensor_status_all()
            self.chart_controller.chart_page.update_sensor_data(sensor_status)

            statuses = [status.connection_status.value for status in sensor_status]
            self.window.status_bridge.update_sensor_status(statuses)
            self.home_controller.update_sensor_status(statuses)
            self.home_controller.update_sensor_ids(self.driver.get_sensor_ids())

    def update_qml_theme(self, color: int):
        self.window.status_bridge.update_theme(color)

    def handle_app_closing(self):
        self.cui_controller.stop()
        if self.driver.is_measuring:
            self.driver.stop_measure()
        self.driver.disconnect(self._com)
        self.home_controller.handle_app_closing()
        self.chart_controller.handle_app_closing()

    def start_measure(self):
        self.window.ui.setting_button.setEnabled(False)

    def stop_measure(self):
        self.window.ui.setting_button.setEnabled(True)

