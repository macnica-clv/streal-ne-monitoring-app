import datetime, re
import sys
from typing import Optional

import PySide6.QtCore as QtCore
from PySide6.QtCore import Signal, Property, Slot, QObject
from PySide6.QtGui import QKeyEvent, QPixmap
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog, QLineEdit, QPushButton

from Views.MainView import tinted_qicon, DummyAppBridge
from Views.UI import Color_Setting, Shortcut_Setting, Language_Setting, Log_Setting, Setting_Page, network_setting, version


# 配色テーマ設定タブ
class ThemeSettingInfo:
    def __init__(self, theme_index: int):
        self.theme_index = theme_index

    def set_theme(self, index: int) -> bool:
        self.theme_index = index
        return True

class ThemeSetting(QWidget):
    def __init__(self, info: ThemeSettingInfo, parent=None):
        super(ThemeSetting, self).__init__(parent)
        self.ui = Color_Setting.Ui_color_setting_tab()
        self.ui.setupUi(self)

        self.info: ThemeSettingInfo = info
        self.ui.theme_select.setCurrentIndex(info.theme_index)
        self.ui.theme_select.currentIndexChanged.connect(
            self.update_theme_preview
        )

    def validate(self) -> bool:
        ret = True
        ret &= self.info.set_theme(self.ui.theme_select.currentIndex())

        return ret

    def cancel(self):
        self.ui.theme_select.setCurrentIndex(self.info.theme_index)

    def update_theme_preview(self, theme: int):
        """
        theme:
          0 = Normal
          1 = Light
          2 = Dark
        """
        if theme == 1:
            path = ":/ChartPages/Images/Pages/ChartPage/white_sample.jpeg"
        elif theme == 2:
            path = ":/ChartPages/Images/Pages/ChartPage/dark_sample.jpeg"
        else:
            path = ":/ChartPages/Images/Pages/ChartPage/normal_sample.jpeg"

        pixmap = QPixmap(path)
        self.ui.preview_image.setPixmap(
            pixmap.scaled(
                self.ui.preview_image.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )


# ショートカット設定タブ
def check_duplicate(targets) -> list[bool]:
    duplicates = []
    for target in targets:
        if len(target) > 0:
            duplicates.append(True if len([i for i, x in enumerate(targets) if x == target]) > 1 else False)
        else:
            duplicates.append(False)
    return duplicates

class ShortcutArea(QObject):
    def __init__(self, value: str, edit: QLineEdit, clear_button: QPushButton, restore_button: QPushButton, parent=None):
        super().__init__(parent=parent)
        self.value = value
        self.edit = edit
        self.clear_button = clear_button
        self.restore_button = restore_button

        self.is_control = False
        self.is_shift = False
        self.is_alt = False
        self.end_key = ""
        self.is_error = False
        self.split_value(value)

        self.edit.setText(value)
        self.edit.keyPressEvent = self.key_press_event
        self.clear_button.clicked.connect(self.clear)
        self.restore_button.clicked.connect(self.restore)

    def key_press_event(self, event: QKeyEvent):
        # 長押し対策
        if event.isAutoRepeat():
            return
        pressed = event.key()
        if pressed == QtCore.Qt.Key.Key_Control:
            self.is_control = not self.is_control
        elif pressed == QtCore.Qt.Key.Key_Shift:
            self.is_shift = not self.is_shift
        elif pressed == QtCore.Qt.Key.Key_Alt:
            self.is_alt = not self.is_alt
        elif QtCore.Qt.Key.Key_0 <= pressed <= QtCore.Qt.Key.Key_9 or QtCore.Qt.Key.Key_A <= pressed <= QtCore.Qt.Key.Key_Z:
            self.end_key = chr(pressed)
        else:
            print(f"Invalid key {pressed}")

        shortcuts = []
        is_mac = sys.platform == "darwin"
        if self.is_control:
            shortcuts.append("Cmd") if is_mac else shortcuts.append("Ctrl")
        if self.is_shift:
            shortcuts.append("Shift")
        if self.is_alt:
            shortcuts.append("Opt") if is_mac else shortcuts.append("Alt")
        shortcuts.append(self.end_key)
        self.edit.setText("+".join(shortcuts))

    def split_value(self, value: str):
        self.is_control = value.find("Ctrl") >= 0
        self.is_shift = value.find("Shift") >= 0
        self.is_alt = value.find("Alt") >= 0
        self.end_key = value[-1] if value else ""

    def validate(self):
        if len(self.edit.text()) == 0 or re.match(".*[A-Z|0-9]$", self.edit.text()):
            self.is_error = False
        else:
            self.is_error = True
        return not self.is_error

    def confirm_value(self):
        self.value = self.edit.text()
        return self.value

    def set_error(self, is_err: bool):
        self.edit.setStyleSheet(f"border: 1px solid {'red' if is_err or self.is_error else 'black'};")

    def clear(self):
        self.edit.clear()
        self.split_value("")

    def restore(self):
        self.edit.setText(self.value)
        self.split_value(self.value)

class ShortcutSettingInfo:
    def __init__(self, shortcuts: list[str]):
        self.shortcuts: list[str] = shortcuts

    def set_shortcut(self, index: int, key: str) -> bool:
        if index < len(self.shortcuts):
            self.shortcuts[index] = key
            return True
        else:
            return False

class ShortcutSetting(QWidget):
    def __init__(self, info: ShortcutSettingInfo, parent=None):
        super(ShortcutSetting, self).__init__(parent)
        self.ui = Shortcut_Setting.Ui_sc_setting_tab()
        self.ui.setupUi(self)

        # 設定値をUIに反映する
        self.info = info
        self.edit_areas: list[ShortcutArea] = []
        self.edit_areas.append(ShortcutArea(info.shortcuts[0], self.ui.start_edit, self.ui.start_config_clear, self.ui.start_config_restore, parent=self))
        self.edit_areas.append(ShortcutArea(info.shortcuts[1], self.ui.stop_edit, self.ui.stop_config_clear, self.ui.stop_config_restore, parent=self))
        self.edit_areas.append(ShortcutArea(info.shortcuts[2], self.ui.auto_range_edit, self.ui.auto_range_config_clear, self.ui.auto_range_config_restore, parent=self))
        self.edit_areas.append(ShortcutArea(info.shortcuts[3], self.ui.save_edit, self.ui.save_config_clear, self.ui.save_config_restore, parent=self))
        self.edit_areas.append(ShortcutArea(info.shortcuts[4], self.ui.capture_edit, self.ui.capture_config_clear, self.ui.capture_config_restore, parent=self))

    def validate(self) -> bool:
        # 入力値チェック
        ret = True
        for i, area in enumerate(self.edit_areas):
            ret &= area.validate()

        # 重複チェック
        duplicates = check_duplicate([area.edit.text() for area in self.edit_areas])
        for i, dp in enumerate(duplicates):
            self.edit_areas[i].set_error(dp)

        # エラーがなければ変更を確定する
        ret &= not any(duplicates)
        if ret:
            for i, area in enumerate(self.edit_areas):
                self.info.set_shortcut(i, area.confirm_value())
        return ret

    def cancel(self):
        for area in self.edit_areas:
            area.restore()


# 言語設定タブ
class LanguageSettingInfo:
    def __init__(self, lang_index: int):
        self.lang_index: int = lang_index

    def set_language(self, index: int) -> bool:
        self.lang_index = index
        return True

class LanguageSetting(QWidget):
    def __init__(self, info: LanguageSettingInfo, parent=None):
        super(LanguageSetting, self).__init__(parent)
        self.ui = Language_Setting.Ui_language_setting()
        self.ui.setupUi(self)

        # 設定値をUIに反映する
        self.info: LanguageSettingInfo = info
        self.ui.language_select.setCurrentIndex(info.lang_index)

    def validate(self) -> bool:
        ret = True
        ret &= self.info.set_language(self.ui.language_select.currentIndex())

        return ret

    def cancel(self):
        self.ui.language_select.setCurrentIndex(self.info.lang_index)


# ログ保存設定タブ
class LogSettingInfo:
    def __init__(self, auto_save, save_ma, save_fft, save_std, log_filename_prefix, log_save_dst, sample_num, cap_save_dst):
        self.auto_save: bool = auto_save
        self.save_ma: bool = save_ma
        self.save_fft: bool = save_fft
        self.save_std: bool = save_std
        self.log_filename_prefix: str = log_filename_prefix
        self.log_save_dst: str = log_save_dst
        self.sample_num: int = sample_num
        self.cap_save_dst: str = cap_save_dst

class LogSettingBridge(QObject):
    autoSaveChanged = Signal()
    saveKindsChanged = Signal()

    def __init__(self, parent=None):
        super(LogSettingBridge, self).__init__(parent)
        self._auto_save = False
        self._save_ma = False
        self._save_fft = False
        self._save_std = False

    @Property(bool, notify=autoSaveChanged)
    def auto_save(self):
        return self._auto_save

    @Property(bool, notify=saveKindsChanged)
    def save_std(self):
        return self._save_std

    @Property(bool, notify=saveKindsChanged)
    def save_fft(self):
        return self._save_fft

    @Property(bool, notify=saveKindsChanged)
    def save_ma(self):
        return self._save_ma

    @Slot(bool)
    def set_auto_save(self, auto_save):
        self._auto_save = auto_save

    @Slot(bool)
    def set_save_std(self, save_std):
        self._save_std = save_std

    @Slot(bool)
    def set_save_fft(self, save_fft):
        self._save_fft = save_fft

    @Slot(bool)
    def set_save_ma(self, save_ma):
        self._save_ma = save_ma

    def update_auto_save(self, auto_save):
        self._auto_save = auto_save
        self.autoSaveChanged.emit()

    def update_save_kinds(self, save_std, save_fft, save_ma):
        self._save_std = save_std
        self._save_fft = save_fft
        self._save_ma = save_ma
        self.saveKindsChanged.emit()

    def get_auto_save(self):
        return self._auto_save

    def get_save_std(self):
        return self._save_std

    def get_save_fft(self):
        return self._save_fft

    def get_save_ma(self):
        return self._save_ma

class LogSetting(QWidget):
    def __init__(self, info: LogSettingInfo, parent=None):
        super(LogSetting, self).__init__(parent)
        self.app_bridge = DummyAppBridge(initial_theme=0)
        self.ui = Log_Setting.Ui_log_setting_tab()
        self.ui.setupUi(self)
        self.reset_stylesheet()
        self.sample_rate = 1000
        self.header_size = 0
        self.row_size = 0

        self.info: LogSettingInfo = info
        self.ui.prefix_edit.setText(info.log_filename_prefix)
        self.ui.log_location_edit.setText(info.log_save_dst)
        self.ui.sample_count_edit.setValue(info.sample_num)
        self.ui.capture_location_edit.setText(info.cap_save_dst)

        self.ls_bridge = LogSettingBridge()
        self.ui.autosave_area.rootContext().setContextProperty("bridge", self.ls_bridge)
        self.ls_bridge.update_auto_save(info.auto_save)
        self.ls_bridge.update_save_kinds(info.save_std, info.save_fft, info.save_ma)

        self.ui.log_location_select_button.clicked.connect(lambda: self.browse_dir(self.ui.log_location_edit))
        self.ui.capture_location_select_button.clicked.connect(lambda: self.browse_dir(self.ui.capture_location_edit))
        self.ui.sample_count_edit.valueChanged.connect(self.calc_time_file)
        self.ui.sample_count_edit.valueChanged.connect(self.calc_file_size)

        self.ui.autosave_area.rootContext().setContextProperty("appBridge", self.app_bridge)

    def browse_dir(self, tb: QLineEdit):
        file_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            "")

        if file_path:
            tb.setText(file_path)

    def calc_time_file(self):
        td = datetime.timedelta(seconds=self.ui.sample_count_edit.value() / self.sample_rate)
        m, s = divmod(td.seconds, 60)
        h, m = divmod(m, 60)
        self.ui.sample_time_label.setText(f"{td.days}d {h:02d}h {m:02d}m {s:02d}.{td.microseconds:06d}s")

    def calc_file_size(self):
        size = self.header_size + self.row_size * self.ui.sample_count_edit.value()
        self.ui.sample_size_label.setText(f"{(size / 1024 / 1024):.3f} MB/File")

    def validate(self) -> bool:
        ret = True
        self.info.auto_save = self.ls_bridge.get_auto_save()
        self.info.save_std = self.ls_bridge.get_save_std()
        self.info.save_fft = self.ls_bridge.get_save_fft()
        self.info.save_ma = self.ls_bridge.get_save_ma()
        self.info.log_filename_prefix = self.ui.prefix_edit.text()
        self.info.log_save_dst = self.ui.log_location_edit.text()
        self.info.sample_num = self.ui.sample_count_edit.value()
        self.info.cap_save_dst = self.ui.capture_location_edit.text()

        return ret

    def cancel(self):
        self.ls_bridge.update_auto_save(self.info.auto_save)
        self.ui.prefix_edit.setText(self.info.log_filename_prefix)
        self.ui.log_location_edit.setText(self.info.log_save_dst)
        self.ui.sample_count_edit.setValue(self.info.sample_num)
        self.ui.capture_location_edit.setText(self.info.cap_save_dst)

    def reset_stylesheet(self):
        self.setStyleSheet("")

