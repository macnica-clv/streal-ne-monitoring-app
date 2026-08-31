# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'version.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_version_tab(object):
    def setupUi(self, version_tab):
        if not version_tab.objectName():
            version_tab.setObjectName(u"version_tab")
        version_tab.resize(563, 303)
        version_tab.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(version_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption = QLabel(version_tab)
        self.caption.setObjectName(u"caption")
        font = QFont()
        font.setPointSize(11)
        self.caption.setFont(font)

        self.verticalLayout.addWidget(self.caption)

        self.version = QWidget(version_tab)
        self.version.setObjectName(u"version")
        self.version.setMinimumSize(QSize(400, 0))
        self.version.setMaximumSize(QSize(400, 16777215))
        self.gridLayout = QGridLayout(self.version)
        self.gridLayout.setObjectName(u"gridLayout")
        self.version_label = QLabel(self.version)
        self.version_label.setObjectName(u"version_label")

        self.gridLayout.addWidget(self.version_label, 0, 0, 1, 1)

        self.version_num = QLabel(self.version)
        self.version_num.setObjectName(u"version_num")

        self.gridLayout.addWidget(self.version_num, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.version)

        self.copyright = QWidget(version_tab)
        self.copyright.setObjectName(u"copyright")
        self.copyright.setMaximumSize(QSize(400, 16777215))
        self.gridLayout_2 = QGridLayout(self.copyright)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.copyright_label = QLabel(self.copyright)
        self.copyright_label.setObjectName(u"copyright_label")

        self.gridLayout_2.addWidget(self.copyright_label, 0, 0, 1, 1)

        self.mac_copuright = QLabel(self.copyright)
        self.mac_copuright.setObjectName(u"mac_copuright")

        self.gridLayout_2.addWidget(self.mac_copuright, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.copyright)

        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottom_spacer)


        self.retranslateUi(version_tab)

        QMetaObject.connectSlotsByName(version_tab)
    # setupUi

    def retranslateUi(self, version_tab):
        version_tab.setWindowTitle(QCoreApplication.translate("version_tab", u"Form", None))
        self.caption.setText(QCoreApplication.translate("version_tab", u"Application information.", None))
        self.version_label.setText(QCoreApplication.translate("version_tab", u"App version", None))
        self.version_num.setText(QCoreApplication.translate("version_tab", u"Version :  1.0.0.0", None))
        self.copyright_label.setText(QCoreApplication.translate("version_tab", u"Copyright", None))
        self.mac_copuright.setText(QCoreApplication.translate("version_tab", u"\u00a9Macnica, Inc. All rights Reserved.", None))
    # retranslateUi

