# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_setting.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_net_setting_tab(object):
    def setupUi(self, net_setting_tab):
        if not net_setting_tab.objectName():
            net_setting_tab.setObjectName(u"net_setting_tab")
        net_setting_tab.resize(563, 303)
        net_setting_tab.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(net_setting_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption = QLabel(net_setting_tab)
        self.caption.setObjectName(u"caption")
        font = QFont()
        font.setPointSize(11)
        self.caption.setFont(font)

        self.verticalLayout.addWidget(self.caption)

        self.device1 = QWidget(net_setting_tab)
        self.device1.setObjectName(u"device1")
        self.device1.setMinimumSize(QSize(400, 0))
        self.device1.setMaximumSize(QSize(400, 16777215))
        self.gridLayout = QGridLayout(self.device1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.device1_label = QLabel(self.device1)
        self.device1_label.setObjectName(u"device1_label")

        self.gridLayout.addWidget(self.device1_label, 0, 0, 1, 1)

        self.device1_ip = QLineEdit(self.device1)
        self.device1_ip.setObjectName(u"device1_ip")

        self.gridLayout.addWidget(self.device1_ip, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.device1)

        self.device2 = QWidget(net_setting_tab)
        self.device2.setObjectName(u"device2")
        self.device2.setMaximumSize(QSize(400, 16777215))
        self.gridLayout_2 = QGridLayout(self.device2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.device2_label = QLabel(self.device2)
        self.device2_label.setObjectName(u"device2_label")

        self.gridLayout_2.addWidget(self.device2_label, 0, 0, 1, 1)

        self.device2_ip = QLineEdit(self.device2)
        self.device2_ip.setObjectName(u"device2_ip")

        self.gridLayout_2.addWidget(self.device2_ip, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.device2)

        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottom_spacer)


        self.retranslateUi(net_setting_tab)

        QMetaObject.connectSlotsByName(net_setting_tab)
    # setupUi

    def retranslateUi(self, net_setting_tab):
        net_setting_tab.setWindowTitle(QCoreApplication.translate("net_setting_tab", u"Form", None))
        self.caption.setText(QCoreApplication.translate("net_setting_tab", u"Set IP address.", None))
        self.device1_label.setText(QCoreApplication.translate("net_setting_tab", u"Device1 IP", None))
        self.device2_label.setText(QCoreApplication.translate("net_setting_tab", u"Device2 IP", None))
    # retranslateUi

