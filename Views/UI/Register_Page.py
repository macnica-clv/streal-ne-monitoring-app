# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Register_Page.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)
from Views import resources_rc

class Ui_register_page(object):
    def setupUi(self, register_page):
        if not register_page.objectName():
            register_page.setObjectName(u"register_page")
        register_page.setWindowModality(Qt.WindowModality.ApplicationModal)
        register_page.resize(868, 652)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(register_page.sizePolicy().hasHeightForWidth())
        register_page.setSizePolicy(sizePolicy)
        self.main_widget = QWidget(register_page)
        self.main_widget.setObjectName(u"main_widget")
        self.verticalLayout = QVBoxLayout(self.main_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.register_setting_area = QWidget(self.main_widget)
        self.register_setting_area.setObjectName(u"register_setting_area")
        self.register_setting_area.setStyleSheet(u"#register_setting_area {\n"
"           /* \u5185\u5074\u306e\u30a6\u30a3\u30b8\u30a7\u30c3\u30c8\u304c\u767d */\n"
"}\n"
"QScrollBar:vertical {\n"
"    width: 8px;\n"
"    background: transparent;\n"
"    margin: 2px 0 2px 0;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgb(180, 180, 180);\n"
"    min-height: 20px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: rgb(150, 150, 150);\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed {\n"
"    background: rgb(120, 120, 120);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.verticalLayout_13 = QVBoxLayout(self.register_setting_area)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.help_area = QWidget(self.register_setting_area)
        self.help_area.setObjectName(u"help_area")
        self.help_area.setMinimumSize(QSize(0, 25))
        self.help_area.setMaximumSize(QSize(16777215, 25))
        self.help_area.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.help_area)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.select_channel_label = QLabel(self.help_area)
        self.select_channel_label.setObjectName(u"select_channel_label")
        font = QFont()
        font.setPointSize(12)
        self.select_channel_label.setFont(font)
        self.select_channel_label.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.select_channel_label)

        self.ch_select = QComboBox(self.help_area)
        self.ch_select.addItem("")
        self.ch_select.addItem("")
        self.ch_select.addItem("")
        self.ch_select.addItem("")
        self.ch_select.setObjectName(u"ch_select")
        self.ch_select.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.ch_select)

        self.help_spacer = QSpacerItem(550, 4, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.help_spacer)

        self.help_button = QPushButton(self.help_area)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/RegisterPages/Images/Pages/RegisterPage/help-circle-sharp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.help_button.setIcon(icon)
        self.help_button.setIconSize(QSize(20, 20))
        self.help_button.setFlat(True)

        self.horizontalLayout_3.addWidget(self.help_button)


        self.verticalLayout_13.addWidget(self.help_area)

        self.setting_area = QScrollArea(self.register_setting_area)
        self.setting_area.setObjectName(u"setting_area")
        self.setting_area.setStyleSheet(u"")
        self.setting_area.setFrameShape(QFrame.Shape.NoFrame)
        self.setting_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setting_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setting_area.setWidgetResizable(True)
        self.setting_scroll_area = QWidget()
        self.setting_scroll_area.setObjectName(u"setting_scroll_area")
        self.setting_scroll_area.setEnabled(True)
        self.setting_scroll_area.setGeometry(QRect(0, 0, 824, 970))
        self.setting_scroll_area.setMinimumSize(QSize(500, 970))
        self.setting_scroll_area.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.setting_scroll_area)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.output_mode = QGroupBox(self.setting_scroll_area)
        self.output_mode.setObjectName(u"output_mode")
        self.output_mode.setMinimumSize(QSize(0, 50))
        self.output_mode.setStyleSheet(u"")
        self.output_mode.setFlat(True)
        self.horizontalLayout = QHBoxLayout(self.output_mode)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 6, -1, -1)
        self.label = QLabel(self.output_mode)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(10)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.output_mode)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_3.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer = QSpacerItem(399, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.output_mode_select = QComboBox(self.output_mode)
        self.output_mode_select.addItem("")
        self.output_mode_select.addItem("")
        self.output_mode_select.setObjectName(u"output_mode_select")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.output_mode_select.sizePolicy().hasHeightForWidth())
        self.output_mode_select.setSizePolicy(sizePolicy1)
        self.output_mode_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout.addWidget(self.output_mode_select)


        self.verticalLayout_4.addWidget(self.output_mode)

        self.osr = QGroupBox(self.setting_scroll_area)
        self.osr.setObjectName(u"osr")
        self.osr.setMinimumSize(QSize(0, 50))
        self.osr.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.horizontalLayout_4 = QHBoxLayout(self.osr)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 6, -1, -1)
        self.label_3 = QLabel(self.osr)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.label_3)

        self.label_4 = QLabel(self.osr)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_5.addWidget(self.label_4)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.horizontalSpacer_2 = QSpacerItem(294, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.osr_select = QComboBox(self.osr)
        self.osr_select.addItem("")
        self.osr_select.addItem("")
        self.osr_select.addItem("")
        self.osr_select.addItem("")
        self.osr_select.setObjectName(u"osr_select")

        self.horizontalLayout_4.addWidget(self.osr_select)


        self.verticalLayout_4.addWidget(self.osr)

        self.register_refresh_operation = QGroupBox(self.setting_scroll_area)
        self.register_refresh_operation.setObjectName(u"register_refresh_operation")
        self.register_refresh_operation.setMinimumSize(QSize(0, 50))
        self.register_refresh_operation.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.register_refresh_operation.setFlat(True)
        self.horizontalLayout_5 = QHBoxLayout(self.register_refresh_operation)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 6, -1, -1)
        self.label_5 = QLabel(self.register_refresh_operation)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet(u"")

        self.verticalLayout_6.addWidget(self.label_5)

        self.label_6 = QLabel(self.register_refresh_operation)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_6.addWidget(self.label_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)

        self.horizontalSpacer_3 = QSpacerItem(294, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.register_refresh_op_select = QComboBox(self.register_refresh_operation)
        self.register_refresh_op_select.addItem("")
        self.register_refresh_op_select.addItem("")
        self.register_refresh_op_select.setObjectName(u"register_refresh_op_select")
        sizePolicy1.setHeightForWidth(self.register_refresh_op_select.sizePolicy().hasHeightForWidth())
        self.register_refresh_op_select.setSizePolicy(sizePolicy1)
        self.register_refresh_op_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_5.addWidget(self.register_refresh_op_select)


        self.verticalLayout_4.addWidget(self.register_refresh_operation)

        self.groupBox_4 = QGroupBox(self.setting_scroll_area)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 50))
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.groupBox_4.setFlat(True)
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(5, 6, -1, -1)
        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setStyleSheet(u"")

        self.verticalLayout_7.addWidget(self.label_7)

        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_7.addWidget(self.label_8)


        self.horizontalLayout_6.addLayout(self.verticalLayout_7)

        self.horizontalSpacer_4 = QSpacerItem(338, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.sensor_id_select = QComboBox(self.groupBox_4)
        self.sensor_id_select.addItem("")
        self.sensor_id_select.addItem("")
        self.sensor_id_select.addItem("")
        self.sensor_id_select.addItem("")
        self.sensor_id_select.setObjectName(u"sensor_id_select")
        sizePolicy1.setHeightForWidth(self.sensor_id_select.sizePolicy().hasHeightForWidth())
        self.sensor_id_select.setSizePolicy(sizePolicy1)
        self.sensor_id_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_6.addWidget(self.sensor_id_select)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.setting_scroll_area)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 50))
        self.groupBox_5.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.groupBox_5.setFlat(True)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(5, 6, -1, -1)
        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)
        self.label_9.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.label_9)

        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_8.addWidget(self.label_10)


        self.horizontalLayout_7.addLayout(self.verticalLayout_8)

        self.horizontalSpacer_5 = QSpacerItem(157, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.temp_orig_min = QLabel(self.groupBox_5)
        self.temp_orig_min.setObjectName(u"temp_orig_min")
        self.temp_orig_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_7.addWidget(self.temp_orig_min)

        self.temp_orig_slider = QSlider(self.groupBox_5)
        self.temp_orig_slider.setObjectName(u"temp_orig_slider")
        sizePolicy1.setHeightForWidth(self.temp_orig_slider.sizePolicy().hasHeightForWidth())
        self.temp_orig_slider.setSizePolicy(sizePolicy1)
        self.temp_orig_slider.setMinimumSize(QSize(160, 0))
        self.temp_orig_slider.setMinimum(-128)
        self.temp_orig_slider.setMaximum(127)
        self.temp_orig_slider.setOrientation(Qt.Orientation.Horizontal)
        self.temp_orig_slider.setInvertedAppearance(False)
        self.temp_orig_slider.setInvertedControls(False)

        self.horizontalLayout_7.addWidget(self.temp_orig_slider)

        self.temp_orig_max = QLabel(self.groupBox_5)
        self.temp_orig_max.setObjectName(u"temp_orig_max")
        self.temp_orig_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_7.addWidget(self.temp_orig_max)

        self.temp_orig_spin = QSpinBox(self.groupBox_5)
        self.temp_orig_spin.setObjectName(u"temp_orig_spin")
        self.temp_orig_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.temp_orig_spin.setMinimum(-128)
        self.temp_orig_spin.setMaximum(127)
        self.temp_orig_spin.setSingleStep(1)

        self.horizontalLayout_7.addWidget(self.temp_orig_spin)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.setting_scroll_area)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 62))
        self.groupBox_6.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.groupBox_6.setFlat(True)
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 6, -1, -1)
        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)
        self.label_13.setStyleSheet(u"")

        self.verticalLayout_9.addWidget(self.label_13)

        self.label_14 = QLabel(self.groupBox_6)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_9.addWidget(self.label_14)

        self.label_15 = QLabel(self.groupBox_6)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_9.addWidget(self.label_15)


        self.horizontalLayout_8.addLayout(self.verticalLayout_9)

        self.horizontalSpacer_6 = QSpacerItem(190, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.temp_th0_min = QLabel(self.groupBox_6)
        self.temp_th0_min.setObjectName(u"temp_th0_min")
        self.temp_th0_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_8.addWidget(self.temp_th0_min)

        self.temp_th0_slider = QSlider(self.groupBox_6)
        self.temp_th0_slider.setObjectName(u"temp_th0_slider")
        sizePolicy1.setHeightForWidth(self.temp_th0_slider.sizePolicy().hasHeightForWidth())
        self.temp_th0_slider.setSizePolicy(sizePolicy1)
        self.temp_th0_slider.setMinimumSize(QSize(160, 0))
        self.temp_th0_slider.setStyleSheet(u"background-color:none\n"
"")
        self.temp_th0_slider.setMinimum(-128)
        self.temp_th0_slider.setMaximum(127)
        self.temp_th0_slider.setOrientation(Qt.Orientation.Horizontal)
        self.temp_th0_slider.setInvertedAppearance(False)
        self.temp_th0_slider.setInvertedControls(False)

        self.horizontalLayout_8.addWidget(self.temp_th0_slider)

        self.temp_th0_max = QLabel(self.groupBox_6)
        self.temp_th0_max.setObjectName(u"temp_th0_max")
        self.temp_th0_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_8.addWidget(self.temp_th0_max)

        self.temp_th0_spin = QSpinBox(self.groupBox_6)
        self.temp_th0_spin.setObjectName(u"temp_th0_spin")
        self.temp_th0_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.temp_th0_spin.setMinimum(-128)
        self.temp_th0_spin.setMaximum(127)
        self.temp_th0_spin.setSingleStep(1)
        self.temp_th0_spin.setValue(0)

        self.horizontalLayout_8.addWidget(self.temp_th0_spin)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.setting_scroll_area)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(0, 50))
        self.groupBox_7.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.groupBox_7.setFlat(True)
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 6, -1, -1)
        self.label_18 = QLabel(self.groupBox_7)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font1)
        self.label_18.setStyleSheet(u"")

        self.verticalLayout_10.addWidget(self.label_18)

        self.label_19 = QLabel(self.groupBox_7)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_10.addWidget(self.label_19)


        self.horizontalLayout_9.addLayout(self.verticalLayout_10)

        self.horizontalSpacer_7 = QSpacerItem(272, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.offset_coef0_min = QLabel(self.groupBox_7)
        self.offset_coef0_min.setObjectName(u"offset_coef0_min")
        self.offset_coef0_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_9.addWidget(self.offset_coef0_min)

        self.offset_coef0_slider = QSlider(self.groupBox_7)
        self.offset_coef0_slider.setObjectName(u"offset_coef0_slider")
        sizePolicy1.setHeightForWidth(self.offset_coef0_slider.sizePolicy().hasHeightForWidth())
        self.offset_coef0_slider.setSizePolicy(sizePolicy1)
        self.offset_coef0_slider.setMinimumSize(QSize(160, 0))
        self.offset_coef0_slider.setStyleSheet(u"background-color:none\n"
"")
        self.offset_coef0_slider.setMinimum(-20)
        self.offset_coef0_slider.setMaximum(20)
        self.offset_coef0_slider.setOrientation(Qt.Orientation.Horizontal)
        self.offset_coef0_slider.setInvertedAppearance(False)
        self.offset_coef0_slider.setInvertedControls(False)

        self.horizontalLayout_9.addWidget(self.offset_coef0_slider)

        self.offset_coef0_max = QLabel(self.groupBox_7)
        self.offset_coef0_max.setObjectName(u"offset_coef0_max")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.offset_coef0_max.sizePolicy().hasHeightForWidth())
        self.offset_coef0_max.setSizePolicy(sizePolicy2)
        self.offset_coef0_max.setMinimumSize(QSize(18, 0))
        self.offset_coef0_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_9.addWidget(self.offset_coef0_max)

        self.offset_coef0_spin = QSpinBox(self.groupBox_7)
        self.offset_coef0_spin.setObjectName(u"offset_coef0_spin")
        self.offset_coef0_spin.setMinimumSize(QSize(78, 0))
        self.offset_coef0_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.offset_coef0_spin.setMinimum(-2)
        self.offset_coef0_spin.setMaximum(2)
        self.offset_coef0_spin.setSingleStep(0)

        self.horizontalLayout_9.addWidget(self.offset_coef0_spin)


        self.verticalLayout_4.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.setting_scroll_area)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(0, 50))
        self.groupBox_8.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.groupBox_8.setFlat(True)
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(5, 6, -1, -1)
        self.label_20 = QLabel(self.groupBox_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)
        self.label_20.setStyleSheet(u"")

        self.verticalLayout_11.addWidget(self.label_20)

        self.label_21 = QLabel(self.groupBox_8)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_11.addWidget(self.label_21)


        self.horizontalLayout_10.addLayout(self.verticalLayout_11)

        self.horizontalSpacer_8 = QSpacerItem(205, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.offset_temp_coef0_min = QLabel(self.groupBox_8)
        self.offset_temp_coef0_min.setObjectName(u"offset_temp_coef0_min")
        self.offset_temp_coef0_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_10.addWidget(self.offset_temp_coef0_min)

        self.offset_temp_coef0_slider = QSlider(self.groupBox_8)
        self.offset_temp_coef0_slider.setObjectName(u"offset_temp_coef0_slider")
        sizePolicy1.setHeightForWidth(self.offset_temp_coef0_slider.sizePolicy().hasHeightForWidth())
        self.offset_temp_coef0_slider.setSizePolicy(sizePolicy1)
        self.offset_temp_coef0_slider.setMinimumSize(QSize(160, 0))
        self.offset_temp_coef0_slider.setStyleSheet(u"background-color:none\n"
"")
        self.offset_temp_coef0_slider.setMinimum(-10)
        self.offset_temp_coef0_slider.setMaximum(10)
        self.offset_temp_coef0_slider.setOrientation(Qt.Orientation.Horizontal)
        self.offset_temp_coef0_slider.setInvertedAppearance(False)
        self.offset_temp_coef0_slider.setInvertedControls(False)

        self.horizontalLayout_10.addWidget(self.offset_temp_coef0_slider)

        self.offset_temp_coef0_max = QLabel(self.groupBox_8)
        self.offset_temp_coef0_max.setObjectName(u"offset_temp_coef0_max")
        sizePolicy2.setHeightForWidth(self.offset_temp_coef0_max.sizePolicy().hasHeightForWidth())
        self.offset_temp_coef0_max.setSizePolicy(sizePolicy2)
        self.offset_temp_coef0_max.setMinimumSize(QSize(18, 0))
        self.offset_temp_coef0_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_10.addWidget(self.offset_temp_coef0_max)

        self.offset_temp_coef0_spin = QSpinBox(self.groupBox_8)
        self.offset_temp_coef0_spin.setObjectName(u"offset_temp_coef0_spin")
        self.offset_temp_coef0_spin.setMinimumSize(QSize(78, 0))
        self.offset_temp_coef0_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.offset_temp_coef0_spin.setMinimum(-1)
        self.offset_temp_coef0_spin.setMaximum(1)
        self.offset_temp_coef0_spin.setSingleStep(0)

        self.horizontalLayout_10.addWidget(self.offset_temp_coef0_spin)


        self.verticalLayout_4.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.setting_scroll_area)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(0, 50))
        self.groupBox_9.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.groupBox_9.setFlat(True)
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(5, 6, -1, -1)
        self.label_26 = QLabel(self.groupBox_9)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)
        self.label_26.setStyleSheet(u"")

        self.verticalLayout_12.addWidget(self.label_26)

        self.label_27 = QLabel(self.groupBox_9)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_12.addWidget(self.label_27)


        self.horizontalLayout_11.addLayout(self.verticalLayout_12)

        self.horizontalSpacer_9 = QSpacerItem(266, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_9)

        self.offset_coef1_min = QLabel(self.groupBox_9)
        self.offset_coef1_min.setObjectName(u"offset_coef1_min")
        self.offset_coef1_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_11.addWidget(self.offset_coef1_min)

        self.offset_coef1_slider = QSlider(self.groupBox_9)
        self.offset_coef1_slider.setObjectName(u"offset_coef1_slider")
        sizePolicy1.setHeightForWidth(self.offset_coef1_slider.sizePolicy().hasHeightForWidth())
        self.offset_coef1_slider.setSizePolicy(sizePolicy1)
        self.offset_coef1_slider.setMinimumSize(QSize(160, 0))
        self.offset_coef1_slider.setStyleSheet(u"background-color:none\n"
"")
        self.offset_coef1_slider.setMinimum(-20)
        self.offset_coef1_slider.setMaximum(20)
        self.offset_coef1_slider.setOrientation(Qt.Orientation.Horizontal)
        self.offset_coef1_slider.setInvertedAppearance(False)
        self.offset_coef1_slider.setInvertedControls(False)

        self.horizontalLayout_11.addWidget(self.offset_coef1_slider)

        self.offset_coef1_max = QLabel(self.groupBox_9)
        self.offset_coef1_max.setObjectName(u"offset_coef1_max")
        sizePolicy2.setHeightForWidth(self.offset_coef1_max.sizePolicy().hasHeightForWidth())
        self.offset_coef1_max.setSizePolicy(sizePolicy2)
        self.offset_coef1_max.setMinimumSize(QSize(18, 0))
        self.offset_coef1_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_11.addWidget(self.offset_coef1_max)

        self.offset_coef1_spin = QSpinBox(self.groupBox_9)
        self.offset_coef1_spin.setObjectName(u"offset_coef1_spin")
        self.offset_coef1_spin.setMinimumSize(QSize(78, 0))
        self.offset_coef1_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.offset_coef1_spin.setMinimum(-2)
        self.offset_coef1_spin.setMaximum(2)
        self.offset_coef1_spin.setSingleStep(0)

        self.horizontalLayout_11.addWidget(self.offset_coef1_spin)


        self.verticalLayout_4.addWidget(self.groupBox_9)

        self.offset_temp_coef1 = QGroupBox(self.setting_scroll_area)
        self.offset_temp_coef1.setObjectName(u"offset_temp_coef1")
        self.offset_temp_coef1.setMinimumSize(QSize(0, 50))
        self.offset_temp_coef1.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.offset_temp_coef1.setFlat(True)
        self.horizontalLayout_12 = QHBoxLayout(self.offset_temp_coef1)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(5, 6, -1, -1)
        self.label_30 = QLabel(self.offset_temp_coef1)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font1)
        self.label_30.setStyleSheet(u"")

        self.verticalLayout_14.addWidget(self.label_30)

        self.label_31 = QLabel(self.offset_temp_coef1)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_14.addWidget(self.label_31)


        self.horizontalLayout_12.addLayout(self.verticalLayout_14)

        self.horizontalSpacer_10 = QSpacerItem(199, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)

        self.offset_temp_coef1_min = QLabel(self.offset_temp_coef1)
        self.offset_temp_coef1_min.setObjectName(u"offset_temp_coef1_min")
        self.offset_temp_coef1_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_12.addWidget(self.offset_temp_coef1_min)

        self.offset_temp_coef1_slider = QSlider(self.offset_temp_coef1)
        self.offset_temp_coef1_slider.setObjectName(u"offset_temp_coef1_slider")
        sizePolicy1.setHeightForWidth(self.offset_temp_coef1_slider.sizePolicy().hasHeightForWidth())
        self.offset_temp_coef1_slider.setSizePolicy(sizePolicy1)
        self.offset_temp_coef1_slider.setMinimumSize(QSize(160, 0))
        self.offset_temp_coef1_slider.setStyleSheet(u"background-color:none\n"
"")
        self.offset_temp_coef1_slider.setMinimum(-10)
        self.offset_temp_coef1_slider.setMaximum(10)
        self.offset_temp_coef1_slider.setOrientation(Qt.Orientation.Horizontal)
        self.offset_temp_coef1_slider.setInvertedAppearance(False)
        self.offset_temp_coef1_slider.setInvertedControls(False)

        self.horizontalLayout_12.addWidget(self.offset_temp_coef1_slider)

        self.offset_temp_coef1_max = QLabel(self.offset_temp_coef1)
        self.offset_temp_coef1_max.setObjectName(u"offset_temp_coef1_max")
        sizePolicy2.setHeightForWidth(self.offset_temp_coef1_max.sizePolicy().hasHeightForWidth())
        self.offset_temp_coef1_max.setSizePolicy(sizePolicy2)
        self.offset_temp_coef1_max.setMinimumSize(QSize(18, 0))
        self.offset_temp_coef1_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_12.addWidget(self.offset_temp_coef1_max)

        self.offset_temp_coef1_spin = QSpinBox(self.offset_temp_coef1)
        self.offset_temp_coef1_spin.setObjectName(u"offset_temp_coef1_spin")
        self.offset_temp_coef1_spin.setMinimumSize(QSize(78, 0))
        self.offset_temp_coef1_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.offset_temp_coef1_spin.setMinimum(-1)
        self.offset_temp_coef1_spin.setMaximum(1)
        self.offset_temp_coef1_spin.setSingleStep(0)

        self.horizontalLayout_12.addWidget(self.offset_temp_coef1_spin)


        self.verticalLayout_4.addWidget(self.offset_temp_coef1)

        self.fsadj_offset_coef = QGroupBox(self.setting_scroll_area)
        self.fsadj_offset_coef.setObjectName(u"fsadj_offset_coef")
        self.fsadj_offset_coef.setMinimumSize(QSize(0, 62))
        self.fsadj_offset_coef.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.fsadj_offset_coef.setFlat(True)
        self.horizontalLayout_13 = QHBoxLayout(self.fsadj_offset_coef)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(5, 6, -1, -1)
        self.label_32 = QLabel(self.fsadj_offset_coef)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font1)
        self.label_32.setStyleSheet(u"")

        self.verticalLayout_15.addWidget(self.label_32)

        self.label_33 = QLabel(self.fsadj_offset_coef)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_15.addWidget(self.label_33)

        self.label_34 = QLabel(self.fsadj_offset_coef)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_15.addWidget(self.label_34)


        self.horizontalLayout_13.addLayout(self.verticalLayout_15)

        self.horizontalSpacer_11 = QSpacerItem(175, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)

        self.fsadj_offset_coef_min = QLabel(self.fsadj_offset_coef)
        self.fsadj_offset_coef_min.setObjectName(u"fsadj_offset_coef_min")
        self.fsadj_offset_coef_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_13.addWidget(self.fsadj_offset_coef_min)

        self.fsadj_offset_coef_slider = QSlider(self.fsadj_offset_coef)
        self.fsadj_offset_coef_slider.setObjectName(u"fsadj_offset_coef_slider")
        sizePolicy1.setHeightForWidth(self.fsadj_offset_coef_slider.sizePolicy().hasHeightForWidth())
        self.fsadj_offset_coef_slider.setSizePolicy(sizePolicy1)
        self.fsadj_offset_coef_slider.setMinimumSize(QSize(160, 0))
        self.fsadj_offset_coef_slider.setStyleSheet(u"background-color:none\n"
"")
        self.fsadj_offset_coef_slider.setMinimum(-20)
        self.fsadj_offset_coef_slider.setMaximum(20)
        self.fsadj_offset_coef_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fsadj_offset_coef_slider.setInvertedAppearance(False)
        self.fsadj_offset_coef_slider.setInvertedControls(False)

        self.horizontalLayout_13.addWidget(self.fsadj_offset_coef_slider)

        self.fsadj_offset_coef_max = QLabel(self.fsadj_offset_coef)
        self.fsadj_offset_coef_max.setObjectName(u"fsadj_offset_coef_max")
        sizePolicy2.setHeightForWidth(self.fsadj_offset_coef_max.sizePolicy().hasHeightForWidth())
        self.fsadj_offset_coef_max.setSizePolicy(sizePolicy2)
        self.fsadj_offset_coef_max.setMinimumSize(QSize(18, 0))
        self.fsadj_offset_coef_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_13.addWidget(self.fsadj_offset_coef_max)

        self.fsadj_offset_coef_spin = QSpinBox(self.fsadj_offset_coef)
        self.fsadj_offset_coef_spin.setObjectName(u"fsadj_offset_coef_spin")
        self.fsadj_offset_coef_spin.setMinimumSize(QSize(78, 0))
        self.fsadj_offset_coef_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.fsadj_offset_coef_spin.setMinimum(-2)
        self.fsadj_offset_coef_spin.setMaximum(2)
        self.fsadj_offset_coef_spin.setSingleStep(0)

        self.horizontalLayout_13.addWidget(self.fsadj_offset_coef_spin)


        self.verticalLayout_4.addWidget(self.fsadj_offset_coef)

        self.fsadj_gain_coef = QGroupBox(self.setting_scroll_area)
        self.fsadj_gain_coef.setObjectName(u"fsadj_gain_coef")
        self.fsadj_gain_coef.setMinimumSize(QSize(0, 62))
        self.fsadj_gain_coef.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.fsadj_gain_coef.setFlat(True)
        self.horizontalLayout_14 = QHBoxLayout(self.fsadj_gain_coef)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(5, 6, -1, -1)
        self.label_35 = QLabel(self.fsadj_gain_coef)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font1)
        self.label_35.setStyleSheet(u"")

        self.verticalLayout_16.addWidget(self.label_35)

        self.label_36 = QLabel(self.fsadj_gain_coef)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_16.addWidget(self.label_36)

        self.label_37 = QLabel(self.fsadj_gain_coef)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_16.addWidget(self.label_37)


        self.horizontalLayout_14.addLayout(self.verticalLayout_16)

        self.horizontalSpacer_12 = QSpacerItem(178, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_12)

        self.fsadj_gain_coef_min = QLabel(self.fsadj_gain_coef)
        self.fsadj_gain_coef_min.setObjectName(u"fsadj_gain_coef_min")
        self.fsadj_gain_coef_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_14.addWidget(self.fsadj_gain_coef_min)

        self.fsadj_gain_coef_slider = QSlider(self.fsadj_gain_coef)
        self.fsadj_gain_coef_slider.setObjectName(u"fsadj_gain_coef_slider")
        sizePolicy1.setHeightForWidth(self.fsadj_gain_coef_slider.sizePolicy().hasHeightForWidth())
        self.fsadj_gain_coef_slider.setSizePolicy(sizePolicy1)
        self.fsadj_gain_coef_slider.setMinimumSize(QSize(160, 0))
        self.fsadj_gain_coef_slider.setStyleSheet(u"background-color:none\n"
"")
        self.fsadj_gain_coef_slider.setMinimum(-20)
        self.fsadj_gain_coef_slider.setMaximum(20)
        self.fsadj_gain_coef_slider.setOrientation(Qt.Orientation.Horizontal)
        self.fsadj_gain_coef_slider.setInvertedAppearance(False)
        self.fsadj_gain_coef_slider.setInvertedControls(False)

        self.horizontalLayout_14.addWidget(self.fsadj_gain_coef_slider)

        self.fsadj_gain_coef_max = QLabel(self.fsadj_gain_coef)
        self.fsadj_gain_coef_max.setObjectName(u"fsadj_gain_coef_max")
        sizePolicy2.setHeightForWidth(self.fsadj_gain_coef_max.sizePolicy().hasHeightForWidth())
        self.fsadj_gain_coef_max.setSizePolicy(sizePolicy2)
        self.fsadj_gain_coef_max.setMinimumSize(QSize(18, 0))
        self.fsadj_gain_coef_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_14.addWidget(self.fsadj_gain_coef_max)

        self.fsadj_gain_coef_spin = QSpinBox(self.fsadj_gain_coef)
        self.fsadj_gain_coef_spin.setObjectName(u"fsadj_gain_coef_spin")
        self.fsadj_gain_coef_spin.setMinimumSize(QSize(78, 0))
        self.fsadj_gain_coef_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.fsadj_gain_coef_spin.setMinimum(-2)
        self.fsadj_gain_coef_spin.setMaximum(2)
        self.fsadj_gain_coef_spin.setSingleStep(0)

        self.horizontalLayout_14.addWidget(self.fsadj_gain_coef_spin)


        self.verticalLayout_4.addWidget(self.fsadj_gain_coef)

        self.offset_g2_coef = QGroupBox(self.setting_scroll_area)
        self.offset_g2_coef.setObjectName(u"offset_g2_coef")
        self.offset_g2_coef.setMinimumSize(QSize(0, 62))
        self.offset_g2_coef.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.offset_g2_coef.setFlat(True)
        self.horizontalLayout_15 = QHBoxLayout(self.offset_g2_coef)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(5, 6, -1, -1)
        self.label_38 = QLabel(self.offset_g2_coef)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font1)
        self.label_38.setStyleSheet(u"")

        self.verticalLayout_17.addWidget(self.label_38)

        self.label_39 = QLabel(self.offset_g2_coef)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_17.addWidget(self.label_39)

        self.label_40 = QLabel(self.offset_g2_coef)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_17.addWidget(self.label_40)


        self.horizontalLayout_15.addLayout(self.verticalLayout_17)

        self.horizontalSpacer_13 = QSpacerItem(263, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_13)

        self.offset_g2_coef_select = QComboBox(self.offset_g2_coef)
        self.offset_g2_coef_select.addItem("")
        self.offset_g2_coef_select.addItem("")
        self.offset_g2_coef_select.setObjectName(u"offset_g2_coef_select")
        sizePolicy1.setHeightForWidth(self.offset_g2_coef_select.sizePolicy().hasHeightForWidth())
        self.offset_g2_coef_select.setSizePolicy(sizePolicy1)
        self.offset_g2_coef_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_15.addWidget(self.offset_g2_coef_select)


        self.verticalLayout_4.addWidget(self.offset_g2_coef)

        self.g2_coef = QGroupBox(self.setting_scroll_area)
        self.g2_coef.setObjectName(u"g2_coef")
        self.g2_coef.setMinimumSize(QSize(0, 62))
        self.g2_coef.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.g2_coef.setFlat(True)
        self.horizontalLayout_16 = QHBoxLayout(self.g2_coef)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(5, 6, -1, -1)
        self.label_41 = QLabel(self.g2_coef)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font1)
        self.label_41.setStyleSheet(u"")

        self.verticalLayout_18.addWidget(self.label_41)

        self.label_42 = QLabel(self.g2_coef)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_18.addWidget(self.label_42)

        self.label_43 = QLabel(self.g2_coef)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_18.addWidget(self.label_43)


        self.horizontalLayout_16.addLayout(self.verticalLayout_18)

        self.horizontalSpacer_14 = QSpacerItem(233, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_14)

        self.g2_coef_select = QComboBox(self.g2_coef)
        self.g2_coef_select.addItem("")
        self.g2_coef_select.addItem("")
        self.g2_coef_select.addItem("")
        self.g2_coef_select.addItem("")
        self.g2_coef_select.addItem("")
        self.g2_coef_select.setObjectName(u"g2_coef_select")
        sizePolicy1.setHeightForWidth(self.g2_coef_select.sizePolicy().hasHeightForWidth())
        self.g2_coef_select.setSizePolicy(sizePolicy1)
        self.g2_coef_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_16.addWidget(self.g2_coef_select)


        self.verticalLayout_4.addWidget(self.g2_coef)

        self.pga_conf = QGroupBox(self.setting_scroll_area)
        self.pga_conf.setObjectName(u"pga_conf")
        self.pga_conf.setMinimumSize(QSize(0, 50))
        self.pga_conf.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.pga_conf.setFlat(True)
        self.horizontalLayout_17 = QHBoxLayout(self.pga_conf)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(5, 6, -1, -1)
        self.label_44 = QLabel(self.pga_conf)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font1)
        self.label_44.setStyleSheet(u"")

        self.verticalLayout_19.addWidget(self.label_44)

        self.label_45 = QLabel(self.pga_conf)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_19.addWidget(self.label_45)


        self.horizontalLayout_17.addLayout(self.verticalLayout_19)

        self.horizontalSpacer_15 = QSpacerItem(412, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_15)

        self.pga_conf_select = QComboBox(self.pga_conf)
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.addItem("")
        self.pga_conf_select.setObjectName(u"pga_conf_select")
        sizePolicy1.setHeightForWidth(self.pga_conf_select.sizePolicy().hasHeightForWidth())
        self.pga_conf_select.setSizePolicy(sizePolicy1)
        self.pga_conf_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_17.addWidget(self.pga_conf_select)


        self.verticalLayout_4.addWidget(self.pga_conf)

        self.ocal = QGroupBox(self.setting_scroll_area)
        self.ocal.setObjectName(u"ocal")
        self.ocal.setMinimumSize(QSize(0, 50))
        self.ocal.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.ocal.setFlat(True)
        self.horizontalLayout_18 = QHBoxLayout(self.ocal)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(5, 6, -1, -1)
        self.label_46 = QLabel(self.ocal)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font1)
        self.label_46.setStyleSheet(u"")

        self.verticalLayout_20.addWidget(self.label_46)

        self.label_47 = QLabel(self.ocal)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_20.addWidget(self.label_47)


        self.horizontalLayout_18.addLayout(self.verticalLayout_20)

        self.horizontalSpacer_16 = QSpacerItem(301, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_16)

        self.ocal_min = QLabel(self.ocal)
        self.ocal_min.setObjectName(u"ocal_min")
        self.ocal_min.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_18.addWidget(self.ocal_min)

        self.ocal_slider = QSlider(self.ocal)
        self.ocal_slider.setObjectName(u"ocal_slider")
        sizePolicy1.setHeightForWidth(self.ocal_slider.sizePolicy().hasHeightForWidth())
        self.ocal_slider.setSizePolicy(sizePolicy1)
        self.ocal_slider.setMinimumSize(QSize(160, 0))
        self.ocal_slider.setStyleSheet(u"background-color:none\n"
"")
        self.ocal_slider.setMinimum(-128)
        self.ocal_slider.setMaximum(127)
        self.ocal_slider.setOrientation(Qt.Orientation.Horizontal)
        self.ocal_slider.setInvertedAppearance(False)
        self.ocal_slider.setInvertedControls(False)

        self.horizontalLayout_18.addWidget(self.ocal_slider)

        self.ocal_max = QLabel(self.ocal)
        self.ocal_max.setObjectName(u"ocal_max")
        self.ocal_max.setStyleSheet(u"background-color:none\n"
"")

        self.horizontalLayout_18.addWidget(self.ocal_max)

        self.ocal_spin = QSpinBox(self.ocal)
        self.ocal_spin.setObjectName(u"ocal_spin")
        self.ocal_spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.ocal_spin.setMinimum(-128)
        self.ocal_spin.setMaximum(127)
        self.ocal_spin.setSingleStep(1)

        self.horizontalLayout_18.addWidget(self.ocal_spin)


        self.verticalLayout_4.addWidget(self.ocal)

        self.scal = QGroupBox(self.setting_scroll_area)
        self.scal.setObjectName(u"scal")
        self.scal.setMinimumSize(QSize(0, 50))
        self.scal.setStyleSheet(u"QGroupBox {\n"
"	border-top:none;\n"
"	border-bottom:1px solid #C1C7CD;\n"
"}")
        self.scal.setFlat(True)
        self.horizontalLayout_19 = QHBoxLayout(self.scal)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(5, 6, -1, -1)
        self.label_48 = QLabel(self.scal)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font1)
        self.label_48.setStyleSheet(u"")

        self.verticalLayout_21.addWidget(self.label_48)

        self.label_49 = QLabel(self.scal)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_21.addWidget(self.label_49)


        self.horizontalLayout_19.addLayout(self.verticalLayout_21)

        self.horizontalSpacer_17 = QSpacerItem(173, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_17)

        self.scal_select = QComboBox(self.scal)
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.addItem("")
        self.scal_select.setObjectName(u"scal_select")
        sizePolicy1.setHeightForWidth(self.scal_select.sizePolicy().hasHeightForWidth())
        self.scal_select.setSizePolicy(sizePolicy1)
        self.scal_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_19.addWidget(self.scal_select)


        self.verticalLayout_4.addWidget(self.scal)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout_4)

        self.setting_area.setWidget(self.setting_scroll_area)

        self.verticalLayout_13.addWidget(self.setting_area)


        self.verticalLayout.addWidget(self.register_setting_area)

        self.button_area = QWidget(self.main_widget)
        self.button_area.setObjectName(u"button_area")
        self.button_area.setMinimumSize(QSize(0, 40))
        self.button_area.setMaximumSize(QSize(16777215, 40))
        self.button_area.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.button_area)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.preset_select = QComboBox(self.button_area)
        self.preset_select.addItem("")
        self.preset_select.addItem("")
        self.preset_select.addItem("")
        self.preset_select.setObjectName(u"preset_select")
        self.preset_select.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.preset_select)

        self.load_button = QPushButton(self.button_area)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(221, 225, 230);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(200, 205, 210);  /* \u5c11\u3057\u6fc3\u3044 */\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(170, 175, 180);  /* \u3055\u3089\u306b\u6fc3\u3044 */\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.load_button)

        self.save_button = QPushButton(self.button_area)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 29, 108);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 96, 152);\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 17, 64);\n"
