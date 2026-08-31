from sys import version_info

from PySide6.QtCore import QObject, Signal
from PySide6 import QtCore
from PySide6.QtGui import QPixmap

from Utils.MessageBox import ConfirmDialog, InfoDialog
from Models.Board import BoardKind
from Models.Config import Config, ConfigThemeSettings, ConfigShortcutSettings, ConfigLanguageSettings, ConfigLogSettings, ConfigNetworkSettings, ConnectionMethodKind
from Models.Hizmil_Driver import HizmilDriver, ResultKind
from Views.SettingView import SettingPage, SettingPageInfo, \
    ThemeSettingInfo, ShortcutSettingInfo, LanguageSettingInfo, LogSettingInfo, NetworkSettingInfo, VersionSettingInfo


class SettingController(QObject):
    themeChanged = Signal()
    scChanged = Signal()
    langChanged = Signal()
    networkChanged = Signal()
    versionChanged = Signal()

    def __init__(self, config: Config,  driver: HizmilDriver, parent=None):
        super(SettingController, self).__init__(parent)
        self._config = config
        self._driver = driver
        config_theme = config.load_config_theme()
        config_sc = config.load_config_shortcut()
        config_lang = config.load_config_language()
        config_log = config.load_config_log()
        config_net = config.load_config_network()

        theme_info = ThemeSettingInfo(config_theme.window_theme)
        sc_info = ShortcutSettingInfo([config_sc.meas_start, config_sc.meas_stop, config_sc.auto_range, config_sc.save_log, config_sc.capture])
        lang_info = LanguageSettingInfo(config_lang.language)
        log_info = LogSettingInfo(config_log.log_auto_save, config_log.log_save_ma, config_log.log_save_fft, config_log.log_save_std,
                                  config_log.log_filename_prefix, config_log.log_save_dst, config_log.log_sampling_num, config_log.capture_save_dst)
        net_info = NetworkSettingInfo(config_net.device1_ip,config_net.device2_ip)
        version_info = VersionSettingInfo()

        self.page_info = SettingPageInfo(theme_info, sc_info, lang_info, log_info, net_info, version_info)

        self.setting_page = SettingPage(self.page_info, parent=parent)
        self.setting_page.themeSaveRequested.connect(self.save_theme_info)
        self.setting_page.shortcutSaveRequested.connect(self.save_shortcut_info)
        self.setting_page.languageSaveRequested.connect(self.save_language_info)
        self.setting_page.logSaveRequested.connect(self.save_log_info)
        self.setting_page.networkSaveRequested.connect(self.save_network_info)

    def set_driver(self, driver: HizmilDriver):
        self._driver = driver

    def set_sampling_rate(self, rate):
        self.setting_page.set_sampling_rate(rate)

    def set_file_size(self, header_size, row_size):
        self.setting_page.set_file_size(header_size, row_size)

    def save_theme_info(self, info: ThemeSettingInfo):
        config_theme = ConfigThemeSettings()
        config_theme.window_theme = info.theme_index
        self._config.save_config_theme(config_theme)
        self.update_theme_preview(info.theme_index)
        self.themeChanged.emit()

    def save_shortcut_info(self, info: ShortcutSettingInfo):
        config_sc = ConfigShortcutSettings()
        config_sc.meas_start = info.shortcuts[0]
        config_sc.meas_stop = info.shortcuts[1]
        config_sc.auto_range = info.shortcuts[2]
        config_sc.save_log = info.shortcuts[3]
        config_sc.capture = info.shortcuts[4]
        self._config.save_config_shortcut(config_sc)
        self.scChanged.emit()

    def save_language_info(self, info: LanguageSettingInfo):
        config_lang = ConfigLanguageSettings()
        config_lang.language = info.lang_index
        self._config.save_config_language(config_lang)
        self.langChanged.emit()

    def save_log_info(self, info: LogSettingInfo):
        config_log = ConfigLogSettings()
        config_log.log_auto_save = info.auto_save
        config_log.log_save_ma = info.save_ma
        config_log.log_save_fft = info.save_fft
        config_log.log_save_std = info.save_std
        config_log.log_filename_prefix = info.log_filename_prefix
        config_log.log_save_dst = info.log_save_dst
        config_log.log_sampling_num = info.sample_num
        config_log.capture_save_dst = info.cap_save_dst
        self._config.save_config_log(config_log)

    def save_network_info(self, info: NetworkSettingInfo):
        # --- Config 保存 ---
        config_net = ConfigNetworkSettings()
        config_net.device1_ip = info.device1_ip
        config_net.device2_ip = info.device2_ip
        self._config.save_config_network(config_net)

        # --- ドライバ未接続 ---
        if not self._driver.is_connected():
            InfoDialog(
                "Network Setting",
                "The device is not connected."
            ).exec()
            return

        try:
            # --- IP 書き込み ---
            if info.device1_ip:
                ip1 = self.ip_to_bytes(info.device1_ip)
                self._driver.set_network_address(
                    BoardKind.board1,
                    self._driver.NETWORK_ADDR_TYPE_IP,
                    ip1
                )

            if info.device2_ip:
                ip2 = self.ip_to_bytes(info.device2_ip)
                self._driver.set_network_address(
                    BoardKind.board2,
                    self._driver.NETWORK_ADDR_TYPE_IP,
                    ip2
                )

            # ✅ 通信方式に関係なくメッセージ表示
            InfoDialog(
                "Network Setting",
                "IP address has been configured.\nPlease restart the device."
            ).exec()

        except Exception as e:
            print("Invalid IP:", e)
            InfoDialog(
                "Network Setting",
                "An error occurred while configuring the IP address."
            ).exec()

        self.networkChanged.emit()

    def ip_to_bytes(self, ip: str) -> bytearray:
        parts = ip.split(".")
        if len(parts) != 4:
            raise ValueError("Invalid IP format")

        return bytearray(int(p) for p in parts)

    def show(self):
        self.setting_page.setVisible(True)
        self.setting_page.set_page(0)

        theme = self._config.load_config_theme().window_theme
        self.update_theme_preview(theme)

    def hide(self):
        self.setting_page.setVisible(False)

    def update_language(self):
        self.setting_page.ui.retranslateUi(self.setting_page)
        self.setting_page.update_language()

    # SettingController �ɒǉ�
    def update_theme_preview(self, theme: int):
        if hasattr(self.setting_page, "color_setting"):
            self.setting_page.color_setting.update_theme_preview(theme)

