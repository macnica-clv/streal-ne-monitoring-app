from enum import Enum
from operator import truediv
from typing import Optional

from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Property, Slot, QObject, QSize
from PySide6.QtWidgets import QWidget

from Views import Home_Page, resources_rc
from Views.MainView import tinted_qicon, DummyAppBridge


class ConnectionLogStatus(Enum):
    success = 0
    sensor_not_detected = 1
    board_not_detected = 2
    other_error = 3
    mixed_sensor = 4
    disconnected = 5

class ConnectSetting(QObject):
    methodChanged = Signal()
    comUpdated = Signal()
    ipUpdated = Signal()
    indexUpdated = Signal()
    connectRequested = Signal(int, list)
    disconnectRequested = Signal()

    def __init__(self):
        super(ConnectSetting, self).__init__()
        self._connect_method = 0
        self._com_port_num = 2
        self._com_lists: list[list[str]] = [[] for _ in range(self._com_port_num)]
        self._com_indexes: list[int] = [0 for _ in range(self._com_port_num)]
        self._ip_ports: list[list[int]] = [[0, 0, 0, 0] for _ in range(self._com_port_num)]

    @Property(int, notify=methodChanged)
    def method(self):
        return self._connect_method
    @Property(list, notify=comUpdated)
    def com_lists(self):
        return self._com_lists
    @Property(list, notify=indexUpdated)
    def com_indexes(self):
        return self._com_indexes
    @Property(list, notify=ipUpdated)
    def ip_ports(self):
        return self._ip_ports

    def com_port(self, index):
        return self._com_lists[index][self._com_indexes[index]]
    def ip_port(self, index):
        return ".".join([str(i) for i in self._ip_ports[index]])

    @Slot(int)
    def set_method(self, value):
        self._connect_method = value
    @Slot(int, int)
    def set_com_port(self, index, value):
        self._com_indexes[index] = value
    @Slot(int, int, int)
    def set_ip_port(self, index, number, value):
        self._ip_ports[index][number] = value
    @Slot()
    def connect_proc(self):
        if self._connect_method == 0:
            ports = [self.com_port(i).replace("-", "") for i in range(self._com_port_num)]
            self.connectRequested.emit(self._connect_method, ports)
        elif self._connect_method == 1:
            ips = [self.ip_port(i) for i in range(self._com_port_num)]
            self.connectRequested.emit(self._connect_method, ips)

    @Slot()
    def disconnect_proc(self):
        self.disconnectRequested.emit()

    def update_method(self, method: int):
        if 0 <= method < 2:
            self._connect_method = method
            self.methodChanged.emit()

    def update_com_ports(self, com_lists: list[list[str]]):
        for i in range(len(com_lists)):
            self._com_lists[i] = com_lists[i]
        self.comUpdated.emit()

    def update_com_indexes(self, ports: list[str]):
        for i in range(len(ports)):
            if ports[i] in self._com_lists[i]:
                self._com_indexes[i] = self._com_lists[i].index(ports[i])
            else:
                self._com_indexes[i] = 0
        self.indexUpdated.emit()

    def update_ip_addr(self, addr_list: list[str]):
        for i in range(len(addr_list)):
            addr = addr_list[i].split('.')
            if len(addr) != 4:
                self._ip_ports[i] = [0, 0, 0, 0]
            else:
                self._ip_ports[i] = [int(s) for s in addr]
        self.ipUpdated.emit()


