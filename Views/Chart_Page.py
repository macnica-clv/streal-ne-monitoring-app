# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Chart_Page.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_chart_page(object):
    def setupUi(self, chart_page):
        if not chart_page.objectName():
            chart_page.setObjectName(u"chart_page")
        chart_page.resize(1396, 838)
        chart_page.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.page_layout = QGridLayout(chart_page)
        self.page_layout.setSpacing(0)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.measurement_area = QWidget(chart_page)
        self.measurement_area.setObjectName(u"measurement_area")
        self.verticalLayout_3 = QVBoxLayout(self.measurement_area)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.measurement_area)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(2)
        self.splitter.setChildrenCollapsible(False)
        self.chart_area = QWidget(self.splitter)
        self.chart_area.setObjectName(u"chart_area")
        self.chart_area.setMinimumSize(QSize(0, 200))
        self.chart_area.setStyleSheet(u"background-color: rgb(200, 200, 150);")
        self.splitter.addWidget(self.chart_area)
        self.table_area = QWidget(self.splitter)
        self.table_area.setObjectName(u"table_area")
        self.table_area.setMinimumSize(QSize(0, 200))
        self.table_area.setStyleSheet(u"background-color: rgb(200, 150, 150);")
        self.verticalLayout_2 = QVBoxLayout(self.table_area)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.table_header = QWidget(self.table_area)
        self.table_header.setObjectName(u"table_header")
        self.table_header.setMinimumSize(QSize(0, 30))
        self.table_header.setMaximumSize(QSize(16777215, 30))
        self.table_header.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.table_header)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.table_title = QLabel(self.table_header)
        self.table_title.setObjectName(u"table_title")
        self.table_title.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.table_title)

        self.header_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.header_spacer)

        self.table_setting_button = QPushButton(self.table_header)
        self.table_setting_button.setObjectName(u"table_setting_button")
        self.table_setting_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon = QIcon()
        icon.addFile(u":/ChartPages/Images/Pages/ChartPage/table-options.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.table_setting_button.setIcon(icon)
        self.table_setting_button.setIconSize(QSize(20, 20))
        self.table_setting_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.table_setting_button)


        self.verticalLayout_2.addWidget(self.table_header)

        self.sensor_info = QTableWidget(self.table_area)
        if (self.sensor_info.columnCount() < 7):
            self.sensor_info.setColumnCount(7)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.NoBrush)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setForeground(brush);
        self.sensor_info.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.sensor_info.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.sensor_info.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.sensor_info.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.sensor_info.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.sensor_info.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.sensor_info.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        if (self.sensor_info.rowCount() < 4):
            self.sensor_info.setRowCount(4)
        self.sensor_info.setObjectName(u"sensor_info")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensor_info.sizePolicy().hasHeightForWidth())
        self.sensor_info.setSizePolicy(sizePolicy)
        self.sensor_info.setMinimumSize(QSize(0, 1))
        palette = QPalette()
        brush1 = QBrush(QColor(52, 58, 63, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        brush2 = QBrush(QColor(200, 150, 150, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush2)
        brush3 = QBrush(QColor(255, 255, 255, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, brush3)
        brush4 = QBrush(QColor(52, 58, 63, 128))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush4)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush4)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush4)
#endif
        self.sensor_info.setPalette(palette)
        self.sensor_info.setStyleSheet(u"")
        self.sensor_info.setAutoScrollMargin(7)
        self.sensor_info.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.sensor_info.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.sensor_info.setRowCount(4)
        self.sensor_info.setColumnCount(7)
        self.sensor_info.horizontalHeader().setMinimumSectionSize(23)
        self.sensor_info.horizontalHeader().setDefaultSectionSize(109)
        self.sensor_info.horizontalHeader().setStretchLastSection(True)
        self.sensor_info.verticalHeader().setVisible(False)
        self.sensor_info.verticalHeader().setMinimumSectionSize(24)
        self.sensor_info.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout_2.addWidget(self.sensor_info)

        self.splitter.addWidget(self.table_area)

        self.verticalLayout_3.addWidget(self.splitter)


        self.page_layout.addWidget(self.measurement_area, 2, 1, 1, 1)

        self.sub_menu = QWidget(chart_page)
        self.sub_menu.setObjectName(u"sub_menu")
        self.sub_menu.setMinimumSize(QSize(0, 40))
        self.sub_menu.setMaximumSize(QSize(16777215, 40))
        self.sub_menu.setStyleSheet(u"background-color: rgb(150, 150, 200);")
        self.horizontalLayout = QHBoxLayout(self.sub_menu)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 2, 7, 2)
        self.open_button = QPushButton(self.sub_menu)
        self.open_button.setObjectName(u"open_button")
        self.open_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon1 = QIcon()
        icon1.addFile(u":/ChartPages/Images/Pages/ChartPage/add-folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_button.setIcon(icon1)
        self.open_button.setIconSize(QSize(20, 20))
        self.open_button.setFlat(True)

        self.horizontalLayout.addWidget(self.open_button)

        self.sub_line1 = QFrame(self.sub_menu)
        self.sub_line1.setObjectName(u"sub_line1")
        self.sub_line1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.sub_line1.setFrameShape(QFrame.Shape.VLine)
        self.sub_line1.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.sub_line1)

        self.x_zoom_area = QWidget(self.sub_menu)
        self.x_zoom_area.setObjectName(u"x_zoom_area")
        self.x_zoom_area.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        self.gridLayout_2 = QGridLayout(self.x_zoom_area)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.x_zoom_in_button = QPushButton(self.x_zoom_area)
        self.x_zoom_in_button.setObjectName(u"x_zoom_in_button")
        icon2 = QIcon()
        icon2.addFile(u":/ChartPages/Images/Pages/ChartPage/zoom-in.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.x_zoom_in_button.setIcon(icon2)

        self.gridLayout_2.addWidget(self.x_zoom_in_button, 1, 0, 1, 1)

        self.x_zoom_out_button = QPushButton(self.x_zoom_area)
        self.x_zoom_out_button.setObjectName(u"x_zoom_out_button")
        icon3 = QIcon()
        icon3.addFile(u":/ChartPages/Images/Pages/ChartPage/zoom-out.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.x_zoom_out_button.setIcon(icon3)

        self.gridLayout_2.addWidget(self.x_zoom_out_button, 1, 1, 1, 1)

        self.x_zoom_label = QLabel(self.x_zoom_area)
        self.x_zoom_label.setObjectName(u"x_zoom_label")
        self.x_zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.x_zoom_label, 0, 0, 1, 2)


        self.horizontalLayout.addWidget(self.x_zoom_area)

        self.strain_zoom_area = QWidget(self.sub_menu)
        self.strain_zoom_area.setObjectName(u"strain_zoom_area")
        self.strain_zoom_area.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        self.gridLayout_3 = QGridLayout(self.strain_zoom_area)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.strain_zoom_in_button = QPushButton(self.strain_zoom_area)
        self.strain_zoom_in_button.setObjectName(u"strain_zoom_in_button")
        self.strain_zoom_in_button.setIcon(icon2)

        self.gridLayout_3.addWidget(self.strain_zoom_in_button, 1, 0, 1, 1)

        self.strain_zoom_out_button = QPushButton(self.strain_zoom_area)
        self.strain_zoom_out_button.setObjectName(u"strain_zoom_out_button")
        self.strain_zoom_out_button.setIcon(icon3)

        self.gridLayout_3.addWidget(self.strain_zoom_out_button, 1, 1, 1, 1)

        self.strain_zoom_label = QLabel(self.strain_zoom_area)
        self.strain_zoom_label.setObjectName(u"strain_zoom_label")
        self.strain_zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.strain_zoom_label, 0, 0, 1, 2)


        self.horizontalLayout.addWidget(self.strain_zoom_area)

        self.temp_zoom_area = QWidget(self.sub_menu)
        self.temp_zoom_area.setObjectName(u"temp_zoom_area")
        self.temp_zoom_area.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        self.gridLayout_4 = QGridLayout(self.temp_zoom_area)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.temp_zoom_in_button = QPushButton(self.temp_zoom_area)
        self.temp_zoom_in_button.setObjectName(u"temp_zoom_in_button")
        self.temp_zoom_in_button.setIcon(icon2)

        self.gridLayout_4.addWidget(self.temp_zoom_in_button, 1, 0, 1, 1)

        self.temp_zoom_out_button = QPushButton(self.temp_zoom_area)
        self.temp_zoom_out_button.setObjectName(u"temp_zoom_out_button")
        self.temp_zoom_out_button.setIcon(icon3)

        self.gridLayout_4.addWidget(self.temp_zoom_out_button, 1, 1, 1, 1)

        self.temp_zoom_label = QLabel(self.temp_zoom_area)
        self.temp_zoom_label.setObjectName(u"temp_zoom_label")
        self.temp_zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.temp_zoom_label, 0, 0, 1, 2)


        self.horizontalLayout.addWidget(self.temp_zoom_area)

        self.capture_button = QPushButton(self.sub_menu)
        self.capture_button.setObjectName(u"capture_button")
        self.capture_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon4 = QIcon()
        icon4.addFile(u":/ChartPages/Images/Pages/ChartPage/camera.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.capture_button.setIcon(icon4)
        self.capture_button.setIconSize(QSize(20, 20))
        self.capture_button.setFlat(True)

        self.horizontalLayout.addWidget(self.capture_button)

        self.sub_line2 = QFrame(self.sub_menu)
        self.sub_line2.setObjectName(u"sub_line2")
        self.sub_line2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.sub_line2.setFrameShape(QFrame.Shape.VLine)
        self.sub_line2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.sub_line2)

        self.sampling_settings = QWidget(self.sub_menu)
        self.sampling_settings.setObjectName(u"sampling_settings")
        self.gridLayout = QGridLayout(self.sampling_settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 2)
        self.sampling_rate_edit = QLineEdit(self.sampling_settings)
        self.sampling_rate_edit.setObjectName(u"sampling_rate_edit")
        self.sampling_rate_edit.setStyleSheet(u"")
        self.sampling_rate_edit.setText(u"0")
        self.sampling_rate_edit.setClearButtonEnabled(False)

        self.gridLayout.addWidget(self.sampling_rate_edit, 1, 0, 1, 1)

        self.sampling_rate_unit = QComboBox(self.sampling_settings)
        self.sampling_rate_unit.setObjectName(u"sampling_rate_unit")
        self.sampling_rate_unit.setStyleSheet(u"background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.sampling_rate_unit, 1, 1, 1, 1)

        self.sampling_label = QLabel(self.sampling_settings)
        self.sampling_label.setObjectName(u"sampling_label")
        font = QFont()
        font.setPointSize(8)
        self.sampling_label.setFont(font)

        self.gridLayout.addWidget(self.sampling_label, 0, 0, 1, 2)


        self.horizontalLayout.addWidget(self.sampling_settings)

        self.sub_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.sub_spacer)

        self.filter_config_button = QPushButton(self.sub_menu)
        self.filter_config_button.setObjectName(u"filter_config_button")
        self.filter_config_button.setStyleSheet(u" QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon5 = QIcon()
        icon5.addFile(u":/ChartPages/Images/Pages/ChartPage/filter.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.filter_config_button.setIcon(icon5)
        self.filter_config_button.setIconSize(QSize(20, 20))
        self.filter_config_button.setFlat(True)

        self.horizontalLayout.addWidget(self.filter_config_button)

        self.sensor_config_button = QPushButton(self.sub_menu)
        self.sensor_config_button.setObjectName(u"sensor_config_button")
        self.sensor_config_button.setStyleSheet(u" QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon6 = QIcon()
        icon6.addFile(u":/ChartPages/Images/Pages/ChartPage/options-outline.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sensor_config_button.setIcon(icon6)
        self.sensor_config_button.setIconSize(QSize(20, 20))
        self.sensor_config_button.setFlat(True)

        self.horizontalLayout.addWidget(self.sensor_config_button)


        self.page_layout.addWidget(self.sub_menu, 1, 1, 1, 1)

        self.sensor_settings = QWidget(chart_page)
        self.sensor_settings.setObjectName(u"sensor_settings")
        self.sensor_settings.setMinimumSize(QSize(250, 0))
        self.sensor_settings.setMaximumSize(QSize(250, 16777215))
        self.sensor_settings.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.sensor_settings)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(-1, 0, 9, 54)
        self.sensor_settings_header = QWidget(self.sensor_settings)
        self.sensor_settings_header.setObjectName(u"sensor_settings_header")
        self.horizontalLayout_5 = QHBoxLayout(self.sensor_settings_header)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.sensor_settings_close_button = QPushButton(self.sensor_settings_header)
        self.sensor_settings_close_button.setObjectName(u"sensor_settings_close_button")
        self.sensor_settings_close_button.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u":/ChartPages/Images/Pages/ChartPage/close-sharp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sensor_settings_close_button.setIcon(icon7)
        self.sensor_settings_close_button.setFlat(True)

        self.horizontalLayout_5.addWidget(self.sensor_settings_close_button)

        self.sensor_settings_label = QLabel(self.sensor_settings_header)
        self.sensor_settings_label.setObjectName(u"sensor_settings_label")
        self.sensor_settings_label.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.sensor_settings_label)

        self.sensor_settings_header_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.sensor_settings_header_spacer)


        self.verticalLayout_4.addWidget(self.sensor_settings_header)

        self.scrollArea = QScrollArea(self.sensor_settings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setStyleSheet(u"border:none\n"
"")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 232, 740))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 0, -1, 0)
        self.graph_settings_ch1 = QQuickWidget(self.scrollAreaWidgetContents)
        self.graph_settings_ch1.setObjectName(u"graph_settings_ch1")
        self.graph_settings_ch1.setMinimumSize(QSize(0, 147))
        self.graph_settings_ch1.setMaximumSize(QSize(16777215, 136))
        self.graph_settings_ch1.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.graph_settings_ch1.setSource(QUrl(u"qrc:/qml/qml/SensorSetting.qml"))

        self.verticalLayout_5.addWidget(self.graph_settings_ch1)

        self.graph_settings_ch2 = QQuickWidget(self.scrollAreaWidgetContents)
        self.graph_settings_ch2.setObjectName(u"graph_settings_ch2")
        self.graph_settings_ch2.setMinimumSize(QSize(0, 147))
        self.graph_settings_ch2.setMaximumSize(QSize(16777215, 136))
        self.graph_settings_ch2.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.graph_settings_ch2.setSource(QUrl(u"qrc:/qml/qml/SensorSetting.qml"))

        self.verticalLayout_5.addWidget(self.graph_settings_ch2)

        self.graph_settings_ch3 = QQuickWidget(self.scrollAreaWidgetContents)
        self.graph_settings_ch3.setObjectName(u"graph_settings_ch3")
        self.graph_settings_ch3.setMinimumSize(QSize(0, 147))
        self.graph_settings_ch3.setMaximumSize(QSize(16777215, 136))
        self.graph_settings_ch3.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.graph_settings_ch3.setSource(QUrl(u"qrc:/qml/qml/SensorSetting.qml"))

        self.verticalLayout_5.addWidget(self.graph_settings_ch3)

        self.graph_settings_ch4 = QQuickWidget(self.scrollAreaWidgetContents)
        self.graph_settings_ch4.setObjectName(u"graph_settings_ch4")
        self.graph_settings_ch4.setMinimumSize(QSize(0, 147))
        self.graph_settings_ch4.setMaximumSize(QSize(16777215, 136))
        self.graph_settings_ch4.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.graph_settings_ch4.setSource(QUrl(u"qrc:/qml/qml/SensorSetting.qml"))

        self.verticalLayout_5.addWidget(self.graph_settings_ch4)

        self.register_settings_button = QPushButton(self.scrollAreaWidgetContents)
        self.register_settings_button.setObjectName(u"register_settings_button")
        self.register_settings_button.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.register_settings_button)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)


        self.page_layout.addWidget(self.sensor_settings, 0, 2, 3, 1)

        self.main_menu = QWidget(chart_page)
        self.main_menu.setObjectName(u"main_menu")
        self.main_menu.setMinimumSize(QSize(0, 55))
        self.main_menu.setMaximumSize(QSize(16777215, 55))
        self.main_menu.setStyleSheet(u"background-color: rgb(200, 150, 200);")
        self.horizontalLayout_3 = QHBoxLayout(self.main_menu)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 6, -1, 6)
        self.meas_start_button = QPushButton(self.main_menu)
        self.meas_start_button.setObjectName(u"meas_start_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.meas_start_button.sizePolicy().hasHeightForWidth())
        self.meas_start_button.setSizePolicy(sizePolicy1)
        self.meas_start_button.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon8 = QIcon()
        icon8.addFile(u":/ChartPages/Images/Pages/ChartPage/play-outline.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.meas_start_button.setIcon(icon8)

        self.horizontalLayout_3.addWidget(self.meas_start_button)

        self.meas_stop_button = QPushButton(self.main_menu)
        self.meas_stop_button.setObjectName(u"meas_stop_button")
        sizePolicy1.setHeightForWidth(self.meas_stop_button.sizePolicy().hasHeightForWidth())
        self.meas_stop_button.setSizePolicy(sizePolicy1)
        self.meas_stop_button.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon9 = QIcon()
        icon9.addFile(u":/ChartPages/Images/Pages/ChartPage/pause.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.meas_stop_button.setIcon(icon9)

        self.horizontalLayout_3.addWidget(self.meas_stop_button)

        self.main_split_line_1 = QFrame(self.main_menu)
        self.main_split_line_1.setObjectName(u"main_split_line_1")
        self.main_split_line_1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.main_split_line_1.setFrameShape(QFrame.Shape.VLine)
        self.main_split_line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.main_split_line_1)

        self.auto_range_button = QPushButton(self.main_menu)
        self.auto_range_button.setObjectName(u"auto_range_button")
        sizePolicy1.setHeightForWidth(self.auto_range_button.sizePolicy().hasHeightForWidth())
        self.auto_range_button.setSizePolicy(sizePolicy1)
        self.auto_range_button.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon10 = QIcon()
        icon10.addFile(u":/ChartPages/Images/Pages/ChartPage/ruler-measure.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.auto_range_button.setIcon(icon10)

        self.horizontalLayout_3.addWidget(self.auto_range_button)

        self.auto_balance_button = QPushButton(self.main_menu)
        self.auto_balance_button.setObjectName(u"auto_balance_button")
        sizePolicy1.setHeightForWidth(self.auto_balance_button.sizePolicy().hasHeightForWidth())
        self.auto_balance_button.setSizePolicy(sizePolicy1)
        self.auto_balance_button.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon11 = QIcon()
        icon11.addFile(u":/ChartPages/Images/Pages/ChartPage/auto-balance.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.auto_balance_button.setIcon(icon11)

        self.horizontalLayout_3.addWidget(self.auto_balance_button)

        self.main_split_line_2 = QFrame(self.main_menu)
        self.main_split_line_2.setObjectName(u"main_split_line_2")
        self.main_split_line_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.main_split_line_2.setFrameShape(QFrame.Shape.VLine)
        self.main_split_line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.main_split_line_2)

        self.save_log_button = QPushButton(self.main_menu)
        self.save_log_button.setObjectName(u"save_log_button")
        sizePolicy1.setHeightForWidth(self.save_log_button.sizePolicy().hasHeightForWidth())
        self.save_log_button.setSizePolicy(sizePolicy1)
        self.save_log_button.setStyleSheet(u"QPushButton{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);} QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";} QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon12 = QIcon()
        icon12.addFile(u":/ChartPages/Images/Pages/ChartPage/save-floppy-disk.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_log_button.setIcon(icon12)

        self.horizontalLayout_3.addWidget(self.save_log_button)

        self.main_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.main_spacer)


        self.page_layout.addWidget(self.main_menu, 0, 1, 1, 1)

        self.filter_settings = QWidget(chart_page)
        self.filter_settings.setObjectName(u"filter_settings")
        self.filter_settings.setMinimumSize(QSize(250, 0))
        self.filter_settings.setMaximumSize(QSize(250, 16777215))
        self.filter_settings.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.filter_settings)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 9)
        self.filter_settings_header = QWidget(self.filter_settings)
        self.filter_settings_header.setObjectName(u"filter_settings_header")
        self.filter_settings_header.setStyleSheet(u"")
        self.horizontalLayout_4 = QHBoxLayout(self.filter_settings_header)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.filter_settings_label = QLabel(self.filter_settings_header)
        self.filter_settings_label.setObjectName(u"filter_settings_label")
        self.filter_settings_label.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.filter_settings_label)

        self.filter_settings_header_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.filter_settings_header_spacer)

        self.filter_settings_close_button = QPushButton(self.filter_settings_header)
        self.filter_settings_close_button.setObjectName(u"filter_settings_close_button")
        self.filter_settings_close_button.setStyleSheet(u"")
        self.filter_settings_close_button.setIcon(icon7)
        self.filter_settings_close_button.setFlat(True)

        self.horizontalLayout_4.addWidget(self.filter_settings_close_button)


        self.verticalLayout.addWidget(self.filter_settings_header)

        self.filter_setting_tabs = QTabWidget(self.filter_settings)
        self.filter_setting_tabs.setObjectName(u"filter_setting_tabs")
        self.filter_tab = QWidget()
        self.filter_tab.setObjectName(u"filter_tab")
        self.verticalLayout_7 = QVBoxLayout(self.filter_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, -1, 0, -1)
        self.ma_settings = QQuickWidget(self.filter_tab)
        self.ma_settings.setObjectName(u"ma_settings")
        self.ma_settings.setMinimumSize(QSize(0, 100))
        self.ma_settings.setMaximumSize(QSize(16777215, 100))
        self.ma_settings.setStyleSheet(u"border: 1px rgb(200,200,200);")
        self.ma_settings.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.ma_settings.setSource(QUrl(u"qrc:/qml/qml/MovingAverage.qml"))

        self.verticalLayout_7.addWidget(self.ma_settings)

        self.line_4 = QFrame(self.filter_tab)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_4)

        self.fft_settings = QQuickWidget(self.filter_tab)
        self.fft_settings.setObjectName(u"fft_settings")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.fft_settings.sizePolicy().hasHeightForWidth())
        self.fft_settings.setSizePolicy(sizePolicy2)
        self.fft_settings.setMinimumSize(QSize(0, 300))
        self.fft_settings.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.fft_settings.setSource(QUrl(u"qrc:/qml/qml/FFT.qml"))

        self.verticalLayout_7.addWidget(self.fft_settings)

        self.line_5 = QFrame(self.filter_tab)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_5)

        self.filter_settings_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.filter_settings_spacer)

        self.apply_filter_button = QPushButton(self.filter_tab)
        self.apply_filter_button.setObjectName(u"apply_filter_button")
        self.apply_filter_button.setMinimumSize(QSize(0, 29))
        self.apply_filter_button.setStyleSheet(u"background-color: rgb(15, 98, 254);\n"
"color: white;")
        icon13 = QIcon()
        icon13.addFile(u":/ChartPages/Images/Pages/ChartPage/refresh-ccw.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.apply_filter_button.setIcon(icon13)
        self.apply_filter_button.setIconSize(QSize(14, 14))

        self.verticalLayout_7.addWidget(self.apply_filter_button)

        self.filter_setting_tabs.addTab(self.filter_tab, "")
        self.csv_tab = QWidget()
        self.csv_tab.setObjectName(u"csv_tab")
        self.verticalLayout_6 = QVBoxLayout(self.csv_tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.csv_browse_area = QWidget(self.csv_tab)
        self.csv_browse_area.setObjectName(u"csv_browse_area")
        self.csv_browse_area.setMinimumSize(QSize(0, 150))
        self.csv_browse_area.setMaximumSize(QSize(16777215, 150))
        self.gridLayout_5 = QGridLayout(self.csv_browse_area)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.csv_browse_button = QPushButton(self.csv_browse_area)
        self.csv_browse_button.setObjectName(u"csv_browse_button")
        sizePolicy2.setHeightForWidth(self.csv_browse_button.sizePolicy().hasHeightForWidth())
        self.csv_browse_button.setSizePolicy(sizePolicy2)

        self.gridLayout_5.addWidget(self.csv_browse_button, 2, 1, 1, 1)

        self.csv_browse_label = QLabel(self.csv_browse_area)
        self.csv_browse_label.setObjectName(u"csv_browse_label")

        self.gridLayout_5.addWidget(self.csv_browse_label, 1, 0, 1, 1)

        self.csv_calc_type_label = QLabel(self.csv_browse_area)
        self.csv_calc_type_label.setObjectName(u"csv_calc_type_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.csv_calc_type_label.setFont(font1)

        self.gridLayout_5.addWidget(self.csv_calc_type_label, 0, 0, 1, 2)

        self.csv_browse_edit = QLineEdit(self.csv_browse_area)
        self.csv_browse_edit.setObjectName(u"csv_browse_edit")

        self.gridLayout_5.addWidget(self.csv_browse_edit, 2, 0, 1, 1)

        self.ch_select_label = QLabel(self.csv_browse_area)
        self.ch_select_label.setObjectName(u"ch_select_label")

        self.gridLayout_5.addWidget(self.ch_select_label, 3, 0, 1, 1)

        self.ch_select_combobox = QComboBox(self.csv_browse_area)
        self.ch_select_combobox.addItem(u"CH1")
        self.ch_select_combobox.addItem(u"CH2")
        self.ch_select_combobox.addItem(u"CH3")
        self.ch_select_combobox.addItem(u"CH4")
        self.ch_select_combobox.addItem("")
        self.ch_select_combobox.setObjectName(u"ch_select_combobox")

        self.gridLayout_5.addWidget(self.ch_select_combobox, 4, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.csv_browse_area)

        self.line_2 = QFrame(self.csv_tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_2)

        self.csv_setting_area = QWidget(self.csv_tab)
        self.csv_setting_area.setObjectName(u"csv_setting_area")
        self.csv_setting_area.setMinimumSize(QSize(0, 80))
        self.gridLayout_6 = QGridLayout(self.csv_setting_area)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(2)
        self.startpoint_label = QLabel(self.csv_setting_area)
        self.startpoint_label.setObjectName(u"startpoint_label")
        self.startpoint_label.setFont(font)

        self.gridLayout_6.addWidget(self.startpoint_label, 2, 0, 1, 1)

        self.startpoint_date_label = QLabel(self.csv_setting_area)
        self.startpoint_date_label.setObjectName(u"startpoint_date_label")
        font2 = QFont()
        font2.setPointSize(7)
        self.startpoint_date_label.setFont(font2)

        self.gridLayout_6.addWidget(self.startpoint_date_label, 4, 0, 1, 1)

        self.endpoint_date_label = QLabel(self.csv_setting_area)
        self.endpoint_date_label.setObjectName(u"endpoint_date_label")
        self.endpoint_date_label.setFont(font2)

        self.gridLayout_6.addWidget(self.endpoint_date_label, 4, 2, 1, 1)

        self.range_selection_label = QLabel(self.csv_setting_area)
        self.range_selection_label.setObjectName(u"range_selection_label")

        self.gridLayout_6.addWidget(self.range_selection_label, 1, 0, 1, 1)

        self.endpoint_label = QLabel(self.csv_setting_area)
        self.endpoint_label.setObjectName(u"endpoint_label")
        self.endpoint_label.setFont(font)

        self.gridLayout_6.addWidget(self.endpoint_label, 2, 2, 1, 1)

        self.endpoint_edit = QSpinBox(self.csv_setting_area)
        self.endpoint_edit.setObjectName(u"endpoint_edit")

        self.gridLayout_6.addWidget(self.endpoint_edit, 3, 2, 1, 1)

        self.startpoint_edit = QSpinBox(self.csv_setting_area)
        self.startpoint_edit.setObjectName(u"startpoint_edit")

        self.gridLayout_6.addWidget(self.startpoint_edit, 3, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.csv_setting_area)

        self.line = QFrame(self.csv_tab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.csv_output_area = QWidget(self.csv_tab)
        self.csv_output_area.setObjectName(u"csv_output_area")
        self.csv_output_area.setMinimumSize(QSize(0, 150))
        self.gridLayout_7 = QGridLayout(self.csv_output_area)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(49)
        self.gridLayout_7.setVerticalSpacing(3)
        self.output_label = QLabel(self.csv_output_area)
        self.output_label.setObjectName(u"output_label")

        self.gridLayout_7.addWidget(self.output_label, 0, 0, 1, 1)

        self.min_output = QLineEdit(self.csv_output_area)
        self.min_output.setObjectName(u"min_output")
        self.min_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.min_output, 2, 1, 1, 1)

        self.sigma_label = QLabel(self.csv_output_area)
        self.sigma_label.setObjectName(u"sigma_label")
        self.sigma_label.setFont(font)

        self.gridLayout_7.addWidget(self.sigma_label, 4, 0, 1, 1)

        self.min_label = QLabel(self.csv_output_area)
        self.min_label.setObjectName(u"min_label")
        self.min_label.setFont(font)

        self.gridLayout_7.addWidget(self.min_label, 2, 0, 1, 1)

        self.sigma3_label = QLabel(self.csv_output_area)
        self.sigma3_label.setObjectName(u"sigma3_label")
        self.sigma3_label.setFont(font)

        self.gridLayout_7.addWidget(self.sigma3_label, 6, 0, 1, 1)

        self.sigma_output = QLineEdit(self.csv_output_area)
        self.sigma_output.setObjectName(u"sigma_output")
        self.sigma_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.sigma_output, 4, 1, 1, 1)

        self.max_label = QLabel(self.csv_output_area)
        self.max_label.setObjectName(u"max_label")
        self.max_label.setFont(font)

        self.gridLayout_7.addWidget(self.max_label, 1, 0, 1, 1)

        self.sigma3_output = QLineEdit(self.csv_output_area)
        self.sigma3_output.setObjectName(u"sigma3_output")
        self.sigma3_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.sigma3_output, 6, 1, 1, 1)

        self.sigma33_output = QLineEdit(self.csv_output_area)
        self.sigma33_output.setObjectName(u"sigma33_output")
        self.sigma33_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.sigma33_output, 7, 1, 1, 1)

        self.ave_label = QLabel(self.csv_output_area)
        self.ave_label.setObjectName(u"ave_label")
        self.ave_label.setFont(font)

        self.gridLayout_7.addWidget(self.ave_label, 3, 0, 1, 1)

        self.max_output = QLineEdit(self.csv_output_area)
        self.max_output.setObjectName(u"max_output")
        sizePolicy2.setHeightForWidth(self.max_output.sizePolicy().hasHeightForWidth())
        self.max_output.setSizePolicy(sizePolicy2)
        self.max_output.setMinimumSize(QSize(0, 0))
        self.max_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.max_output, 1, 1, 1, 1)

        self.ave_output = QLineEdit(self.csv_output_area)
        self.ave_output.setObjectName(u"ave_output")
        self.ave_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.ave_output, 3, 1, 1, 1)

        self.sigma33_label = QLabel(self.csv_output_area)
        self.sigma33_label.setObjectName(u"sigma33_label")
        self.sigma33_label.setFont(font)

        self.gridLayout_7.addWidget(self.sigma33_label, 7, 0, 1, 1)

        self.sigma2_output = QLineEdit(self.csv_output_area)
        self.sigma2_output.setObjectName(u"sigma2_output")
        self.sigma2_output.setReadOnly(True)

        self.gridLayout_7.addWidget(self.sigma2_output, 5, 1, 1, 1)

        self.sigma2_label = QLabel(self.csv_output_area)
        self.sigma2_label.setObjectName(u"sigma2_label")
        self.sigma2_label.setFont(font)

        self.gridLayout_7.addWidget(self.sigma2_label, 5, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.csv_output_area)

        self.line_3 = QFrame(self.csv_tab)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_3)

        self.csv_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.csv_spacer)

        self.csv_calc_button = QPushButton(self.csv_tab)
        self.csv_calc_button.setObjectName(u"csv_calc_button")
        self.csv_calc_button.setStyleSheet(u"background-color: rgb(15, 98, 254);\n"
"color: white;")

        self.verticalLayout_6.addWidget(self.csv_calc_button)

        self.filter_setting_tabs.addTab(self.csv_tab, "")

        self.verticalLayout.addWidget(self.filter_setting_tabs)


        self.page_layout.addWidget(self.filter_settings, 0, 0, 3, 1)


        self.retranslateUi(chart_page)

        self.filter_setting_tabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(chart_page)
    # setupUi

    def retranslateUi(self, chart_page):
        chart_page.setWindowTitle(QCoreApplication.translate("chart_page", u"Form", None))
        self.table_title.setText(QCoreApplication.translate("chart_page", u"Sensor Data", None))
        self.table_setting_button.setText("")
        ___qtablewidgetitem = self.sensor_info.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("chart_page", u"View(Strain\u30fbTemp)", None));
        ___qtablewidgetitem1 = self.sensor_info.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("chart_page", u"Sensor Name", None));
        ___qtablewidgetitem2 = self.sensor_info.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("chart_page", u"Temperature", None));
        ___qtablewidgetitem3 = self.sensor_info.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("chart_page", u"Current Value", None));
        ___qtablewidgetitem4 = self.sensor_info.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("chart_page", u"Initial Value", None));
        ___qtablewidgetitem5 = self.sensor_info.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("chart_page", u"Delta", None));
        ___qtablewidgetitem6 = self.sensor_info.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("chart_page", u"Status", None));
        self.open_button.setText("")
        self.x_zoom_in_button.setText("")
        self.x_zoom_out_button.setText("")
        self.x_zoom_label.setText(QCoreApplication.translate("chart_page", u"X", None))
        self.strain_zoom_in_button.setText("")
        self.strain_zoom_out_button.setText("")
        self.strain_zoom_label.setText(QCoreApplication.translate("chart_page", u"Strain", None))
        self.temp_zoom_in_button.setText("")
        self.temp_zoom_out_button.setText("")
        self.temp_zoom_label.setText(QCoreApplication.translate("chart_page", u"Temp", None))
        self.capture_button.setText("")
        self.sampling_label.setText(QCoreApplication.translate("chart_page", u"Sampling Settings", None))
        self.filter_config_button.setText("")
        self.sensor_config_button.setText("")
        self.sensor_settings_close_button.setText("")
        self.sensor_settings_label.setText(QCoreApplication.translate("chart_page", u"Sensor Advanced Settings", None))
        self.register_settings_button.setText(QCoreApplication.translate("chart_page", u"Register Settings", None))
        self.meas_start_button.setText(QCoreApplication.translate("chart_page", u"Start", None))
        self.meas_stop_button.setText(QCoreApplication.translate("chart_page", u"Stop", None))
        self.auto_range_button.setText(QCoreApplication.translate("chart_page", u"Auto Range", None))
        self.auto_balance_button.setText(QCoreApplication.translate("chart_page", u"Auto Balance", None))
        self.save_log_button.setText(QCoreApplication.translate("chart_page", u"Save log", None))
        self.filter_settings_label.setText(QCoreApplication.translate("chart_page", u"Filter Settings", None))
        self.filter_settings_close_button.setText("")
        self.apply_filter_button.setText(QCoreApplication.translate("chart_page", u" Apply Filter", None))
        self.filter_setting_tabs.setTabText(self.filter_setting_tabs.indexOf(self.filter_tab), QCoreApplication.translate("chart_page", u"Filter", None))
        self.csv_browse_button.setText(QCoreApplication.translate("chart_page", u"Browse", None))
        self.csv_browse_label.setText(QCoreApplication.translate("chart_page", u"CSV Path", None))
        self.csv_calc_type_label.setText(QCoreApplication.translate("chart_page", u"Standard Deviation", None))
        self.ch_select_label.setText(QCoreApplication.translate("chart_page", u"Select CH", None))
        self.ch_select_combobox.setItemText(4, QCoreApplication.translate("chart_page", u"ALL", None))

        self.startpoint_label.setText(QCoreApplication.translate("chart_page", u"Start Point", None))
        self.range_selection_label.setText(QCoreApplication.translate("chart_page", u"Range Selection", None))
        self.endpoint_label.setText(QCoreApplication.translate("chart_page", u"End Point", None))
        self.output_label.setText(QCoreApplication.translate("chart_page", u"Output", None))
        self.sigma_label.setText(QCoreApplication.translate("chart_page", u"\u03c3      :", None))
        self.min_label.setText(QCoreApplication.translate("chart_page", u"Min  :", None))
        self.sigma3_label.setText(QCoreApplication.translate("chart_page", u"3\u03c3    :", None))
        self.max_label.setText(QCoreApplication.translate("chart_page", u"Max :", None))
        self.ave_label.setText(QCoreApplication.translate("chart_page", u"Ave  :", None))
        self.sigma33_label.setText(QCoreApplication.translate("chart_page", u"3.3\u03c3 :", None))
        self.sigma2_label.setText(QCoreApplication.translate("chart_page", u"2\u03c3    :", None))
        self.csv_calc_button.setText(QCoreApplication.translate("chart_page", u"Calc", None))
        self.filter_setting_tabs.setTabText(self.filter_setting_tabs.indexOf(self.csv_tab), QCoreApplication.translate("chart_page", u"CSV", None))
    # retranslateUi

