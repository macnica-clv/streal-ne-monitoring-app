from PySide6 import QtCore
from PySide6.QtCore import Slot, Property, Signal, QObject, QEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QMessageBox, QSlider, QSpinBox, QComboBox

from Utils.MessageBox import ConfirmDialog
from Views.MainView import tinted_qicon
from Views.UI import Register_Page_SR300


class SliderData:
    def __init__(self, item_id, data_min, data_max, step, digit, init, value):
        self.id = item_id
        self.min = data_min
        self.max = data_max
        self.step = step
        self.digit = digit
        self.init = init
        self.value = value
        self.print()

    def set_value(self, value):
        if self.min <= value <= self.max:
            self.value = value

    def reset_value(self):
        self.value = self.init

    def print(self):
        print(f"id = {self.id}, min = {self.min}, max = {self.max}, step = {self.step}, value = {self.value}")


class ComboboxData:
    def __init__(self, item_id, options: list[str], init: int, index: int):
        self.id = item_id
        self.options = options
        self.init = init
        self.index = index
        self.print()

    def set_value(self, value):
        self.index = value

    def reset_value(self):
        self.index = self.init

    def print(self):
        print(f"id = {self.id}, index = {self.index}, list = {self.options}")


class RegisterSettings(QObject):
    sliderUpdated = Signal()
    comboboxUpdated = Signal()

    def __init__(self, parent=None):
        super(RegisterSettings, self).__init__(parent)
        self._combobox_data : list[ComboboxData] = []
        self._slider_data : list[SliderData] = []

    def set_slider_data(self, slider_data: list[SliderData]):
        self._slider_data = slider_data
        self.sliderUpdated.emit()

    def set_combobox_data(self, combobox_data: list[ComboboxData]):
        self._combobox_data = combobox_data
        self.comboboxUpdated.emit()

    @Property(list, notify=sliderUpdated)
    def slider_data(self):
        return self._slider_data

    @Property(list, notify=comboboxUpdated)
    def combobox_data(self):
        return self._combobox_data

    @Slot(int, float)
    def update_slider(self, index, value):
        self._slider_data[index].set_value(value)
        self.sliderUpdated.emit()

    @Slot(int, int)
    def update_combobox(self, index, value):
        self._combobox_data[index].set_value(value)
        self.comboboxUpdated.emit()

    def reset_settings(self):
        for data in self._slider_data:
            data.reset_value()
            data.print()
        self.sliderUpdated.emit()

        for data in self._combobox_data:
            data.reset_value()
            data.print()
        self.comboboxUpdated.emit()


class SliderSetting(QObject):
    def __init__(self, min_tb: QLabel, max_tb: QLabel, slider: QSlider, spinbox: QSpinBox, is_hex=True):
        super(SliderSetting, self).__init__()
        self._data = None
        self.init = 0
        self.min_tb = min_tb
        self.max_tb = max_tb
        self.slider = slider
        self.sb = spinbox
        self.is_hex = is_hex
        self.slider.valueChanged.connect(self.validate_slider)
        self.sb.valueChanged.connect(self.validate_spinbox)

    def set_data(self, data: SliderData):
        self._data = data
        self.init = data.init
        if self.is_hex:
            self.min_tb.setText(f'{data.min:0X}')
            self.max_tb.setText(f'{data.max:0{data.digit}X}')
        else:
            self.min_tb.setText(str(data.min))
            self.max_tb.setText(str(data.max))

        # 誤操作を防ぐため、マウスホイールによる操作は無効にする
        self.slider.setRange(data.min, data.max)
        self.slider.setSingleStep(data.step)
        self.slider.installEventFilter(self)

        self.sb.setRange(data.min, data.max)
        self.sb.setSingleStep(data.step)
        if self.is_hex:
            self.sb.setDisplayIntegerBase(16)
        self.sb.installEventFilter(self)

        self.slider.setValue(data.value)
        self.sb.setValue(data.value)

    def init_data(self):
        self.slider.setValue(self.init)
        self.sb.setValue(self.init)

    def get_data(self):
        return self._data

    def validate_slider(self):
        raw = self.slider.value()

        # dofsだけ（step=10のとき）
        if self._data.step == 10:
            step = self._data.step
            snapped = round(raw / step) * step

            if snapped != raw:
                self.slider.blockSignals(True)
                self.slider.setValue(snapped)
                self.slider.blockSignals(False)

            val = snapped
        else:
            val = raw

        self._data.set_value(val)
        self.sb.setValue(val)

    def validate_spinbox(self):
        raw = self.sb.value()

        # dofsなど「step=10」の項目だけスナップ
        if self._data.step == 10:
            step = self._data.step
            snapped = round(raw / step) * step
            val = snapped

            # 値がズレていた場合のみ補正（無限ループ防止）
            if snapped != raw:
                self.sb.blockSignals(True)
                self.sb.setValue(snapped)
                self.sb.blockSignals(False)
        else:
            val = raw

        # データ反映
        self._data.set_value(val)

        # sliderと同期
        if self.slider.value() != val:
            self.slider.setValue(val)

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Type.Wheel:
            return True
        return False


