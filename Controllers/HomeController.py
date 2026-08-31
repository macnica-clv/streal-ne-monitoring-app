from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication

from Utils.Com import get_com_port_list
from Models.Config import Config, ConfigDataHome
from Models.Hizmil_Driver import HizmilDriver, ConnectionStatus
from Views import HomeView
from Views.HomeView import ConnectionLogStatus


class HomeController:
    def __init__(self, config:Config, parent=None):
        self._driver = HizmilDriver()
        self._config = config
        self._ports = []
        self._log_updated = False
        self._result : ConnectionStatus = ConnectionStatus.success

        self.home_page = HomeView.HomePage(parent=parent)

        self.get_com_list()
        self.load_config()

        self.usb_watcher_timer = QtCore.QTimer()
        self.usb_watcher_timer.timeout.connect(self.check_usb)
        self.usb_watcher_timer.start(1000)

    def show(self):
        self.home_page.setVisible(True)

    def hide(self):
        self.home_page.setVisible(False)

    def set_driver(self, driver: HizmilDriver):
        self._driver = driver

    def request_signal(self):
        return self.home_page.setting_bridge.connectRequested

    def disconnect_signal(self):
        return self.home_page.setting_bridge.disconnectRequested

    def get_com_list(self):
        self._ports = get_com_port_list(vid=0x3398, pid=0x0001)
        print(f"ports: {self._ports}", flush=True)
        self.home_page.update_com_list(self._ports)

    def update_board_status(self, versions: list[str], board_type: str, ports: list[str]):
        self.home_page.status_bridge.update_board_status(versions, board_type, ports)

    def update_sensor_status(self, statuses: list[int]):
        self.home_page.status_bridge.update_sensor_status(statuses)

    def update_sensor_ids(self, ids: list[str]):
        self.home_page.status_bridge.update_sensor_ids(ids)

    def load_config(self):
        param = self._config.load_config_home()
        self.home_page.setting_bridge.update_method(param.connection_method)
        self.home_page.setting_bridge.update_com_indexes([param.com1, param.com2])
        self.home_page.setting_bridge.update_ip_addr([param.ip_addr1, param.ip_addr2])

    def handle_app_closing(self):
        param = ConfigDataHome()
        param.connection_method = self.home_page.setting_bridge.method
        param.com1 = self.home_page.setting_bridge.com_port(0)
        param.com2 = self.home_page.setting_bridge.com_port(1)
        param.ip_addr1 = self.home_page.setting_bridge.ip_port(0)
        param.ip_addr2 = self.home_page.setting_bridge.ip_port(1)
        self._config.save_config_home(param)

    def check_usb(self):
        if not self._driver.is_connected():
            ports = get_com_port_list(vid=0x3398, pid=0x0001)
            if not self._ports == ports:
                self._ports = ports
                self.home_page.update_com_list(self._ports)
                param = self._config.load_config_home()
                self.home_page.setting_bridge.update_com_indexes([param.com1, param.com2])

    def update_log(self, result:ConnectionStatus):
        self._log_updated = True
        log = ConnectionLogStatus.other_error
        if result == ConnectionStatus.success:
            log = ConnectionLogStatus.success
        elif result == ConnectionStatus.sensor_not_detected:
            log = ConnectionLogStatus.sensor_not_detected
        elif result == ConnectionStatus.board_not_detected:
            log = ConnectionLogStatus.board_not_detected
        elif result == ConnectionStatus.mixed_sensor:
            log = ConnectionLogStatus.mixed_sensor

        self.home_page.update_log(log)
        self._result = result

    def notify_disconnected(self):
        self.home_page.update_log(ConnectionLogStatus.disconnected)

    def update_language(self):
        self.home_page.ui.retranslateUi(self.home_page)
        if self._log_updated:
            self.update_log(self._result)