class NetworkSettingInfo:
    def __init__(self, device1_ip="", device2_ip=""):
        self.device1_ip = device1_ip
        self.device2_ip = device2_ip

class NetworkSetting(QWidget):
    def __init__(self, info: NetworkSettingInfo, parent=None):
        super(NetworkSetting, self).__init__(parent)

        self.ui = network_setting.Ui_net_setting_tab()
        self.ui.setupUi(self)

        self.info = info

        # UIに反映
        self.ui.device1_ip.setText(info.device1_ip)
        self.ui.device2_ip.setText(info.device2_ip)

    def validate(self):
        self.info.device1_ip = self.ui.device1_ip.text()
        self.info.device2_ip = self.ui.device2_ip.text()
        return True

    def cancel(self):
        self.ui.device1_ip.setText(self.info.device1_ip)
        self.ui.device2_ip.setText(self.info.device2_ip)

class VersionSettingInfo:
    def __init__(self, version_num=""):
        self.version = version_num

class VersionSetting(QWidget):
    def __init__(self, info: VersionSettingInfo, parent=None):
        super(VersionSetting, self).__init__(parent)

        self.ui = version.Ui_version_tab()
        self.ui.setupUi(self)

# 設定画面の本体
class SettingPageInfo:
    def __init__(self, theme_info, sc_info, lang_info, log_info, net_info, version_info):
        self.theme_info = theme_info
        self.sc_info = sc_info
        self.lang_info = lang_info
        self.log_info = log_info
        self.net_info = net_info
        self.version_info = version_info