class ComboboxSetting(QObject):
    indexChanged = Signal(object, int)  # (item_id, index)

    def __init__(self, cb: QComboBox):
        super(ComboboxSetting, self).__init__()
        self._data = None
        self.init = 0
        self.cb = cb
        self.cb.activated.connect(self.change_index)
        self.cb.installEventFilter(self)

    def set_data(self, data: ComboboxData):
        self._data = data
        self.init = data.init
        self.cb.clear()
        self.cb.addItems(data.options)
        self.cb.setCurrentIndex(data.index)

    def init_data(self):
        self.cb.setCurrentIndex(self.init)

    def get_data(self):
        return self._data

    def change_index(self):
        if self._data is None:
            return
        self._data.index = self.cb.currentIndex()
        self.indexChanged.emit(self._data.id, self._data.index)

    def eventFilter(self, obj, event) -> bool:
            if event.type() == QEvent.Type.Wheel:
                return True
            return False


class RegisterPageSR300(QMainWindow):
    setRomRequested = Signal()
    channelChanged = Signal(int)
    presetChanged = Signal(int)
    comboboxItemChanged = Signal(object, int)  # (item_id, index) 追加

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Register_Page_SR300.Ui_register_page()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowContextHelpButtonHint | self.windowFlags())

        self.sliders: list[SliderSetting] = []
        self.sliders.append(SliderSetting(self.ui.sg_min, self.ui.sg_max, self.ui.sg_slider, self.ui.sg_spin, is_hex=False))
        self.sliders.append(SliderSetting(self.ui.dofs_min, self.ui.dofs_max, self.ui.dofs_slider, self.ui.dofs_max_2, is_hex=False))

        self.combo_boxes: list[ComboboxSetting] = []
        self.combo_boxes.append(ComboboxSetting(self.ui.gain_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.sensor_id_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.ads_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.st_range_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.tsdis0_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.tsdis1_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.tsmod_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.drvsel_select))
        self.combo_boxes.append(ComboboxSetting(self.ui.tofs_select))

        for cb in self.combo_boxes:
            cb.indexChanged.connect(self.comboboxItemChanged)

        self.ui.ch_select.activated.connect(lambda: self.channelChanged.emit(self.ui.ch_select.currentIndex()))
        self.ui.preset_select.activated.connect(lambda: self.presetChanged.emit(self.ui.preset_select.currentIndex()))

        self.ui.reset_button.clicked.connect(self.init_settings)
        self.ui.apply_button.clicked.connect(self.apply)

    def update_combobox_options(self, target_item_id, options: list[str], index: int, init: int):
        for cb in self.combo_boxes:
            data = cb.get_data()
            if data is None:
                continue
            if data.id == target_item_id:
                data.options = options
                data.index = index
                data.init = init
                cb.set_data(data)
                break

    def init_settings(self):
        for slider in self.sliders:
            slider.init_data()
        for combobox in self.combo_boxes:
            combobox.init_data()

    def set_channel(self, channel: int):
        self.ui.ch_select.setCurrentIndex(channel)

    def set_slider_data(self, slider_data: list[SliderData]):
        for slider, data in zip(self.sliders, slider_data):
            slider.set_data(data)

    def set_combobox_data(self, combobox_data: list[ComboboxData]):
        for combobox, data in zip(self.combo_boxes, combobox_data):
            combobox.cb.clear()
            combobox.set_data(data)

    def get_slider_data(self) -> list[SliderData]:
        return [slider.get_data() for slider in self.sliders]

    def get_combobox_data(self) -> list[ComboboxData]:
        return [combobox.get_data() for combobox in self.combo_boxes]

    def apply(self):
        title = self.tr("Confirm")
        body = self.tr("This will modify the registers.\nAre you sure you want to continue?")
        dialog = ConfirmDialog(title, body)
        ret = dialog.exec_()
        if ret == QMessageBox.StandardButton.Ok:
            self.setRomRequested.emit()


    def apply_theme(self, theme: int):
        # theme値の定義は MainController.load_theme の分岐に合わせる（2がDarkなど）
        if theme == 2:      # Dark
            color = "#FFFFFF"
        else:               # Light / Normal
            color = "#2A2D35"  # 例：暗色（お好みで）

        self.ui.help_button_sr300.setIcon(
            tinted_qicon(
                ":/RegisterPages/Images/Pages/RegisterPage/help-circle-sharp.png",
                color,
                self.ui.help_button_sr300.iconSize()
            )
        )
