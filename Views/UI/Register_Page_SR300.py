# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Register_Page_SR300.ui'
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
        register_page.resize(872, 660)
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

        self.help_button_sr300 = QPushButton(self.help_area)
        self.help_button_sr300.setObjectName(u"help_button_sr300")
        self.help_button_sr300.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/RegisterPages/Images/Pages/RegisterPage/help-circle-sharp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.help_button_sr300.setIcon(icon)
        self.help_button_sr300.setIconSize(QSize(20, 20))
        self.help_button_sr300.setFlat(True)

        self.horizontalLayout_3.addWidget(self.help_button_sr300)


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
        self.setting_scroll_area.setGeometry(QRect(0, 0, 828, 600))
        self.setting_scroll_area.setMinimumSize(QSize(500, 600))
        self.setting_scroll_area.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.setting_scroll_area)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.gain = QGroupBox(self.setting_scroll_area)
        self.gain.setObjectName(u"gain")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gain.sizePolicy().hasHeightForWidth())
        self.gain.setSizePolicy(sizePolicy1)
        self.gain.setMinimumSize(QSize(0, 50))
        self.gain.setMaximumSize(QSize(16777215, 50))
        self.gain.setStyleSheet(u"")
        self.gain.setFlat(True)
        self.horizontalLayout = QHBoxLayout(self.gain)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 6, -1, -1)
        self.label = QLabel(self.gain)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(10)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.gain)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color:rgb(135, 141, 150)")

        self.verticalLayout_3.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer = QSpacerItem(399, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.gain_select = QComboBox(self.gain)
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.addItem("")
        self.gain_select.setObjectName(u"gain_select")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gain_select.sizePolicy().hasHeightForWidth())
        self.gain_select.setSizePolicy(sizePolicy2)
        self.gain_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout.addWidget(self.gain_select)


        self.verticalLayout_4.addWidget(self.gain)

        self.osr = QGroupBox(self.setting_scroll_area)
        self.osr.setObjectName(u"osr")
        sizePolicy1.setHeightForWidth(self.osr.sizePolicy().hasHeightForWidth())
        self.osr.setSizePolicy(sizePolicy1)
        self.osr.setMinimumSize(QSize(0, 50))
        self.osr.setMaximumSize(QSize(16777215, 50))
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

        self.sg_min = QLabel(self.osr)
        self.sg_min.setObjectName(u"sg_min")

        self.horizontalLayout_4.addWidget(self.sg_min)

        self.sg_slider = QSlider(self.osr)
        self.sg_slider.setObjectName(u"sg_slider")
        sizePolicy2.setHeightForWidth(self.sg_slider.sizePolicy().hasHeightForWidth())
        self.sg_slider.setSizePolicy(sizePolicy2)
        self.sg_slider.setMinimumSize(QSize(160, 0))
        self.sg_slider.setMinimum(-125)
        self.sg_slider.setMaximum(124)
        self.sg_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.sg_slider)

        self.sg_max = QLabel(self.osr)
        self.sg_max.setObjectName(u"sg_max")

        self.horizontalLayout_4.addWidget(self.sg_max)

        self.sg_spin = QSpinBox(self.osr)
        self.sg_spin.setObjectName(u"sg_spin")
        self.sg_spin.setMinimumSize(QSize(78, 0))

        self.horizontalLayout_4.addWidget(self.sg_spin)


        self.verticalLayout_4.addWidget(self.osr)

        self.register_refresh_operation = QGroupBox(self.setting_scroll_area)
        self.register_refresh_operation.setObjectName(u"register_refresh_operation")
        self.register_refresh_operation.setMinimumSize(QSize(0, 50))
        self.register_refresh_operation.setMaximumSize(QSize(16777215, 50))
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

        self.dofs_min = QLabel(self.register_refresh_operation)
        self.dofs_min.setObjectName(u"dofs_min")

        self.horizontalLayout_5.addWidget(self.dofs_min)

        self.dofs_slider = QSlider(self.register_refresh_operation)
        self.dofs_slider.setObjectName(u"dofs_slider")
        sizePolicy2.setHeightForWidth(self.dofs_slider.sizePolicy().hasHeightForWidth())
        self.dofs_slider.setSizePolicy(sizePolicy2)
        self.dofs_slider.setMinimumSize(QSize(160, 0))
        self.dofs_slider.setMinimum(-635)
        self.dofs_slider.setSingleStep(10)
        self.dofs_slider.setSliderPosition(0)
        self.dofs_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.dofs_slider)

        self.dofs_max = QLabel(self.register_refresh_operation)
        self.dofs_max.setObjectName(u"dofs_max")

        self.horizontalLayout_5.addWidget(self.dofs_max)

        self.dofs_max_2 = QSpinBox(self.register_refresh_operation)
        self.dofs_max_2.setObjectName(u"dofs_max_2")
        self.dofs_max_2.setMinimumSize(QSize(78, 0))

        self.horizontalLayout_5.addWidget(self.dofs_max_2)


        self.verticalLayout_4.addWidget(self.register_refresh_operation)

        self.groupBox_4 = QGroupBox(self.setting_scroll_area)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 50))
        self.groupBox_4.setMaximumSize(QSize(16777215, 50))
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
        sizePolicy2.setHeightForWidth(self.sensor_id_select.sizePolicy().hasHeightForWidth())
        self.sensor_id_select.setSizePolicy(sizePolicy2)
        self.sensor_id_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_6.addWidget(self.sensor_id_select)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.setting_scroll_area)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 50))
        self.groupBox_5.setMaximumSize(QSize(16777215, 50))
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

        self.ads_select = QComboBox(self.groupBox_5)
        self.ads_select.addItem("")
        self.ads_select.addItem("")
        self.ads_select.addItem("")
        self.ads_select.addItem("")
        self.ads_select.setObjectName(u"ads_select")
        sizePolicy2.setHeightForWidth(self.ads_select.sizePolicy().hasHeightForWidth())
        self.ads_select.setSizePolicy(sizePolicy2)
        self.ads_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_7.addWidget(self.ads_select)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.setting_scroll_area)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 50))
        self.groupBox_6.setMaximumSize(QSize(16777215, 50))
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


        self.horizontalLayout_8.addLayout(self.verticalLayout_9)

        self.horizontalSpacer_6 = QSpacerItem(190, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.st_range_select = QComboBox(self.groupBox_6)
        self.st_range_select.addItem("")
        self.st_range_select.addItem("")
        self.st_range_select.setObjectName(u"st_range_select")
        sizePolicy2.setHeightForWidth(self.st_range_select.sizePolicy().hasHeightForWidth())
        self.st_range_select.setSizePolicy(sizePolicy2)
        self.st_range_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_8.addWidget(self.st_range_select)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.setting_scroll_area)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(0, 50))
        self.groupBox_7.setMaximumSize(QSize(16777215, 50))
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

        self.tsdis0_select = QComboBox(self.groupBox_7)
        self.tsdis0_select.addItem("")
        self.tsdis0_select.addItem("")
        self.tsdis0_select.setObjectName(u"tsdis0_select")
        sizePolicy2.setHeightForWidth(self.tsdis0_select.sizePolicy().hasHeightForWidth())
        self.tsdis0_select.setSizePolicy(sizePolicy2)
        self.tsdis0_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_9.addWidget(self.tsdis0_select)


        self.verticalLayout_4.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.setting_scroll_area)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(0, 50))
        self.groupBox_8.setMaximumSize(QSize(16777215, 50))
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

        self.tsdis1_select = QComboBox(self.groupBox_8)
        self.tsdis1_select.addItem("")
        self.tsdis1_select.addItem("")
        self.tsdis1_select.setObjectName(u"tsdis1_select")
        sizePolicy2.setHeightForWidth(self.tsdis1_select.sizePolicy().hasHeightForWidth())
        self.tsdis1_select.setSizePolicy(sizePolicy2)
        self.tsdis1_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_10.addWidget(self.tsdis1_select)


        self.verticalLayout_4.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.setting_scroll_area)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(0, 50))
        self.groupBox_9.setMaximumSize(QSize(16777215, 50))
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

        self.tsmod_select = QComboBox(self.groupBox_9)
        self.tsmod_select.addItem("")
        self.tsmod_select.addItem("")
        self.tsmod_select.setObjectName(u"tsmod_select")
        sizePolicy2.setHeightForWidth(self.tsmod_select.sizePolicy().hasHeightForWidth())
        self.tsmod_select.setSizePolicy(sizePolicy2)
        self.tsmod_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_11.addWidget(self.tsmod_select)


        self.verticalLayout_4.addWidget(self.groupBox_9)

        self.offset_temp_coef1 = QGroupBox(self.setting_scroll_area)
        self.offset_temp_coef1.setObjectName(u"offset_temp_coef1")
        self.offset_temp_coef1.setMinimumSize(QSize(0, 50))
        self.offset_temp_coef1.setMaximumSize(QSize(16777215, 50))
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

        self.drvsel_select = QComboBox(self.offset_temp_coef1)
        self.drvsel_select.addItem("")
        self.drvsel_select.addItem("")
        self.drvsel_select.setObjectName(u"drvsel_select")
        sizePolicy2.setHeightForWidth(self.drvsel_select.sizePolicy().hasHeightForWidth())
        self.drvsel_select.setSizePolicy(sizePolicy2)
        self.drvsel_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_12.addWidget(self.drvsel_select)


        self.verticalLayout_4.addWidget(self.offset_temp_coef1)

        self.fsadj_offset_coef = QGroupBox(self.setting_scroll_area)
        self.fsadj_offset_coef.setObjectName(u"fsadj_offset_coef")
        self.fsadj_offset_coef.setMinimumSize(QSize(0, 50))
        self.fsadj_offset_coef.setMaximumSize(QSize(16777215, 50))
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


        self.horizontalLayout_13.addLayout(self.verticalLayout_15)

        self.horizontalSpacer_11 = QSpacerItem(175, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)

        self.tofs_select = QComboBox(self.fsadj_offset_coef)
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.addItem("")
        self.tofs_select.setObjectName(u"tofs_select")
        sizePolicy2.setHeightForWidth(self.tofs_select.sizePolicy().hasHeightForWidth())
        self.tofs_select.setSizePolicy(sizePolicy2)
        self.tofs_select.setMinimumSize(QSize(265, 0))

        self.horizontalLayout_13.addWidget(self.tofs_select)


        self.verticalLayout_4.addWidget(self.fsadj_offset_coef)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

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
        sizePolicy2.setHeightForWidth(self.apply_button.sizePolicy().hasHeightForWidth())
        self.apply_button.setSizePolicy(sizePolicy2)
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

        self.help_button_sr300.setText(QCoreApplication.translate("register_page", u"Data Sheet", None))
        self.gain.setTitle("")
        self.label.setText(QCoreApplication.translate("register_page", u"Amplifier Gain Adjustment", None))
        self.label_2.setText(QCoreApplication.translate("register_page", u"Adjust the sensor gain and measurement range.", None))
        self.gain_select.setItemText(0, QCoreApplication.translate("register_page", u"8.0", None))
        self.gain_select.setItemText(1, QCoreApplication.translate("register_page", u"15.8", None))
        self.gain_select.setItemText(2, QCoreApplication.translate("register_page", u"31.4", None))
        self.gain_select.setItemText(3, QCoreApplication.translate("register_page", u"65.1", None))
        self.gain_select.setItemText(4, QCoreApplication.translate("register_page", u"120", None))
        self.gain_select.setItemText(5, QCoreApplication.translate("register_page", u"248", None))
        self.gain_select.setItemText(6, QCoreApplication.translate("register_page", u"504", None))
        self.gain_select.setItemText(7, QCoreApplication.translate("register_page", u"1016", None))

        self.osr.setTitle("")
        self.label_3.setText(QCoreApplication.translate("register_page", u"Sensor Sensitivity Fine Adjustment", None))
        self.label_4.setText(QCoreApplication.translate("register_page", u"Fine-tune the sensor sensitivity.", None))
        self.sg_min.setText(QCoreApplication.translate("register_page", u"-12.5", None))
        self.sg_max.setText(QCoreApplication.translate("register_page", u"12.4", None))
        self.register_refresh_operation.setTitle("")
        self.label_5.setText(QCoreApplication.translate("register_page", u"Internal Offset Adjustment", None))
        self.label_6.setText(QCoreApplication.translate("register_page", u"Adjust the initial offset value.", None))
        self.dofs_min.setText(QCoreApplication.translate("register_page", u"-63.5", None))
        self.dofs_max.setText(QCoreApplication.translate("register_page", u"63.5", None))
        self.label_7.setText(QCoreApplication.translate("register_page", u"Sensor ID", None))
        self.label_8.setText(QCoreApplication.translate("register_page", u"Set the ID for device recognition.", None))
        self.sensor_id_select.setItemText(0, QCoreApplication.translate("register_page", u"0", None))
        self.sensor_id_select.setItemText(1, QCoreApplication.translate("register_page", u"1", None))
        self.sensor_id_select.setItemText(2, QCoreApplication.translate("register_page", u"2", None))
        self.sensor_id_select.setItemText(3, QCoreApplication.translate("register_page", u"3", None))

        self.label_9.setText(QCoreApplication.translate("register_page", u"Sampling Frequency", None))
        self.label_10.setText(QCoreApplication.translate("register_page", u"Set the A/D converter sampling frequency.", None))
        self.ads_select.setItemText(0, QCoreApplication.translate("register_page", u"1.25KHz", None))
        self.ads_select.setItemText(1, QCoreApplication.translate("register_page", u"2.5KHz", None))
        self.ads_select.setItemText(2, QCoreApplication.translate("register_page", u"5.0KHz", None))
        self.ads_select.setItemText(3, QCoreApplication.translate("register_page", u"10.0KHz", None))

        self.label_13.setText(QCoreApplication.translate("register_page", u"Strain Measurement Range", None))
        self.label_14.setText(QCoreApplication.translate("register_page", u"Set the measurable strain range.", None))
        self.st_range_select.setItemText(0, QCoreApplication.translate("register_page", u"about 1u\u03b5", None))
        self.st_range_select.setItemText(1, QCoreApplication.translate("register_page", u"about 0.5u\u03b5", None))

        self.label_18.setText(QCoreApplication.translate("register_page", u"Temperature Sensor Output 1", None))
        self.label_19.setText(QCoreApplication.translate("register_page", u"Configure the output format for temperature measurement.", None))
        self.tsdis0_select.setItemText(0, QCoreApplication.translate("register_page", u"Digital Output Enabled", None))
        self.tsdis0_select.setItemText(1, QCoreApplication.translate("register_page", u"Digital Output Disabled", None))

        self.label_20.setText(QCoreApplication.translate("register_page", u"Temperature Sensor Output 2", None))
        self.label_21.setText(QCoreApplication.translate("register_page", u"Configure the output format for temperature measurement.", None))
        self.tsdis1_select.setItemText(0, QCoreApplication.translate("register_page", u"Analog Output Enabled", None))
        self.tsdis1_select.setItemText(1, QCoreApplication.translate("register_page", u"Analog Output Disabled", None))

        self.label_26.setText(QCoreApplication.translate("register_page", u"Temperature Resolution", None))
        self.label_27.setText(QCoreApplication.translate("register_page", u"Set the temperature resolution.", None))
        self.tsmod_select.setItemText(0, QCoreApplication.translate("register_page", u"1\u2103", None))
        self.tsmod_select.setItemText(1, QCoreApplication.translate("register_page", u"0.0625\u2103", None))

        self.label_30.setText(QCoreApplication.translate("register_page", u"Output Driver Setting", None))
        self.label_31.setText(QCoreApplication.translate("register_page", u"Switch the current drive capability.", None))
        self.drvsel_select.setItemText(0, QCoreApplication.translate("register_page", u"Output Current \u00b130\u03bcA", None))
        self.drvsel_select.setItemText(1, QCoreApplication.translate("register_page", u"Output Current \u00b12mA", None))

        self.label_32.setText(QCoreApplication.translate("register_page", u"Offset Temperature Compensation", None))
        self.label_33.setText(QCoreApplication.translate("register_page", u"Compensate for offset drift due to temperature changes.", None))
        self.tofs_select.setItemText(0, QCoreApplication.translate("register_page", u"50.0", None))
        self.tofs_select.setItemText(1, QCoreApplication.translate("register_page", u"25.0", None))
        self.tofs_select.setItemText(2, QCoreApplication.translate("register_page", u"12.5", None))
        self.tofs_select.setItemText(3, QCoreApplication.translate("register_page", u"6.25", None))
        self.tofs_select.setItemText(4, QCoreApplication.translate("register_page", u"3.125", None))
        self.tofs_select.setItemText(5, QCoreApplication.translate("register_page", u"1.5625", None))
        self.tofs_select.setItemText(6, QCoreApplication.translate("register_page", u"0.78125", None))
        self.tofs_select.setItemText(7, QCoreApplication.translate("register_page", u"0.0", None))
        self.tofs_select.setItemText(8, QCoreApplication.translate("register_page", u"-0.78125", None))
        self.tofs_select.setItemText(9, QCoreApplication.translate("register_page", u"-1.5625", None))
        self.tofs_select.setItemText(10, QCoreApplication.translate("register_page", u"-3.125", None))
        self.tofs_select.setItemText(11, QCoreApplication.translate("register_page", u"-6.25", None))
        self.tofs_select.setItemText(12, QCoreApplication.translate("register_page", u"-12.5", None))
        self.tofs_select.setItemText(13, QCoreApplication.translate("register_page", u"-25.0", None))
        self.tofs_select.setItemText(14, QCoreApplication.translate("register_page", u"-50.0", None))

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