class SettingPage(QMainWindow):
    themeSaveRequested = Signal(ThemeSettingInfo)
    shortcutSaveRequested = Signal(ShortcutSettingInfo)
    languageSaveRequested = Signal(LanguageSettingInfo)
    logSaveRequested = Signal(LogSettingInfo)
    networkSaveRequested = Signal(NetworkSettingInfo)

    def __init__(self, page_info: SettingPageInfo, parent=None):
        super().__init__(parent=parent)
        self.ui = Setting_Page.Ui_setting_page()
        self.ui.setupUi(self)
        self.reset_stylesheet()

        self.color_setting = ThemeSetting(page_info.theme_info, parent=self)
        self.ui.body_layout.addWidget(self.color_setting)
        self.shortcut_setting = ShortcutSetting(page_info.sc_info, parent=self)
        self.ui.body_layout.addWidget(self.shortcut_setting)
        self.language_setting = LanguageSetting(page_info.lang_info, parent=self)
        self.ui.body_layout.addWidget(self.language_setting)
        self.log_setting = LogSetting(page_info.log_info, parent=self)
        self.ui.body_layout.addWidget(self.log_setting)
        self.network_setting = NetworkSetting(page_info.net_info, parent=self)
        self.ui.body_layout.addWidget(self.network_setting)
        self.version_setting = VersionSetting(page_info.version_info, parent=self)
        self.ui.body_layout.addWidget(self.version_setting)

        for btn in (
                self.ui.color_button,
                self.ui.sc_button,
                self.ui.lang_button,
                self.ui.log_button,
                self.ui.network_button,
                self.ui.version_Button
        ):
            btn.setCheckable(True)

        self.ui.color_button.clicked.connect(lambda: self.set_page(0))
        self.ui.sc_button.clicked.connect(lambda: self.set_page(1))
        self.ui.lang_button.clicked.connect(lambda: self.set_page(2))
        self.ui.log_button.clicked.connect(lambda: self.set_page(3))
        self.ui.network_button.clicked.connect(lambda: self.set_page(4))
        self.ui.version_Button.clicked.connect(lambda: self.set_page(5))
        self.ui.apply_button.clicked.connect(self.save_info)
        self.ui.cancel_button.clicked.connect(self.cancel)

        self.page: int = 0
        self.show_color_setting()

    def set_sampling_rate(self, rate):
        self.log_setting.sample_rate = rate

    def set_file_size(self, header_size, row_size):
        self.log_setting.header_size = header_size
        self.log_setting.row_size = row_size

    def save_info(self):
        if self.page == 0:
            self.color_setting.validate()
            self.themeSaveRequested.emit(self.color_setting.info)
        elif self.page == 1:
            if self.shortcut_setting.validate():
                self.shortcutSaveRequested.emit(self.shortcut_setting.info)
        elif self.page == 2:
            self.language_setting.validate()
            self.languageSaveRequested.emit(self.language_setting.info)
        elif self.page == 3:
            self.log_setting.validate()
            self.logSaveRequested.emit(self.log_setting.info)
        elif self.page == 4:
            self.network_setting.validate()
            self.networkSaveRequested.emit(self.network_setting.info)

        else:
            print("Invalid page number")

    def cancel(self):
        self.color_setting.cancel()
        self.shortcut_setting.cancel()
        self.language_setting.cancel()
        self.log_setting.cancel()
        self.network_setting.cancel()
        self.close()

    def closeEvent(self, event):
        self.cancel()
        event.accept()

    def close_all_tabs(self):
        self.color_setting.setVisible(False)
        self.shortcut_setting.setVisible(False)
        self.language_setting.setVisible(False)
        self.log_setting.setVisible(False)
        self.network_setting.setVisible(False)
        self.version_setting.setVisible(False)

    def show_color_setting(self):
        self.close_all_tabs()
        self.color_setting.setVisible(True)
        self.page = 0

    # 親要素のStyleSheetを引き継ぐため、子要素のStyleSheetを削除する
    def reset_stylesheet(self):
        self.setStyleSheet("")
        self.ui.apply_button.setStyleSheet("")
        self.ui.cancel_button.setStyleSheet("")

    def update_language(self):
        self.color_setting.ui.retranslateUi(self.color_setting)
        self.shortcut_setting.ui.retranslateUi(self.shortcut_setting)
        self.language_setting.ui.retranslateUi(self.language_setting)
        self.log_setting.ui.retranslateUi(self.log_setting)
        self.network_setting.ui.retranslateUi(self.network_setting)
        self.version_setting.ui.retranslateUi(self.version_setting)

    def set_page(self, page: int):
        self.close_all_tabs()
        self.reset_menu_selection()

        if page == 0:
            self.color_setting.setVisible(True)
            self.ui.color_button.setChecked(True)
        elif page == 1:
            self.shortcut_setting.setVisible(True)
            self.ui.sc_button.setChecked(True)
        elif page == 2:
            self.language_setting.setVisible(True)
            self.ui.lang_button.setChecked(True)
        elif page == 3:
            self.log_setting.setVisible(True)
            self.ui.log_button.setChecked(True)
        elif page == 4:
            self.network_setting.setVisible(True)
            self.ui.network_button.setChecked(True)
        elif page == 5:
            self.version_setting.setVisible(True)
            self.ui.version_Button.setChecked(True)

        self.page = page

    def reset_menu_selection(self):
        for btn in (
                self.ui.color_button,
                self.ui.sc_button,
                self.ui.lang_button,
                self.ui.log_button,
                self.ui.network_button,
                self.ui.version_Button,
        ):
            btn.setChecked(False)