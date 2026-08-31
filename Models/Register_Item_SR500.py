from enum import Enum

from PySide6.QtCore import QCoreApplication

from Models.Hizmil_Driver import HizmilDriver, ResultKind
from Models.Sensor import RegData, RegPageKind
from Models.SensorSR500 import RegAddrKind


class ItemType(Enum):
    dec = 0
    hex = 1
    list = 2
    none = 3


class ItemKind(Enum):
    output_mode = 0
    osr = 1
    tmp_orig = 2
    tmp_th0 = 3
    offset_coef0 = 4
    offset_temp_coef0 = 5
    sense_coef0 = 6
    sense_temp_coef0 = 7
    offset_coef1 = 8
    offset_temp_coef1 = 9
    sense_coef1 = 10
    sense_temp_coef1 = 11
    fsadj_offset_coef = 12
    fsadj_gain_coef = 13
    offset_g2_coef = 14
    g2_coef = 15
    pga_conf = 16
    ocal = 17
    scal = 18
    reg_refresh_enable = 19
    id = 20
    item_num = 21

class RegisterItemSR500:
    """ 画面上のレジスタ設定を管理するクラス
        画面上の設定項目とSR500のレジスタは1対1にはなっていないため、このクラスにて吸収する
        コンボボックスで選択する設定項目については、インデックス番号でやりとりすること """

    item_name = {
        ItemKind.output_mode: "output_mode",
        ItemKind.osr: "osr",
        ItemKind.tmp_orig: "tmp_orig",
        ItemKind.tmp_th0: "tmp_th0",
        ItemKind.offset_coef0: "offset_coef0",
        ItemKind.offset_temp_coef0: "offset_temp_coef0",
        ItemKind.sense_coef0: "sense_coef0",
        ItemKind.sense_temp_coef0: "sense_temp_coef0",
        ItemKind.offset_coef1: "offset_coef1",
        ItemKind.offset_temp_coef1: "offset_temp_coef1",
        ItemKind.sense_coef1: "sense_coef1",
        ItemKind.sense_temp_coef1: "sense_temp_coef1",
        ItemKind.fsadj_offset_coef: "fsadj_offset_coef",
        ItemKind.fsadj_gain_coef: "fsadj_gain_coef",
        ItemKind.offset_g2_coef: "offset_g2_coef",
        ItemKind.g2_coef: "g2_coef",
        ItemKind.pga_conf: "pga_conf",
        ItemKind.ocal: "ocal",
        ItemKind.scal: "scal",
        ItemKind.reg_refresh_enable: "reg_refresh_enable",
        ItemKind.id: "id",
        ItemKind.item_num: "",
    }

    item_init = {
        ItemKind.output_mode: 0,
        ItemKind.osr: 0,
        ItemKind.tmp_orig: 0,
        ItemKind.tmp_th0: 0,
        ItemKind.offset_coef0: 0,
        ItemKind.offset_temp_coef0: 0,
        ItemKind.sense_coef0: 0,
        ItemKind.sense_temp_coef0: 0,
        ItemKind.offset_coef1: 0,
        ItemKind.offset_temp_coef1: 0,
        ItemKind.sense_coef1: 0,
        ItemKind.sense_temp_coef1: 0,
        ItemKind.fsadj_offset_coef: 0,
        ItemKind.fsadj_gain_coef: 0,
        ItemKind.offset_g2_coef: 0,
        ItemKind.g2_coef: 0,
        ItemKind.pga_conf: 0,
        ItemKind.ocal: 0,
        ItemKind.scal: 0,
        ItemKind.reg_refresh_enable: 1,
        ItemKind.id: 0
    }

    item_type: dict[ItemKind, ItemType] = {
        ItemKind.output_mode: ItemType.list,
        ItemKind.osr: ItemType.list,
        ItemKind.tmp_orig: ItemType.hex,
        ItemKind.tmp_th0: ItemType.hex,
        ItemKind.offset_coef0: ItemType.hex,
        ItemKind.offset_temp_coef0: ItemType.hex,
        ItemKind.sense_coef0: ItemType.hex,
        ItemKind.sense_temp_coef0: ItemType.hex,
        ItemKind.offset_coef1: ItemType.hex,
        ItemKind.offset_temp_coef1: ItemType.hex,
        ItemKind.sense_coef1: ItemType.hex,
        ItemKind.sense_temp_coef1: ItemType.hex,
        ItemKind.fsadj_offset_coef: ItemType.hex,
        ItemKind.fsadj_gain_coef: ItemType.hex,
        ItemKind.offset_g2_coef: ItemType.list,
        ItemKind.g2_coef: ItemType.list,
        ItemKind.pga_conf: ItemType.list,
        ItemKind.ocal: ItemType.dec,
        ItemKind.scal: ItemType.list,
        ItemKind.reg_refresh_enable: ItemType.list,
        ItemKind.id: ItemType.list,
        ItemKind.item_num: ItemType.none,
    }

    item_digit: dict[ItemKind, int] = {
        ItemKind.tmp_orig: 2,
        ItemKind.tmp_th0: 2,
        ItemKind.offset_coef0: 4,
        ItemKind.offset_temp_coef0: 4,
        ItemKind.sense_coef0: 4,
        ItemKind.sense_temp_coef0: 4,
        ItemKind.offset_coef1: 4,
        ItemKind.offset_temp_coef1: 4,
        ItemKind.sense_coef1: 4,
        ItemKind.sense_temp_coef1: 4,
        ItemKind.fsadj_offset_coef: 4,
        ItemKind.fsadj_gain_coef: 4,
        ItemKind.ocal: 4,
    }

    """ 最小値、最大値、刻み幅、スケール """
    item_range: dict[ItemKind, tuple[int, int, int]] = {
        ItemKind.tmp_orig: (0, 0xFF, 1),
        ItemKind.tmp_th0: (0, 0xFF, 1),
        ItemKind.offset_coef0: (0, 0xFFFF, 1),
        ItemKind.offset_temp_coef0: (0, 0xFFFF, 1),
        ItemKind.sense_coef0: (0, 0xFFFF, 1),
        ItemKind.sense_temp_coef0: (0, 0xFFFF, 1),
        ItemKind.offset_coef1: (0, 0xFFFF, 1),
        ItemKind.offset_temp_coef1: (0, 0xFFFF, 1),
        ItemKind.sense_coef1: (0, 0xFFFF, 1),
        ItemKind.sense_temp_coef1: (0, 0xFFFF, 1),
        ItemKind.fsadj_offset_coef: (0, 0xFFFF, 1),
        ItemKind.ocal: (-128, 127, 1),
        ItemKind.fsadj_gain_coef: (0, 0xFFFF, 1)
    }

    def __init__(self, driver : HizmilDriver, ch:int):
        self._driver = driver
        self._ch = ch
        self._item = []
        for i in range(ItemKind.item_num.value):
            self._item.append(0)
        self.update_item_map()

    def update_item_map(self):
        self.item_map = {
            ItemKind.output_mode: [
                QCoreApplication.translate("RegisterItemSR500", "Digital Output Mode"),
                QCoreApplication.translate("RegisterItemSR500", "Analog Output Mode")
            ],
            ItemKind.osr: [
                QCoreApplication.translate("RegisterItemSR500", "ADC:192, DAC:32, Input Bandwidth:5449"),
                QCoreApplication.translate("RegisterItemSR500", "ADC:384, DAC:64, Input Bandwidth:2725"),
                QCoreApplication.translate("RegisterItemSR500", "ADC:768, DAC:128, Input Bandwidth:1365"),
                QCoreApplication.translate("RegisterItemSR500", "ADC:1536, DAC:-, Input Bandwidth:681")
            ],
            ItemKind.fsadj_gain_coef: [
                "D555 (±100με)",
                "6aaa (±200με)",
                "471c (±300με)",
                "3555 (±400με)",
                "2aaa (±500με)",
                "238e (±600με)",
                "1e79 (±700με)",
                "1aaa (±800με)",
                "17b4 (±900με)",
                "1555 (±1000με)"
            ],
            ItemKind.offset_g2_coef: [
                QCoreApplication.translate("RegisterItemSR500","1x"),
                QCoreApplication.translate("RegisterItemSR500","2x")
            ],
            ItemKind.g2_coef: [
                QCoreApplication.translate("RegisterItemSR500","1x"),
                QCoreApplication.translate("RegisterItemSR500","2x"),
                QCoreApplication.translate("RegisterItemSR500","4x"),
                QCoreApplication.translate("RegisterItemSR500","8x"),
                QCoreApplication.translate("RegisterItemSR500","16x")
            ],
            ItemKind.pga_conf: [
                "50",
                "62.5",
                "83.3",
                "125",
                "41.7",
                "31.3",
                "25",
                "8.3"
            ],
            #ItemKind.ocal: [str(i) for i in range(127, -128, -1)] + ["0(-128)"],
            ItemKind.scal: [
                "1.868",
                "1.945",
                "2.022",
                "2.098",
                "2.175",
                "2.251",
                "2.326",
                "2.401",
                "1.791",
                "1.714",
                "1.636",
                "1.559",
                "1.482",
                "1.404",
                "1.327",
                "1.249"
            ],
            ItemKind.reg_refresh_enable: [
                QCoreApplication.translate("RegisterItemSR500","Disable"),
                QCoreApplication.translate("RegisterItemSR500","Enable")
            ],
            ItemKind.id: [
                "0",
                "1",
                "2",
                "3"
            ]
        }

    def read_item(self) -> list[int]:
        """ 現在のレジスタ値を取得して設定値に反映する """
        board, board_ch = self._driver.get_board_ch(self._ch)
        reg_data = self._driver.board[board.value].sensor[board_ch].reg_data[0]

        # アウトプットモード
        val = reg_data[RegAddrKind.CONFIG.value] & 0x0001
        self._item[ItemKind.output_mode.value] = val

        # OSR
        val = (reg_data[RegAddrKind.CONFIG.value] >> 1) & 0x0003
        self._item[ItemKind.osr.value] = val

        # 補正基準温度
        val = reg_data[RegAddrKind.TMPCONF.value] & 0x00FF
        self._item[ItemKind.tmp_orig.value] = val

        # 温度境界
        val = (reg_data[RegAddrKind.TMPCONF.value] >> 8) & 0x00FF
        self._item[ItemKind.tmp_th0.value] = val

        # オフセット補正係数(TMPDATA < TMPTH0)
        self._item[ItemKind.offset_coef0.value] = reg_data[RegAddrKind.OFFSETCOEF0.value]

        # 温度オフセット補正係数(TMPDATA < TMPTH0)
        self._item[ItemKind.offset_temp_coef0.value] = reg_data[RegAddrKind.OFFSETTMPCOEF0.value]

        # 感度補正係数(TMPDATA < TMPTH0)
        self._item[ItemKind.sense_coef0.value] = reg_data[RegAddrKind.SENSCOEF0.value]

        # 温度感度補正係数(TMPDATA < TMPTH0)
        self._item[ItemKind.sense_temp_coef0.value] = reg_data[RegAddrKind.SENSTMPCOEF0.value]

        # オフセット補正係数(TMPDATA >= TMPTH0)
        self._item[ItemKind.offset_coef1.value] = reg_data[RegAddrKind.OFFSETCOEF1.value]

        # 温度オフセット補正係数(TMPDATA >= TMPTH0)
        self._item[ItemKind.offset_temp_coef1.value] = reg_data[RegAddrKind.OFFSETTMPCOEF1.value]

        # 感度補正係数(TMPDATA >= TMPTH0)
        self._item[ItemKind.sense_coef1.value] = reg_data[RegAddrKind.SENSCOEF1.value]

        # 温度感度補正係数(TMPDATA >= TMPTH0)
        self._item[ItemKind.sense_temp_coef1.value] = reg_data[RegAddrKind.SENSTMPCOEF1.value]

        # デジタル補正演算(オフセット係数)
        self._item[ItemKind.fsadj_offset_coef.value] = reg_data[RegAddrKind.FSADJOFFSETCOEF.value]

        # デジタル補正演算(ゲイン係数)
        self._item[ItemKind.fsadj_gain_coef.value] = reg_data[RegAddrKind.FSADJGAINCOEF.value]

        # デジタル補正演算(オフセット補正量)
        val = reg_data[RegAddrKind.G2COEF.value] & 0x0007
        self._item[ItemKind.offset_g2_coef.value] = val

        # デジタル補正演算(ゲイン設定)
        val = (reg_data[RegAddrKind.G2COEF.value] >> 4) & 0x0007
        self._item[ItemKind.g2_coef.value] = val

        # PGAのゲイン設定
        val = reg_data[RegAddrKind.PGACONF.value] & 0x0007
        self._item[ItemKind.pga_conf.value] = val

        # PGAでのオフセット補正量
        val = reg_data[RegAddrKind.ANACAL.value] & 0x00FF
        self._item[ItemKind.ocal.value] = val if val < 127 else val - 256

        # センサ励起電流量[mA]
        val = (reg_data[RegAddrKind.ANACAL.value] >> 8) & 0x000F
        self._item[ItemKind.scal.value] = val

        # レジスタリフレッシュ動作
        val = reg_data[RegAddrKind.DMACTRL.value] & 0x0001
        self._item[ItemKind.reg_refresh_enable.value] = val

        # ID
        val = reg_data[RegAddrKind.ID.value] & 0x0003
        self._item[ItemKind.id.value] = val

        return self._item

    def write_item(self) -> bool:
        """ 現在の設定値をレジスタに書き込む """
        board, board_ch = self._driver.get_board_ch(self._ch)
        reg_data = self._driver.board[board.value].sensor[board_ch].reg_data
        write_data : list[RegData] = []

        # アウトプットモード
        # OSR
        val = reg_data[RegPageKind.sensor_reg_page0.value][RegAddrKind.CONFIG.value] & 0x0100
        val |= self._item[ItemKind.output_mode.value] & 0x0001
        val |= (self._item[ItemKind.osr.value] << 1) & 0x0006
        reg = RegData(addr=RegAddrKind.CONFIG.value, data=val)
        write_data.append(reg)

        # 補正基準温度
        # 温度境界
        val = (self._item[ItemKind.tmp_th0.value] << 8 ) | self._item[ItemKind.tmp_orig.value]
        reg = RegData(addr=RegAddrKind.TMPCONF.value, data=val)
        write_data.append(reg)

        # オフセット補正係数(TMPDATA < TMPTH0)
        reg = RegData(addr=RegAddrKind.OFFSETCOEF0.value, data=self._item[ItemKind.offset_coef0.value])
        write_data.append(reg)

        # 温度オフセット補正係数(TMPDATA < TMPTH0)
        reg = RegData(addr=RegAddrKind.OFFSETTMPCOEF0.value, data=self._item[ItemKind.offset_temp_coef0.value])
        write_data.append(reg)

        # 感度補正係数(TMPDATA < TMPTH0)
        reg = RegData(addr=RegAddrKind.SENSCOEF0.value, data=self._item[ItemKind.sense_coef0.value])
        write_data.append(reg)

        # 温度感度補正係数(TMPDATA < TMPTH0)
        reg = RegData(addr=RegAddrKind.SENSTMPCOEF0.value, data=self._item[ItemKind.sense_temp_coef0.value])
        write_data.append(reg)

        # オフセット補正係数(TMPDATA >= TMPTH0)
        reg = RegData(addr=RegAddrKind.OFFSETCOEF1.value, data=self._item[ItemKind.offset_coef1.value])
        write_data.append(reg)

        # 温度オフセット補正係数(TMPDATA >= TMPTH0)
        reg = RegData(addr=RegAddrKind.OFFSETTMPCOEF1.value, data=self._item[ItemKind.offset_temp_coef1.value])
        write_data.append(reg)

        # 感度補正係数(TMPDATA >= TMPTH0)
        reg = RegData(addr=RegAddrKind.SENSCOEF1.value, data=self._item[ItemKind.sense_coef1.value])
        write_data.append(reg)

        # 温度感度補正係数(TMPDATA >= TMPTH0)
        reg = RegData(addr=RegAddrKind.SENSTMPCOEF1.value, data=self._item[ItemKind.sense_temp_coef1.value])
        write_data.append(reg)

        # デジタル補正演算(オフセット係数)
        reg = RegData(addr=RegAddrKind.FSADJOFFSETCOEF.value, data=self._item[ItemKind.fsadj_offset_coef.value])
        write_data.append(reg)

        # デジタル補正演算(ゲイン係数)
        reg = RegData(addr=RegAddrKind.FSADJGAINCOEF.value, data=self._item[ItemKind.fsadj_gain_coef.value])
        write_data.append(reg)

        # デジタル補正演算(オフセット補正量)
        # デジタル補正演算(ゲイン設定)
        val = ((self._item[ItemKind.g2_coef.value] << 4 ) | self._item[ItemKind.offset_g2_coef.value]) & 0x0077
        reg = RegData(addr=RegAddrKind.G2COEF.value, data=val)
        write_data.append(reg)

        # PGAのゲイン設定
        reg = RegData(addr=RegAddrKind.PGACONF.value, data=self._item[ItemKind.pga_conf.value])
        write_data.append(reg)

        # PGAでのオフセット補正量
        # センサ励起電流量[mA]
        val = (self._item[ItemKind.ocal.value] & 0x00FF)
        if val < 0:
            val = 256 + val
        val = (val | (self._item[ItemKind.scal.value] << 8)) & 0x0FFF
        reg = RegData(addr=RegAddrKind.ANACAL.value, data=val)
        write_data.append(reg)

        # レジスタリフレッシュ動作
        val = self._item[ItemKind.g2_coef.value] & 0x0001
        reg = RegData(addr=RegAddrKind.DMACTRL.value, data=val)
        write_data.append(reg)

        # ID
        val = self._item[ItemKind.id.value] & 0x0003
        reg = RegData(addr=RegAddrKind.ID.value, data=val)
        write_data.append(reg)

        result = self._driver.write_reg(self._ch, RegPageKind.sensor_reg_page0.value, write_data)
        return True if result == ResultKind.ok else False

    def set_item(self, item:ItemKind, val:int):
        """ 指定した設定項目の値を変更する """
        self._item[item.value] = val

    def get_item_description(self, item:ItemKind, index) -> str:
        item_list = self.item_map.get(item)
        if isinstance(item_list[0], int):
            return f"0x{index:0{item_list[0]}X}"
        else:
            return item_list[index]

    def get_item_options(self, item: ItemKind) -> list:
        """ 設定値の選択肢を一括取得する """
        return self.item_map.get(item, ["-"])

    def get_item_value(self, item: ItemKind) -> float | int:
        """ 設定値を取得する """
        return self._item[item.value]

    def get_item_type(self, item: ItemKind) -> ItemType:
        """ 設定値の種類を取得する """
        return self.item_type.get(item, ItemType.none)

    def get_item_digit(self, item: ItemKind) -> int:
        """ 設定値の桁数を取得する """
        return self.item_digit.get(item, 1)

    def get_item_init(self, item: ItemKind) -> float:
        """ 設定値の初期値を取得する """
        return self.item_init.get(item, 0)

    def get_item_range_min(self, item: ItemKind) -> float:
        """ 設定値の最小値を取得する """
        return self.item_range.get(item, (0, 1))[0]

    def get_item_range_max(self, item: ItemKind) -> float:
        """ 設定値の最大値を取得する """
        return self.item_range.get(item, (0, 1))[1]

    def get_item_range_step(self, item: ItemKind) -> float:
        """ 設定値の刻み幅を取得する """
        return self.item_range.get(item, (0, 1))[2]

    def get_item_scale(self, item: ItemKind) -> float:
        """ 設定値のスケールファクターを取得する
            Sliderが整数しか扱えないため、小数を扱いたい場合に利用する """
        return self.item_range.get(item, (0, 1))[3]

    def get_all_value_str(self) -> list:
        """ 設定値一覧を取得する """
        values = []
        for kind in ItemKind:
            item_type = self.get_item_type(kind)
            if item_type == ItemType.dec:
                values.append(str(self.get_item_value(kind)))
            elif item_type == ItemType.hex:
                # プレフィックスは不要
                values.append(f'{self.get_item_value(kind):0{self.get_item_digit(kind)}X}')
            elif item_type == ItemType.list:
                options = self.get_item_options(kind)
                value = self.get_item_value(kind)
                values.append(options[value] if (value < len(options)) else "-")
            else:
                values.append("")
        return values

    def get_all_value_max_len(self) -> list[int]:
        """ 設定値の最大文字数を取得する """
        lengths = []
        for kind in ItemKind:
            item_type = self.get_item_type(kind)
            if item_type == ItemType.list:
                lengths.append(max(len(item) for item in self.get_item_options(kind)))
            elif item_type == ItemType.dec or item_type == ItemType.hex:
                lengths.append(self.get_item_digit(kind))
            else:
                pass
        return lengths

    def get_item_names(self) -> list[str]:
        """ 設定値のアイテム名一覧を取得する """
        return [self.item_name[kind] for kind in ItemKind]

    def get_item_name(self, item:ItemKind) -> str:
        return self.item_name.get(item, "")

