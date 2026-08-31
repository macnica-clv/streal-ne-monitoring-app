import os

from PySide6.QtCore import Signal, Property, QObject, Qt, QSize, Slot
from PySide6.QtGui import QPixmap, QColor, QPainter, QIcon
from PySide6.QtWidgets import QMainWindow

from Utils.ResourceLoader import rel_to_abs
from Views import Main_Window



_tinted_icon_cache = {}  # (path, color, w, h) -> QIcon

def tint_pixmap(src: QPixmap, color: QColor) -> QPixmap:
    if src.isNull():
        return src
    tinted = QPixmap(src.size())
    tinted.fill(Qt.transparent)

    p = QPainter(tinted)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setRenderHint(QPainter.SmoothPixmapTransform, True)
    p.drawPixmap(0, 0, src)
    p.setCompositionMode(QPainter.CompositionMode_SourceIn)
    p.fillRect(tinted.rect(), color)
    p.end()
    return tinted

def tinted_qicon(qrc_path: str, color_hex: str, size: QSize) -> QIcon:
    key = (qrc_path, color_hex, size.width(), size.height())
    if key in _tinted_icon_cache:
        return _tinted_icon_cache[key]

    src = QPixmap(qrc_path)
    if not src.isNull() and (src.size() != size):
        src = src.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    icon = QIcon(tint_pixmap(src, QColor(color_hex)))
    _tinted_icon_cache[key] = icon
    return icon


class SensorStatus(QObject):
    themeUpdated = Signal()
    statusUpdated = Signal()

    def __init__(self):
        super().__init__()
        self._theme: int = 0
        self._sensor_statuses: list[int] = []

    @Property(int, notify=themeUpdated)
    def theme(self):
        return self._theme
    @Property(list, notify=statusUpdated)
    def sensor_status(self):
        return self._sensor_statuses

    def update_theme(self, theme: int):
        self._theme = theme
        self.themeUpdated.emit()

    def update_sensor_status(self, statuses: list[int]):
        self._sensor_statuses = statuses
        self.statusUpdated.emit()


class MainWindow(QMainWindow):
    closing_application = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Main_Window.Ui_main_window()
        self.ui.setupUi(self)
        self.reset_stylesheet()

        icon_path = rel_to_abs(os.path.join("Views", "icon", "app.png"))
        self.setWindowIcon(QIcon(icon_path))

        self.status_bridge = SensorStatus()
        self.ui.sensor_status.rootContext().setContextProperty("bridge", self.status_bridge)

    # 親要素のStyleSheetを引き継ぐため、子要素のStyleSheetを削除する
    def reset_stylesheet(self):
        self.ui.toolbar.setStyleSheet("")
        self.ui.home_button.setStyleSheet("")
        self.ui.label.setStyleSheet("")
        self.ui.chart_button.setStyleSheet("")
        self.ui.label_2.setStyleSheet("")
        self.ui.manual_button.setStyleSheet("")
        self.ui.label_3.setStyleSheet("")
        self.ui.setting_button.setStyleSheet("")
        self.ui.status_bar.setStyleSheet("")

    def add_page(self, page):
        self.ui.page_layout.addWidget(page)

    def closeEvent(self, event):
        self.closing_application.emit()


    def apply_theme_icons(self, theme_index: int):
        # ここは「theme_index -> 色」へ変換
        #テーマ定義に合わせて変更
        if theme_index == 0:      # Normal
            icon_color = "#2D3282"
        elif theme_index == 1:    # Light
            icon_color = "#21272A"
        else:                     # Dark
            icon_color = "#FFFFFF"

        self.ui.home_button.setIcon(
            tinted_qicon(":/ToolBar/Images/ToolBar/Home.png", icon_color, QSize(26, 32))
        )
        self.ui.chart_button.setIcon(
            tinted_qicon(":/ToolBar/Images/ToolBar/wave-saw-tool.png", icon_color, QSize(26, 32))
        )
        self.ui.manual_button.setIcon(
            tinted_qicon(":/ToolBar/Images/ToolBar/book.png", icon_color, QSize(26, 32))
        )
        self.ui.setting_button.setIcon(
            tinted_qicon(":/ToolBar/Images/ToolBar/gear-fill.png", icon_color, QSize(23, 26))
        )
        for label in (self.ui.label, self.ui.label_2, self.ui.label_3):
            label.setStyleSheet(f"color: {icon_color};")


class DummyAppBridge(QObject):
    themeChanged = Signal()

    def __init__(self, initial_theme: int = 0, parent: QObject | None = None):
        super().__init__(parent)
        self._theme = int(initial_theme)

    @Property(int, notify=themeChanged)
    def theme(self) -> int:
        return self._theme

    @Slot(int)
    def update_theme(self, theme: int) -> None:
        theme = int(theme)
        if self._theme != theme:
            self._theme = theme
            self.themeChanged.emit()
