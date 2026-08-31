import os

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from Models.Preset import Preset, PresetKey
from Models.Hizmil_Driver import HizmilDriver
from Models.Register_Item_SR300 import RegisterItemSR300, ItemKind
from Utils.ResourceLoader import rel_to_abs
from Views.RegisterViewSR300 import RegisterPageSR300, ComboboxData, SliderData
from Models.Register_Item_SR300 import RegisterItemSR300, ItemKind

class SensorRegister:
    def __init__(self, register, preset_path):
        self._register = register
        self._preset_path = preset_path
        self.combobox_indexes = [ ItemKind.gain, ItemKind.id, ItemKind.ads,
                                  ItemKind.st_range, ItemKind.tsdis0, ItemKind.tsdis1,
                                  ItemKind.tsmod, ItemKind.drvsel, ItemKind.tofs]
        self.slider_indexes = [ ItemKind.sg, ItemKind.dofs ]

    def get_slider_data(self):
        slider_data : list[SliderData] = []
        for index in self.slider_indexes:
            data_min = self._register.get_item_range_min(index)
            data_max = self._register.get_item_range_max(index)
            data_step = self._register.get_item_range_step(index)
            data_digit = self._register.get_item_digit(index)
            data_init = self._register.get_item_init(index)
            data_value = self._register.get_item_value(index)
            slider_data.append(SliderData(index, data_min, data_max, data_step, data_digit, data_init, data_value))
        return slider_data

    def get_combobox_data(self):
        combobox_data : list[ComboboxData] = []
        for index in self.combobox_indexes:
            options = self._register.get_item_options(index)
            data_init = self._register.get_item_init(index)
            data_value = self._register.get_item_value(index)
            combobox_data.append(ComboboxData(index, options, data_init, data_value))
        return combobox_data

    def read_register(self):
        self._register.read_item()

    def write_register(self, index, value):
        self._register.set_item(index, int(value))

    def save_register(self):
        self._register.write_item()

    def load_preset(self, preset_name: str) -> tuple[list[SliderData], list[ComboboxData]]:
        preset = Preset(self._preset_path)

        slider_data: list[SliderData] = self.get_slider_data()
        targets = [PresetKey(name=self._register.get_item_name(data.id), value=self._register.get_item_init(data.id), val_type=int) for data in slider_data]
        preset.load(preset_name, targets)
        for i, target in enumerate(targets):
            slider_data[i].value = target.value

        combobox_data : list[ComboboxData] = self.get_combobox_data()
        targets = [PresetKey(name=self._register.get_item_name(data.id), value=self._register.get_item_init(data.id), val_type=int) for data in combobox_data]
        preset.load(preset_name, targets)
        for i, target in enumerate(targets):
            combobox_data[i].index = target.value

        return slider_data, combobox_data

    def save_preset(self, preset_name: str, indexes: list, values: list):
        targets = []
        for index, value in zip(indexes, values):
            targets.append(PresetKey(name=self._register.get_item_name(index), value=value, val_type=int))
        preset = Preset(self._preset_path)
        preset.save(preset_name, targets)

class RegisterControllerSR300:
    def __init__(self, parent=None):
        self.register_page = RegisterPageSR300(parent=parent)
        self._driver: HizmilDriver = HizmilDriver()
        self._register: list[SensorRegister] = []
        self._sensor_channel = 0
        self._preset_channel = 0
        self.preset_path = rel_to_abs("preset.ini")

        self.register_page.ui.load_button.clicked.connect(self.load_preset)
        self.register_page.ui.save_button.clicked.connect(self.save_preset)
        self.register_page.ui.read_button.clicked.connect(self.load_register)
        self.register_page.ui.write_button.clicked.connect(self.save_register)
        self.register_page.ui.help_button_sr300.clicked.connect(self.open_datasheet)
        self.register_page.setRomRequested.connect(self.apply)
        self.register_page.channelChanged.connect(self.change_channel)
        self.register_page.presetChanged.connect(self.change_preset)

        self.register_page.comboboxItemChanged.connect(self.on_combobox_item_changed)


    def on_combobox_item_changed(self, item_id, index: int):
        # item_id は ItemKind が入ってくる想定（ComboboxData.id）
        if item_id != ItemKind.st_range:
            return
        reg = self._register[self._sensor_channel]._register
        reg.set_item(ItemKind.st_range, int(index))
        new_options = reg.get_item_options(ItemKind.tofs)

        current_tofs = reg.get_item_value(ItemKind.tofs)
        if current_tofs >= len(new_options):
            current_tofs = 0
            reg.set_item(ItemKind.tofs, 0)

        # 4) UI の tofs コンボボックスだけ更新
        init_tofs = reg.get_item_init(ItemKind.tofs)
        self.register_page.update_combobox_options(ItemKind.tofs, new_options, int(current_tofs), int(init_tofs))

    def set_driver(self, driver: HizmilDriver):
        self._driver = driver
        self._register = [SensorRegister(RegisterItemSR300(driver, ch), self.preset_path) for ch in range(driver.ch_max)]

    def show(self):
        if len(self._register) < 1:
            print("Register isn't ready.")
            return
        # 表示する直前に最新の値を取ってくる
        self.change_channel(0)
        self.register_page.set_channel(0)
        self.register_page.setVisible(True)

    def hide(self):
        self.register_page.setVisible(False)

    def change_channel(self, sensor_channel):
        self._sensor_channel = sensor_channel
        self.load_register()

    def change_preset(self, preset_channel):
        self._preset_channel = preset_channel

    def load_register(self):
        # レジスタを読み込んだらUIに反映する
        self._register[self._sensor_channel].read_register()
        self.register_page.set_slider_data(self._register[self._sensor_channel].get_slider_data())
        self.register_page.set_combobox_data(self._register[self._sensor_channel].get_combobox_data())

    def save_register(self):
        for data in self.register_page.get_slider_data():
            self._register[self._sensor_channel].write_register(data.id, data.value)
        for data in self.register_page.get_combobox_data():
            self._register[self._sensor_channel].write_register(data.id, data.index)

        self._register[self._sensor_channel].save_register()
        self._driver.init_status(self._sensor_channel)

    def open_datasheet(self):
        url = QUrl("https://go.macnica.co.jp/Entry-CLV-DL-STRL-20251118-SR300series-Datasheet.html")
        QDesktopServices.openUrl(url)

    # TBD：SR300対応時、SR300用のキー文字列に差し替える
    def load_preset(self):
        slider_data, combobox_data = self._register[self._sensor_channel].load_preset(f"SR300_{self._preset_channel}")
        self.register_page.set_slider_data(slider_data)
        self.register_page.set_combobox_data(combobox_data)

    def save_preset(self):
        indexes, values = [], []
        for data in self.register_page.get_slider_data():
            indexes.append(data.id)
            values.append(data.value)
        for data in self.register_page.get_combobox_data():
            indexes.append(data.id)
            values.append(data.index)
        self._register[self._sensor_channel].save_preset(f"SR300_{self._preset_channel}", indexes, values)

    def apply(self):
        result = self._driver.set_rom(self._sensor_channel)
        print(result)

    def update_language(self):
        self.register_page.ui.retranslateUi(self.register_page)
        if len(self._register) > 0:
            # コンボボックスを再生成
            self._register = [SensorRegister(RegisterItemSR300(self._driver, ch), self.preset_path) for ch in
                              range(self._driver.ch_max)]
            self.load_register()

    def apply_theme(self, theme: int):
        self.register_page.apply_theme(theme)