class ConnectStatus(QObject):
    boardStatusUpdated = Signal()
    sensorStatusUpdated = Signal()
    sensorIdUpdated = Signal()

    def __init__(self):
        super(ConnectStatus, self).__init__()
        self._connected_board: str = "-----"
        self._connected_ports: list[str] = []
        self._board_versions: list[str] = []
        self._sensor_ids: list[str] = []
        self._sensor_statuses: list[int] = []

    @Property(str, notify=boardStatusUpdated)
    def connected_board(self):
        return self._connected_board
    @Property(str, notify=boardStatusUpdated)
    def connected_port(self):
        if len(self._connected_ports) == 0:
            return "-"
        return ", ".join([port for port in self._connected_ports if port])
    @Property(str, notify=boardStatusUpdated)
    def board_version(self):
        if len(self._board_versions) == 0:
            return "-"
        return ", ".join([version for version in self._board_versions if version])
    @Property(str, notify=sensorIdUpdated)
    def sensor_ids(self):
        if len(self._sensor_ids) == 0:
            return "-"
        return ", ".join([f"{sensor_id}" for sensor_id in self._sensor_ids])
    @Property(list, notify=sensorStatusUpdated)
    def sensor_status(self):
        return self._sensor_statuses

    def update_board_status(self, versions: list[str], board_type: str, ports: list[str]):
        self._connected_board = board_type
        self._connected_ports = ports
        self._board_versions = versions
        self.boardStatusUpdated.emit()

    def update_sensor_status(self, statuses: list[int]):
        self._sensor_statuses = statuses
        self.sensorStatusUpdated.emit()

    def update_sensor_ids(self, ids: list[str]):
        self._sensor_ids = ids
        self.sensorIdUpdated.emit()


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_bridge2 = DummyAppBridge(initial_theme=0)
        self.app_bridge3 = DummyAppBridge(initial_theme=0)
        self.ui = Home_Page.Ui_home_page()

        self.ui.setupUi(self)

        if self.app_bridge2 is not None:
            self.ui.connect_settings.rootContext().setContextProperty("appBridge2", self.app_bridge2)
        if self.app_bridge3 is not None:
            self.ui.connect_settings.rootContext().setContextProperty("appBridge3", self.app_bridge3)

        self.reset_stylesheet()

        self.setting_bridge = ConnectSetting()
        self.ui.connect_settings.rootContext().setContextProperty("bridge", self.setting_bridge)
        self.status_bridge = ConnectStatus()
        self.ui.connect_status.rootContext().setContextProperty("bridge", self.status_bridge)

        self._theme = 0
        self._last_log: ConnectionLogStatus | None = None



    def update_com_list(self, com_list: list[str]):
        if len(com_list) < 1:
            com_ports = [["-"], ["-"]]
        elif len(com_list) < 2:
            com_ports = [com_list, ["-"]]
        else:
            com_ports = [com_list, com_list]
        self.setting_bridge.update_com_ports(com_ports)

    def reset_stylesheet(self):
        """ 親要素のStyleSheetを引き継ぐため、子要素のStyleSheetを削除する """
        self.setStyleSheet("")
        self.ui.home_title.setStyleSheet("")
        self.ui.title_body.setStyleSheet("")
        self.ui.message_info.setStyleSheet("")
        self.ui.info_icon.setStyleSheet("")

    def update_log(self, log:ConnectionLogStatus):
        self._last_log = log
        """ ログのラベルとアイコンを更新する """
        success = True
        if log == ConnectionLogStatus.success:
            self.ui.message_body.setText(self.tr("Connection Successful"))
        elif log == ConnectionLogStatus.sensor_not_detected:
            self.ui.message_body.setText(self.tr("The sensor is not connected. Please connect the sensor."))
            success = False
        elif log == ConnectionLogStatus.board_not_detected:
            self.ui.message_body.setText(self.tr("The evaluation kit is not connected. Please connect the evaluation kit."))
            success = False
        elif log == ConnectionLogStatus.mixed_sensor:
            self.ui.message_body.setText(self.tr("Multiple sensor types are connected. Please connect only one type."))
            success = False
        elif log == ConnectionLogStatus.disconnected:
            self.ui.message_body.setText(self.tr("Disconnected."))
        else:
            self.ui.message_body.setText(self.tr("Connection Failed."))
            success = False

        color = self._message_color(success)
        self.ui.message_body.setStyleSheet(f"color: {color};")

        if success:
            self.ui.info_icon.setIcon(QIcon(":/HomePages/Images/Pages/HomePage/check-circled-outline.png"))
        else:
            self.ui.info_icon.setIcon(QIcon(":/HomePages/Images/Pages/HomePage/triangle-danger-f.png"))

    @staticmethod
    def force_same_disabled(icon: QIcon, size: QSize) -> QIcon:
        # Normal の見た目を pixmap として取り出して Disabled に登録
        pm = icon.pixmap(size, QIcon.Normal, QIcon.Off)
        icon.addPixmap(pm, QIcon.Disabled, QIcon.Off)
        return icon

    def _message_color(self, success: bool) -> str:
        if self._theme == 2:  # Dark
            return "#42BE65" if success else "#FF8389"
        else:  # Normal / Light
            return "green" if success else "red"

    def apply_theme(self, theme: int):
        self._theme = theme
        if theme == 0:      # Normal
            icon_color = "#2D3282"
        elif theme == 1:    # Light
            icon_color = "#21272A"
        else:                     # Dark
            icon_color = "#FFFFFF"

        sz40 = QSize(40, 40)
        icon = tinted_qicon(":/HomePages/Images/Pages/HomePage/home.png", icon_color, sz40)
        self.ui.title_icon.setIcon(self.force_same_disabled(icon, sz40))

        if self._last_log is not None:
            self.update_log(self._last_log)
