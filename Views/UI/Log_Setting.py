# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Log_Setting.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)
from Views import resources_rc

class Ui_log_setting_tab(object):
    def setupUi(self, log_setting_tab):
        if not log_setting_tab.objectName():
            log_setting_tab.setObjectName(u"log_setting_tab")
        log_setting_tab.resize(717, 614)
        log_setting_tab.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(log_setting_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption = QLabel(log_setting_tab)
        self.caption.setObjectName(u"caption")
        font = QFont()
        font.setPointSize(11)
        self.caption.setFont(font)

        self.verticalLayout.addWidget(self.caption)

        self.log_settings_label = QLabel(log_setting_tab)
        self.log_settings_label.setObjectName(u"log_settings_label")
        self.log_settings_label.setFont(font)

        self.verticalLayout.addWidget(self.log_settings_label)

        self.line_2 = QFrame(log_setting_tab)
        self.line_2.setObjectName(u"line_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMinimumSize(QSize(500, 0))
        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(2)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.autosave_area = QQuickWidget(log_setting_tab)
        self.autosave_area.setObjectName(u"autosave_area")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.autosave_area.sizePolicy().hasHeightForWidth())
        self.autosave_area.setSizePolicy(sizePolicy1)
        self.autosave_area.setMinimumSize(QSize(500, 90))
        self.autosave_area.setMaximumSize(QSize(500, 16777215))
        self.autosave_area.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.autosave_area.setSource(QUrl(u"qrc:/qml/qml/auto_save.qml"))

        self.verticalLayout.addWidget(self.autosave_area)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.log_location_label = QLabel(log_setting_tab)
        self.log_location_label.setObjectName(u"log_location_label")
        font1 = QFont()
        font1.setBold(True)
        self.log_location_label.setFont(font1)

        self.verticalLayout.addWidget(self.log_location_label)

        self.log_location_area = QWidget(log_setting_tab)
        self.log_location_area.setObjectName(u"log_location_area")
        self.log_location_area.setMinimumSize(QSize(400, 0))
        self.log_location_area.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout = QHBoxLayout(self.log_location_area)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.log_location_edit = QLineEdit(self.log_location_area)
        self.log_location_edit.setObjectName(u"log_location_edit")

        self.horizontalLayout.addWidget(self.log_location_edit)

        self.log_location_select_button = QPushButton(self.log_location_area)
        self.log_location_select_button.setObjectName(u"log_location_select_button")
        sizePolicy.setHeightForWidth(self.log_location_select_button.sizePolicy().hasHeightForWidth())
        self.log_location_select_button.setSizePolicy(sizePolicy)
        self.log_location_select_button.setMinimumSize(QSize(50, 0))
        self.log_location_select_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.log_location_select_button)


        self.verticalLayout.addWidget(self.log_location_area)

        self.prefix_label = QLabel(log_setting_tab)
        self.prefix_label.setObjectName(u"prefix_label")
        self.prefix_label.setFont(font1)

        self.verticalLayout.addWidget(self.prefix_label)

        self.prefix_edit = QLineEdit(log_setting_tab)
        self.prefix_edit.setObjectName(u"prefix_edit")
        sizePolicy.setHeightForWidth(self.prefix_edit.sizePolicy().hasHeightForWidth())
        self.prefix_edit.setSizePolicy(sizePolicy)
        self.prefix_edit.setMinimumSize(QSize(297, 0))

        self.verticalLayout.addWidget(self.prefix_edit)

        self.sample_count_label = QLabel(log_setting_tab)
        self.sample_count_label.setObjectName(u"sample_count_label")
        self.sample_count_label.setFont(font1)

        self.verticalLayout.addWidget(self.sample_count_label)

        self.sample_count_edit = QSpinBox(log_setting_tab)
        self.sample_count_edit.setObjectName(u"sample_count_edit")
        self.sample_count_edit.setMinimumSize(QSize(200, 0))
        self.sample_count_edit.setMaximumSize(QSize(200, 16777215))
        self.sample_count_edit.setMinimum(1)
        self.sample_count_edit.setMaximum(300000)

        self.verticalLayout.addWidget(self.sample_count_edit)

        self.sample_time_label = QLabel(log_setting_tab)
        self.sample_time_label.setObjectName(u"sample_time_label")

        self.verticalLayout.addWidget(self.sample_time_label)

        self.sample_size_label = QLabel(log_setting_tab)
        self.sample_size_label.setObjectName(u"sample_size_label")

        self.verticalLayout.addWidget(self.sample_size_label)

        self.verticalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.capture_settings_label = QLabel(log_setting_tab)
        self.capture_settings_label.setObjectName(u"capture_settings_label")
        self.capture_settings_label.setMinimumSize(QSize(0, 0))
        self.capture_settings_label.setFont(font)

        self.verticalLayout.addWidget(self.capture_settings_label)

        self.line = QFrame(log_setting_tab)
        self.line.setObjectName(u"line")
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QSize(500, 0))
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(2)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.capture_location_label = QLabel(log_setting_tab)
        self.capture_location_label.setObjectName(u"capture_location_label")
        self.capture_location_label.setFont(font1)

        self.verticalLayout.addWidget(self.capture_location_label)

        self.capture_location_area = QWidget(log_setting_tab)
        self.capture_location_area.setObjectName(u"capture_location_area")
        self.capture_location_area.setMinimumSize(QSize(400, 0))
        self.capture_location_area.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.capture_location_area)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.capture_location_edit = QLineEdit(self.capture_location_area)
        self.capture_location_edit.setObjectName(u"capture_location_edit")

        self.horizontalLayout_2.addWidget(self.capture_location_edit)

        self.capture_location_select_button = QPushButton(self.capture_location_area)
        self.capture_location_select_button.setObjectName(u"capture_location_select_button")
        self.capture_location_select_button.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.capture_location_select_button)


        self.verticalLayout.addWidget(self.capture_location_area)

        self.bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottom_spacer)


        self.retranslateUi(log_setting_tab)

        QMetaObject.connectSlotsByName(log_setting_tab)
    # setupUi

    def retranslateUi(self, log_setting_tab):
        log_setting_tab.setWindowTitle(QCoreApplication.translate("log_setting_tab", u"Form", None))
        self.caption.setText(QCoreApplication.translate("log_setting_tab", u"Configure log save options.", None))
        self.log_settings_label.setText(QCoreApplication.translate("log_setting_tab", u"Log Settings", None))
        self.log_location_label.setText(QCoreApplication.translate("log_setting_tab", u"Save Location", None))
        self.log_location_select_button.setText(QCoreApplication.translate("log_setting_tab", u"Browse...", None))
        self.prefix_label.setText(QCoreApplication.translate("log_setting_tab", u"Prefix", None))
        self.sample_count_label.setText(QCoreApplication.translate("log_setting_tab", u"Sample Count (1 ~ 300000)", None))
        self.sample_time_label.setText(QCoreApplication.translate("log_setting_tab", u"0d 00h 00m 00.000000s", None))
        self.sample_size_label.setText(QCoreApplication.translate("log_setting_tab", u"0 MB/File", None))
        self.capture_settings_label.setText(QCoreApplication.translate("log_setting_tab", u"Screen Capture Settings", None))
        self.capture_location_label.setText(QCoreApplication.translate("log_setting_tab", u"Save Location", None))
        self.capture_location_select_button.setText(QCoreApplication.translate("log_setting_tab", u"Browse...", None))
    # retranslateUi

