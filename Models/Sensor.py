import threading

from dataclasses import dataclass
from enum import Enum

# --------------------------
# 列挙型の定義
# --------------------------
class SensorChKind(Enum):
    sensor_ch1 = 0
    sensor_ch2 = 1
    sensor_ch3 = 2
    sensor_ch4 = 3
    sensor_num = 4

class RegPageKind(Enum):
    sensor_reg_page0 = 0
    sensor_reg_page1 = 1
    sensor_reg_page2 = 2
    sensor_reg_page_num = 3

class SensorStandbyKind(Enum):
    standby_off = 0
    standby_on = 1

class SensorConnectionStatusKind(Enum):
    no_connect = 0
    connected = 1
    no_response = 2

class ErrorStatusKind(Enum):
    error_none = 0
    tmp_error = 1
    cal_error = 2
    mem_error = 3
    rom_error = 4
    sec_error = 5

class SensorTypeKind(Enum):
    sr500 = 0
    sr300 = 1

# --------------------------
# データ構造
# --------------------------
@dataclass
class RegData:
    addr: int = 0
    data: int = 0

@dataclass
class SensorStatus:
    temp: float = 0
    current_strain: int = 0
    init_strain: int = 0
    current_strain_value:float = 0
    init_strain_value:float = 0
    status: ErrorStatusKind = ErrorStatusKind.error_none
    connection_status: SensorConnectionStatusKind = SensorConnectionStatusKind.no_connect

class Sensor:

    def __init__(self):
        self.is_enable = False
        self.status = 0
        self.last_temp = 0
        self.last_strain = 0
        self.last_strain_value = 0
        self.init_temp = 0
        self.init_strain = 0
        self.init_strain_value = 0
        self.strain_value = 0
        self.standby = SensorStandbyKind.standby_off
        self._lock = threading.Lock()
        self.connection_status = SensorConnectionStatusKind.no_connect
        self.reg_data = []

    # 抽象メソッド
    def set_registers(self, page:int, data_list:list[RegData]):
        raise NotImplementedError()
    def update_register_calc_value(self):
        raise NotImplementedError()
    def set_strain_value(self, value:int):
        raise NotImplementedError()
    def set_init(self, strain, temp):
        raise NotImplementedError()
    def calc_strain_value(self):
        raise NotImplementedError()
    def calc_strain_value2(self, strain:int) -> float:
        raise NotImplementedError()
    def set_sensor_status(self, status:int, temp:float, strain:int, is_enable:bool):
        raise NotImplementedError()
    def get_sensor_status(self) -> SensorStatus:
        raise NotImplementedError()
    def get_sensor_id(self) -> int:
        raise NotImplementedError()

