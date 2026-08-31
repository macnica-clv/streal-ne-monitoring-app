import threading

from dataclasses import dataclass
from Models.Sensor import Sensor, RegPageKind, SensorConnectionStatusKind, RegData, SensorStatus, ErrorStatusKind
from enum import Enum

# --------------------------
# 列挙型の定義
# --------------------------
class SensorChKindSR300(Enum):
    sensor_ch1 = 0
    sensor_ch2 = 1
    sensor_ch3 = 2
    sensor_ch4 = 3
    sensor_num = 4

class RegAddrKindSR300(Enum):
    GAIN = 0b001
    SG = 0b010
    DOFS = 0b011
    TOFS = 0b100
    TE_AD = 0b101
    DRV = 0b110
    ID = 0b111
    REG_NUM = 0b1000

class SensorSR300(Sensor):
    SENSOR_ADS_ADGAIN_SHIFT = 2
    SENSOR_ADS_ADGAIN_MASK = 0x01
    SENSOR_ID_ERROR_SHIFT = 7
    SENSOR_ID_ERROR_MASK = 0x01
    SENSOR_ID_SEC_SHIFT = 2
    SENSOR_ID_SEC_MASK = 0x01
    SENSOR_ID_MASK = 0x03

    def __init__(self):
        super().__init__()
        self.reg_range = 0

        # レジスタ情報を全て0で初期化
        with self._lock:
            self.reg_data = [[0 for _ in range(RegAddrKindSR300.REG_NUM.value)] for _ in range(RegPageKind.sensor_reg_page_num.value)]

    def set_registers(self, page:int, data_list:list[RegData]):
        for data in data_list:
            self.reg_data[page][data.addr] = data.data
        self.update_register_calc_value()

    def update_register_calc_value(self):
        with self._lock:
            reg_ads = self.reg_data[0][RegAddrKindSR300.TE_AD.value]
            self.reg_range = (reg_ads >> self.SENSOR_ADS_ADGAIN_SHIFT) & self.SENSOR_ADS_ADGAIN_MASK

    def set_strain_value(self, value:int):
        with self._lock:
            self.last_strain = value
            self.last_strain_value = self.calc_strain_value2(value)
        self.calc_strain_value()

    def set_init(self, strain, temp):
        self.init_strain = strain
        self.init_temp = temp
        self.init_strain_value = self.calc_strain_value2(strain)

    def calc_strain_value(self):
        with self._lock:
            self.strain_value = self.last_strain - self.init_strain
            if self.reg_range:
                self.strain_value /= 2

    def calc_strain_value2(self, strain:int) -> float:
        value = strain
        if self.reg_range:
            value /= 2

        return value

    def set_sensor_status(self, status:int, temp:float, strain:int, is_enable:bool):
        with self._lock:
            reg_id = self.reg_data[0][RegAddrKindSR300.ID.value]
            rom_error = (reg_id >> self.SENSOR_ID_ERROR_SHIFT) & self.SENSOR_ID_ERROR_MASK
            sec_error = (reg_id >> self.SENSOR_ID_SEC_SHIFT) & self.SENSOR_ID_SEC_MASK

            if rom_error:
                status = ErrorStatusKind.rom_error
            elif sec_error:
                status = ErrorStatusKind.sec_error
            else:
                status = ErrorStatusKind.error_none
            self.status = status
            self.last_temp = temp
            self.last_strain = strain
            self.is_enable = is_enable
            self.last_strain_value = self.calc_strain_value2(strain)
            connection = SensorConnectionStatusKind.connected if is_enable else SensorConnectionStatusKind.no_connect
            if connection == SensorConnectionStatusKind.no_connect:
                if self.connection_status == SensorConnectionStatusKind.connected:
                    self.connection_status = SensorConnectionStatusKind.no_response
                else:
                    # 前値保持
                    pass
            else:
                self.connection_status = connection
        self.calc_strain_value()

    def get_sensor_status(self) -> SensorStatus:
        with self._lock:
            sensor_status = SensorStatus()
            sensor_status.temp = self.last_temp
            sensor_status.current_strain = self.last_strain
            sensor_status.init_strain = self.init_strain
            sensor_status.current_strain_value = self.last_strain_value
            sensor_status.init_strain_value = self.init_strain_value
            sensor_status.status = self.status
            sensor_status.connection_status = self.connection_status
            return sensor_status

    def get_sensor_id(self) -> int:
        return self.reg_data[0][RegAddrKindSR300.ID.value] & self.SENSOR_ID_MASK