"    color: #FFFFFF;\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/RegisterPages/Images/Pages/RegisterPage/save-sharp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.save_button)

        self.button_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.button_spacer)

        self.reset_button = QPushButton(self.button_area)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(221, 225, 230);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(200, 205, 210);  /* \u5c11\u3057\u6fc3\u3044 */\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(170, 175, 180);  /* \u3055\u3089\u306b\u6fc3\u3044 */\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/RegisterPages/Images/Pages/RegisterPage/refresh-sharp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.reset_button.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.reset_button)

        self.write_button = QPushButton(self.button_area)
        self.write_button.setObjectName(u"write_button")
        self.write_button.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 29, 108);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 96, 152);\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 17, 64);\n"
"    color: #FFFFFF;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/RegisterPages/Images/Pages/RegisterPage/upload.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.write_button.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.write_button)

        self.read_button = QPushButton(self.button_area)
        self.read_button.setObjectName(u"read_button")
        self.read_button.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 29, 108);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 96, 152);\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 17, 64);\n"
"    color: #FFFFFF;\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/RegisterPages/Images/Pages/RegisterPage/download.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.read_button.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.read_button)

        self.apply_button = QPushButton(self.button_area)
        self.apply_button.setObjectName(u"apply_button")
        sizePolicy1.setHeightForWidth(self.apply_button.sizePolicy().hasHeightForWidth())
        self.apply_button.setSizePolicy(sizePolicy1)
        self.apply_button.setMinimumSize(QSize(81, 0))
        self.apply_button.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(15, 98, 254);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(35, 118, 255);\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(10, 78, 204);\n"
