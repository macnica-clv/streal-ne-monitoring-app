import threading

from Models.Sensor import Sensor, RegPageKind, SensorConnectionStatusKind, RegData, SensorStatus, ErrorStatusKind
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


class RegAddrKind(Enum):
    STRDATA = 0x00
    TMPDATA = 0x01
    CTRL = 0x02
    STATUS = 0x03
    CONFIG = 0x04
    TMPCONF = 0x05
    OFFSETCOEF0 = 0x06
    OFFSETTMPCOEF0 = 0x07
    SENSCOEF0 = 0x08
    SENSTMPCOEF0 = 0x09
    OFFSETCOEF1 = 0x0A
    OFFSETTMPCOEF1 = 0x0B
    SENSCOEF1 = 0x0C
    SENSTMPCOEF1 = 0x0D
    FSADJOFFSETCOEF = 0x0E
    FSADJGAINCOEF = 0x0F
    G2COEF = 0x10
    PGACONF = 0x11
    ANACAL = 0x12
    DMACTRL = 0x13
    MEMCTRL = 0x14
    MEMADR = 0x15
    MEMDATA0 = 0x16
    MEMDATA1 = 0x17
    ID = 0x1C
    WLOCK = 0x1D
    CHKSUM = 0x1E
    PAGE = 0x1F
    REG_NUM = 0x20

class SensorStandbyKind(Enum):
    standby_off = 0
    standby_on = 1


# --------------------------
# データ構造
# --------------------------
@dataclass
class RegData:
    addr: int = 0
    data: int = 0


class SensorSR500:
    # --------------------------
    # データテーブル
    # --------------------------
    PGAGAIN = [
        50,
        62.5,
        83.3,
        125,
        41.7,
        31.3,
        25,
        8.3
    ]

    SCAL = [
        1.500,
        1.563,
        1.625,
        1.688,
        1.750,
        1.813,
        1.875,
        1.938,
        1.438,
        1.375,
        1.313,
        1.250,
        1.188,
        1.125,
        1.063,
        1.000
    ]

    TMPERR_MASK = 0x08
    CALERR_MASK = 0x10
    MEMERR_MASK = 0x20

    def __init__(self):
        self.is_enable = False
        self.status = 0
        self.reg_scal = 0
        self.reg_pga_gain = 0
        self.reg_fsadjgain_coef = 0
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

        # レジスタ情報を全て0で初期化
        with self._lock:
            self.reg_data = [[0 for _ in range(RegAddrKind.REG_NUM.value)] for _ in range(RegPageKind.sensor_reg_page_num.value)]

    def set_registers(self, page:int, data_list:list[RegData]):
        for data in data_list:
            self.reg_data[page][data.addr] = data.data
        self.update_register_calc_value()

    def update_register_calc_value(self):
        with self._lock:
            reg_anacal = self.reg_data[RegPageKind.sensor_reg_page0.value][RegAddrKind.ANACAL.value]
            self.reg_scal = self.SCAL[reg_anacal >> 8 & 0x000F]
            reg_pga_conf = self.reg_data[RegPageKind.sensor_reg_page0.value][RegAddrKind.PGACONF.value]
            self.reg_pga_gain = self.PGAGAIN[reg_pga_conf & 0x0007]
            self.reg_fsadjgain_coef = self.reg_data[RegPageKind.sensor_reg_page0.value][RegAddrKind.FSADJGAINCOEF.value]

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
            value = (50 * self.reg_scal) * self.reg_pga_gain
            value /= 5.0
            value *= self.reg_fsadjgain_coef
            value /= 0x2000
            value *= 0x10000

            if value != 0:
                self.strain_value = (self.last_strain - self.init_strain) / value
                # 単位をεからμεに変更する
                self.strain_value *= 1000000

    def calc_strain_value2(self, strain:int) -> float:
        value = (50 * self.reg_scal) * self.reg_pga_gain
        value /= 5.0
        value *= self.reg_fsadjgain_coef
        value /= 0x2000
        value *= 0x10000

        if value != 0:
            value = strain / value
            # 単位をεからμεに変更する
            value *= 1000000

        return value

    def set_sensor_status(self, status:int, temp:float, strain:int, is_enable:bool):
        with self._lock:
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
            if not self.status & self.TMPERR_MASK == 0:
                sensor_status.status = ErrorStatusKind.tmp_error
            elif not self.status & self.CALERR_MASK == 0:
                sensor_status.status = ErrorStatusKind.cal_error
            elif not self.status & self.MEMERR_MASK == 0:
                sensor_status.status = ErrorStatusKind.mem_error
            else:
                sensor_status.status = ErrorStatusKind.error_none
            sensor_status.connection_status = self.connection_status
            return sensor_status

    def get_sensor_id(self) -> int:
        return self.reg_data[RegPageKind.sensor_reg_page0.value][RegAddrKind.ID.value]

