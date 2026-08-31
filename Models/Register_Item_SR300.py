from enum import Enum

from PySide6.QtCore import QCoreApplication

from Models.Hizmil_Driver import HizmilDriver, ResultKind
from Models.SensorSR300 import RegAddrKindSR300, RegData, RegPageKind

TOFS_BIT_MAP = {
    0: 0b0111,
    1: 0b0110,
    2: 0b0101,
    3: 0b0100,
    4: 0b0011,
    5: 0b0010,
    6: 0b0001,
    7: 0b0000,
    8: 0b1111,
    9: 0b1110,
    10: 0b1101,
    11: 0b1100,
    12: 0b1011,
    13: 0b1010,
    14: 0b1001,
}
BIT_TO_INDEX_MAP = {v: k for k, v in TOFS_BIT_MAP.items()}

class ItemType(Enum):
    dec = 0
    hex = 1
    list = 2
    none = 3


class ItemKind(Enum):
    gain = 0
    sg = 1
    dofs = 2
    id = 3
    ads = 4
    st_range = 5
    tsdis0 = 6
    tsdis1 = 7
    tsmod = 8
    drvsel = 9
    tofs = 10
    item_num = 11

class RegisterItemSR300:
    """ 画面上のレジスタ設定を管理するクラス
        画面上の設定項目とSR500のレジスタは1対1にはなっていないため、このクラスにて吸収する
        コンボボックスで選択する設定項目については、インデックス番号でやりとりすること """

    item_name = {
        ItemKind.gain: "gain",
        ItemKind.sg: "sg",
        ItemKind.dofs: "dofs",
        ItemKind.id: "id",
        ItemKind.ads: "ads",
        ItemKind.st_range: "st_range",
        ItemKind.tsdis0: "tsdis0",
        ItemKind.tsdis1: "tsdis1",
        ItemKind.tsmod: "tsmod",
        ItemKind.drvsel: "drvsel",
        ItemKind.tofs: "tofs",
        ItemKind.item_num: ""
    }

    item_init = {
        ItemKind.gain: 0,
        ItemKind.sg: 0,
        ItemKind.dofs: 0,
        ItemKind.id: 0,
        ItemKind.ads: 0,
        ItemKind.st_range: 0,
        ItemKind.tsdis0: 0,
        ItemKind.tsdis1: 0,
        ItemKind.tsmod: 0,
        ItemKind.drvsel: 0,
        ItemKind.tofs: 7,
    }

    item_type: dict[ItemKind, ItemType] = {
        ItemKind.gain: ItemType.list,
        ItemKind.sg: ItemType.dec,
        ItemKind.dofs: ItemType.dec,
        ItemKind.id: ItemType.list,
        ItemKind.ads: ItemType.list,
        ItemKind.st_range: ItemType.list,
        ItemKind.tsdis0: ItemType.list,
        ItemKind.tsdis1: ItemType.list,
        ItemKind.tsmod: ItemType.list,
        ItemKind.drvsel: ItemType.list,
        ItemKind.tofs: ItemType.list,
        ItemKind.item_num: ItemType.none,
    }

    item_digit: dict[ItemKind, int] = {
        ItemKind.sg: 1,
        ItemKind.dofs: 1,
    }

    # UI: sg=-125..124（= -12.5..12.4%）
    # UI: dofs=-635..635（= -63.5..63.5mV）
    item_range: dict[ItemKind, tuple[int, int, int]] = {
        ItemKind.sg: (-125, 124, 1),
        ItemKind.dofs: (-1270, 1270, 10),
    }


    def __init__(self, driver : HizmilDriver, ch:int):
        self._driver = driver
        self._ch = ch
        self._item = []
        for i in range(ItemKind.item_num.value):
            self._item.append(0)
        self.update_item_map()

    def update_item_map(self):
        st_range_val = self._item[ItemKind.st_range.value]
        if st_range_val == 0:
            tofs_list = [
                "4.0",
                "2.0",
                "1.0",
                "0.5",
                "0.25",
                "0.125",
                "0.0625",
                "0.0",
                "-0.0625",
                "-0.125",
                "-0.25",
                "-0.5",
                "-1.0",
                "-2.0",
                "-4.0"
            ]
        elif st_range_val == 1:
            tofs_list = [
                "8.0",
                "4.0",
                "2.0",
                "1.0",
                "0.5",
                "0.25",
                "0.125",
                "0.0",
                "-0.125",
                "-0.25",
                "-0.5",
                "-1.0",
                "-2.0",
                "-4.0",
                "-8.0"
            ]
        else:
            tofs_list = [
                "4.0",
                "2.0",
                "1.0",
                "0.5",
                "0.25",
                "0.125",
                "0.0625",
                "0.0",
                "-0.0625",
                "-0.125",
                "-0.25",
                "-0.5",
                "-1.0",
                "-2.0",
                "-4.0"
            ]

        self.item_map = {
            ItemKind.gain: [
                "8.0",
                "15.8",
                "31.4",
                "65.1",
                "120",
                "248",
                "504",
                "1016"
            ],
            ItemKind.id: [
                "0",
                "1",
                "2",
                "3"
            ],
            ItemKind.ads: [
                "1.25KHz",
                "2.5KHz",
                "5.0KHz",
                "10.0KHz"
            ],
            ItemKind.st_range: [
                QCoreApplication.translate("RegisterItemSR300","about 1uε"),
                QCoreApplication.translate("RegisterItemSR300","about 0.5uε")
            ],
            ItemKind.tsdis0: [
                QCoreApplication.translate("RegisterItemSR300","Digital Output Enabled"),
                QCoreApplication.translate("RegisterItemSR300","Digital Output Disabled")
            ],
            ItemKind.tsdis1: [
                QCoreApplication.translate("RegisterItemSR300","Analog Output Enabled"),
                QCoreApplication.translate("RegisterItemSR300", "Analog Output Disabled")
            ],
            #ItemKind.ocal: [str(i) for i in range(127, -128, -1)] + ["0(-128)"],
            ItemKind.tsmod: [
                "1℃",
                "0.0625℃"
            ],
            ItemKind.drvsel: [
                QCoreApplication.translate("RegisterItemSR300","Output Current ±30μA"),
                QCoreApplication.translate("RegisterItemSR300","Output Current ±2mA")
            ],
            ItemKind.tofs: tofs_list,

        }
        if self._item[ItemKind.tofs.value] >= len(tofs_list):
            self._item[ItemKind.tofs.value] = 0

    def read_item(self) -> list[int]:
        """ 現在のレジスタ値を取得して設定値に反映する """
        board, board_ch = self._driver.get_board_ch(self._ch)
        reg_data = self._driver.board[board.value].sensor[board_ch].reg_data[0]

        # アンプ倍率
        val = reg_data[RegAddrKindSR300.GAIN.value] & 0x0007
        self._item[ItemKind.gain.value] = val

        # ブリッジ電流調整
        val = reg_data[RegAddrKindSR300.SG.value] & 0x00FF
        # 2の補数 → signed
        if val >= 128:
            val -= 256
        # スケーリング戻し
        val = int(round(val * 124 / 127))
        self._item[ItemKind.sg.value] = val

        # オフセット調整
        val = reg_data[RegAddrKindSR300.DOFS.value] & 0x00FF
        # unsigned → signed
        if val >= 128:
            val -= 256
        val = int(round(val * 1270 / 127))
        self._item[ItemKind.dofs.value] = val

        # ID
        val = reg_data[RegAddrKindSR300.ID.value] & 0x0003
        self._item[ItemKind.id.value] = val

        # サンプリング周波数
        val = reg_data[RegAddrKindSR300.TE_AD.value] & 0x0003
        self._item[ItemKind.ads.value] = val

        # ひずみ量測定範囲
        val = (reg_data[RegAddrKindSR300.TE_AD.value] >> 2) & 0x0001
        self._item[ItemKind.st_range.value] = val

        # 温度センサ出力設定デジタル
        val = (reg_data[RegAddrKindSR300.TE_AD.value] >> 4) & 0x0001
        self._item[ItemKind.tsdis0.value] = val

        # 温度センサ出力設定アナログ
        val = (reg_data[RegAddrKindSR300.TE_AD.value] >> 5) & 0x0001
        self._item[ItemKind.tsdis1.value] = val

        # 温度分解能設定
        val = (reg_data[RegAddrKindSR300.TE_AD.value] >> 6) & 0x0001
        self._item[ItemKind.tsmod.value] = val

        # 出力ドライバ設定
        val = reg_data[RegAddrKindSR300.DRV.value] & 0x0001
        self._item[ItemKind.drvsel.value] = val

        # オフセット温度補正
        val = reg_data[RegAddrKindSR300.TOFS.value] & 0x000F
        index = BIT_TO_INDEX_MAP.get(val, 0)
        self._item[ItemKind.tofs.value] = index

        self.update_item_map()
        return self._item

    def write_item(self) -> bool:
        """ 現在の設定値をレジスタに書き込む """

        board, board_ch = self._driver.get_board_ch(self._ch)
        reg_data = self._driver.board[board.value].sensor[board_ch].reg_data
        write_data : list[RegData] = []

        #アンプ倍率
        val = self._item[ItemKind.gain.value] & 0x0007
        reg = RegData(addr=RegAddrKindSR300.GAIN.value, data=val)
        write_data.append(reg)

        # ブリッジ電流調整
        val = int(round(self._item[ItemKind.sg.value] * 127 / 124))
        val = max(-128, min(127, val))
        # 2の補数変換
        if val < 0:
            val = 256 + val
        val &= 0x00FF
        reg = RegData(addr=RegAddrKindSR300.SG.value, data=val)
        write_data.append(reg)

        # オフセット調整
        val = int(round(self._item[ItemKind.dofs.value] * 127 / 1270))
        val = max(-128, min(127, val))
        # 2の補数変換
        if val < 0:
            val = 256 + val
        val &= 0x00FF
        reg = RegData(addr=RegAddrKindSR300.DOFS.value, data=val)
        write_data.append(reg)

        # ID
        val = self._item[ItemKind.id.value] & 0x0003
        reg = RegData(addr=RegAddrKindSR300.ID.value, data=val)
        write_data.append(reg)

        # ADS
        # ひずみ量測定範囲
        # 温度センサ出力設定デジタル
        # 温度センサ出力設定アナログ
        # 温度分解能設定
        val = (self._item[ItemKind.tsmod.value] << 6) |  (self._item[ItemKind.tsdis1.value] << 5) | (self._item[ItemKind.tsdis0.value] << 4) | (self._item[ItemKind.st_range.value] << 2) | self._item[ItemKind.ads.value] & 0x0003
        reg = RegData(addr=RegAddrKindSR300.TE_AD.value, data=val)
        write_data.append(reg)

        # 出力ドライバ設定
        val = self._item[ItemKind.drvsel.value] & 0x0001
        reg = RegData(addr=RegAddrKindSR300.DRV.value, data=val)
        write_data.append(reg)

        # オフセット温度補正
        index = self._item[ItemKind.tofs.value] & 0x000F
        val = TOFS_BIT_MAP.get(index, 0)
        reg = RegData(addr=RegAddrKindSR300.TOFS.value, data=val)
        write_data.append(reg)

        result = self._driver.write_reg(self._ch, RegPageKind.sensor_reg_page0.value, write_data)
        return True if result == ResultKind.ok else False

    def set_item(self, item:ItemKind, val:int):
        """ 指定した設定項目の値を変更する """
        self._item[item.value] = val
        if item == ItemKind.st_range:
            self.update_item_map()

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