"    color: #FFFFFF;\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.apply_button)


        self.verticalLayout.addWidget(self.button_area)

        register_page.setCentralWidget(self.main_widget)

        self.retranslateUi(register_page)

        QMetaObject.connectSlotsByName(register_page)
    # setupUi

    def retranslateUi(self, register_page):
        register_page.setWindowTitle(QCoreApplication.translate("register_page", u"Register Setting", None))
        self.select_channel_label.setText(QCoreApplication.translate("register_page", u"Select Channel", None))
        self.ch_select.setItemText(0, QCoreApplication.translate("register_page", u"#1", None))
        self.ch_select.setItemText(1, QCoreApplication.translate("register_page", u"#2", None))
        self.ch_select.setItemText(2, QCoreApplication.translate("register_page", u"#3", None))
        self.ch_select.setItemText(3, QCoreApplication.translate("register_page", u"#4", None))

        self.help_button.setText(QCoreApplication.translate("register_page", u"Data Sheet", None))
        self.output_mode.setTitle("")
        self.label.setText(QCoreApplication.translate("register_page", u"Output Mode", None))
        self.label_2.setText(QCoreApplication.translate("register_page", u"Set the output mode.", None))
        self.output_mode_select.setItemText(0, QCoreApplication.translate("register_page", u"Digital Output Mode", None))
        self.output_mode_select.setItemText(1, QCoreApplication.translate("register_page", u"Analog Output Mode", None))

        self.osr.setTitle("")
        self.label_3.setText(QCoreApplication.translate("register_page", u"OSR", None))
        self.label_4.setText(QCoreApplication.translate("register_page", u"Set the ADC and DAC oversampling rates.", None))
        self.osr_select.setItemText(0, QCoreApplication.translate("register_page", u"ADC:192, DAC:32, Input Bandwidth:5449", None))
        self.osr_select.setItemText(1, QCoreApplication.translate("register_page", u"ADC:384, DAC:64, Input Bandwidth:2725", None))
        self.osr_select.setItemText(2, QCoreApplication.translate("register_page", u"ADC:768, DAC:128, Input Bandwidth:1365", None))
        self.osr_select.setItemText(3, QCoreApplication.translate("register_page", u"ADC:1536, DAC:-, Input Bandwidth:681", None))

        self.register_refresh_operation.setTitle("")
        self.label_5.setText(QCoreApplication.translate("register_page", u"Register Refresh Operation", None))
        self.label_6.setText(QCoreApplication.translate("register_page", u"Enable/Disable register refresh operation.", None))
        self.register_refresh_op_select.setItemText(0, QCoreApplication.translate("register_page", u"Disable", None))
        self.register_refresh_op_select.setItemText(1, QCoreApplication.translate("register_page", u"Enable", None))

        self.label_7.setText(QCoreApplication.translate("register_page", u"Sensor ID", None))
        self.label_8.setText(QCoreApplication.translate("register_page", u"Set the ID for device recognition.", None))
        self.sensor_id_select.setItemText(0, QCoreApplication.translate("register_page", u"0", None))
        self.sensor_id_select.setItemText(1, QCoreApplication.translate("register_page", u"1", None))
        self.sensor_id_select.setItemText(2, QCoreApplication.translate("register_page", u"2", None))
        self.sensor_id_select.setItemText(3, QCoreApplication.translate("register_page", u"3", None))

        self.label_9.setText(QCoreApplication.translate("register_page", u"Reference Temperature for Calibration", None))
        self.label_10.setText(QCoreApplication.translate("register_page", u"Set the reference temperature for temperature compensation.", None))
        self.temp_orig_min.setText(QCoreApplication.translate("register_page", u"-128", None))
        self.temp_orig_max.setText(QCoreApplication.translate("register_page", u"127", None))
        self.label_13.setText(QCoreApplication.translate("register_page", u"Temperature Threshold", None))
        self.label_14.setText(QCoreApplication.translate("register_page", u"Set the temperature threshold to switch coefficients for", None))
        self.label_15.setText(QCoreApplication.translate("register_page", u"temperature compensation.", None))
        self.temp_th0_min.setText(QCoreApplication.translate("register_page", u"-128", None))
        self.temp_th0_max.setText(QCoreApplication.translate("register_page", u"127", None))
        self.label_18.setText(QCoreApplication.translate("register_page", u"Offset Correction Coefficient", None))
        self.label_19.setText(QCoreApplication.translate("register_page", u"Set the sensitivity correction coefficient.", None))
        self.offset_coef0_min.setText(QCoreApplication.translate("register_page", u"-2.0", None))
        self.offset_coef0_max.setText(QCoreApplication.translate("register_page", u"2.0", None))
        self.label_20.setText(QCoreApplication.translate("register_page", u"Temperature Offst Correction Coefficient", None))
        self.label_21.setText(QCoreApplication.translate("register_page", u"Set the temperature sensitivity correction coefficient.", None))
        self.offset_temp_coef0_min.setText(QCoreApplication.translate("register_page", u"-1.0", None))
        self.offset_temp_coef0_max.setText(QCoreApplication.translate("register_page", u"1.0", None))
        self.label_26.setText(QCoreApplication.translate("register_page", u"Offset Correction Coefficient1", None))
        self.label_27.setText(QCoreApplication.translate("register_page", u"Set the sensitivity correction coefficient1.", None))
        self.offset_coef1_min.setText(QCoreApplication.translate("register_page", u"-2.0", None))
        self.offset_coef1_max.setText(QCoreApplication.translate("register_page", u"2.0", None))
        self.label_30.setText(QCoreApplication.translate("register_page", u"Temperature Offst Correction Coefficient1", None))
        self.label_31.setText(QCoreApplication.translate("register_page", u"Set the temperature sensitivity correction coefficient1.", None))
        self.offset_temp_coef1_min.setText(QCoreApplication.translate("register_page", u"-1.0", None))
        self.offset_temp_coef1_max.setText(QCoreApplication.translate("register_page", u"1.0", None))
        self.label_32.setText(QCoreApplication.translate("register_page", u"Digital Compensation (Offset Coefficient)", None))
        self.label_33.setText(QCoreApplication.translate("register_page", u"Set the offset coefficient for full-scale adjustment in digital", None))
        self.label_34.setText(QCoreApplication.translate("register_page", u"compensation.", None))
        self.fsadj_offset_coef_min.setText(QCoreApplication.translate("register_page", u"-2.0", None))
        self.fsadj_offset_coef_max.setText(QCoreApplication.translate("register_page", u"2.0", None))
        self.label_35.setText(QCoreApplication.translate("register_page", u"Digital Compensation (Gain Coefficient)", None))
        self.label_36.setText(QCoreApplication.translate("register_page", u"Set the gain coefficient for full-scale adjustment in digital ", None))
        self.label_37.setText(QCoreApplication.translate("register_page", u"compensation.", None))
        self.fsadj_gain_coef_min.setText(QCoreApplication.translate("register_page", u"-2.0", None))
        self.fsadj_gain_coef_max.setText(QCoreApplication.translate("register_page", u"2.0", None))
        self.label_38.setText(QCoreApplication.translate("register_page", u"Digital Compensation (Offset Adjustment)", None))
        self.label_39.setText(QCoreApplication.translate("register_page", u"Adjust the offset value in digital compensation.", None))
        self.label_40.setText(QCoreApplication.translate("register_page", u"Please align the setting with the PGA gain.", None))
        self.offset_g2_coef_select.setItemText(0, QCoreApplication.translate("register_page", u"1x", None))
        self.offset_g2_coef_select.setItemText(1, QCoreApplication.translate("register_page", u"2x", None))

        self.label_41.setText(QCoreApplication.translate("register_page", u"Digital Compensation (Gain)", None))
        self.label_42.setText(QCoreApplication.translate("register_page", u"Set the gain in digital compensation.", None))
        self.label_43.setText(QCoreApplication.translate("register_page", u"Use 2\u201316\u00d7 settings only when PGA gain is set to 50\u00d7.", None))
        self.g2_coef_select.setItemText(0, QCoreApplication.translate("register_page", u"1x", None))
        self.g2_coef_select.setItemText(1, QCoreApplication.translate("register_page", u"2x", None))
        self.g2_coef_select.setItemText(2, QCoreApplication.translate("register_page", u"4x", None))
        self.g2_coef_select.setItemText(3, QCoreApplication.translate("register_page", u"8x", None))
        self.g2_coef_select.setItemText(4, QCoreApplication.translate("register_page", u"16x", None))

        self.label_44.setText(QCoreApplication.translate("register_page", u"PGA Gain Setting", None))
        self.label_45.setText(QCoreApplication.translate("register_page", u"Set the PGA gain.", None))
        self.pga_conf_select.setItemText(0, QCoreApplication.translate("register_page", u"50", None))
        self.pga_conf_select.setItemText(1, QCoreApplication.translate("register_page", u"62.5", None))
        self.pga_conf_select.setItemText(2, QCoreApplication.translate("register_page", u"83.3", None))
        self.pga_conf_select.setItemText(3, QCoreApplication.translate("register_page", u"125", None))
        self.pga_conf_select.setItemText(4, QCoreApplication.translate("register_page", u"41.7", None))
        self.pga_conf_select.setItemText(5, QCoreApplication.translate("register_page", u"31.3", None))
        self.pga_conf_select.setItemText(6, QCoreApplication.translate("register_page", u"25", None))
        self.pga_conf_select.setItemText(7, QCoreApplication.translate("register_page", u"8.3", None))

        self.label_46.setText(QCoreApplication.translate("register_page", u"Offset Adjustment for PGA", None))
        self.label_47.setText(QCoreApplication.translate("register_page", u"Set the offset adjustment for PGA.", None))
        self.ocal_min.setText(QCoreApplication.translate("register_page", u"-128", None))
        self.ocal_max.setText(QCoreApplication.translate("register_page", u"127", None))
        self.label_48.setText(QCoreApplication.translate("register_page", u"Sensor Excitation Current [mA]", None))
        self.label_49.setText(QCoreApplication.translate("register_page", u"Set the sensitivity correction using the excitation current source.", None))
        self.scal_select.setItemText(0, QCoreApplication.translate("register_page", u"1.868", None))
        self.scal_select.setItemText(1, QCoreApplication.translate("register_page", u"1.945", None))
        self.scal_select.setItemText(2, QCoreApplication.translate("register_page", u"2.022", None))
        self.scal_select.setItemText(3, QCoreApplication.translate("register_page", u"2.098", None))
        self.scal_select.setItemText(4, QCoreApplication.translate("register_page", u"2.175", None))
        self.scal_select.setItemText(5, QCoreApplication.translate("register_page", u"2.251", None))
        self.scal_select.setItemText(6, QCoreApplication.translate("register_page", u"2.326", None))
        self.scal_select.setItemText(7, QCoreApplication.translate("register_page", u"2.401", None))
        self.scal_select.setItemText(8, QCoreApplication.translate("register_page", u"1.791", None))
        self.scal_select.setItemText(9, QCoreApplication.translate("register_page", u"1.714", None))
        self.scal_select.setItemText(10, QCoreApplication.translate("register_page", u"1.636", None))
        self.scal_select.setItemText(11, QCoreApplication.translate("register_page", u"1.559", None))
        self.scal_select.setItemText(12, QCoreApplication.translate("register_page", u"1.482", None))
        self.scal_select.setItemText(13, QCoreApplication.translate("register_page", u"1.404", None))
        self.scal_select.setItemText(14, QCoreApplication.translate("register_page", u"1.327", None))
        self.scal_select.setItemText(15, QCoreApplication.translate("register_page", u"1.249", None))

        self.preset_select.setItemText(0, QCoreApplication.translate("register_page", u"Preset 1", None))
        self.preset_select.setItemText(1, QCoreApplication.translate("register_page", u"Preset 2", None))
        self.preset_select.setItemText(2, QCoreApplication.translate("register_page", u"Preset 3", None))

        self.load_button.setText(QCoreApplication.translate("register_page", u"Load Preset", None))
        self.save_button.setText(QCoreApplication.translate("register_page", u"Save Preset", None))
        self.reset_button.setText(QCoreApplication.translate("register_page", u"Restore Defaults", None))
        self.write_button.setText(QCoreApplication.translate("register_page", u"Write", None))
        self.read_button.setText(QCoreApplication.translate("register_page", u"Read", None))
        self.apply_button.setText(QCoreApplication.translate("register_page", u"Apply", None))
    # retranslateUi

