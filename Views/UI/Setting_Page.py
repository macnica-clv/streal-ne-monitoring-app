# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setting_Page.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from Views import resources_rc

class Ui_setting_page(object):
    def setupUi(self, setting_page):
        if not setting_page.objectName():
            setting_page.setObjectName(u"setting_page")
        setting_page.setWindowModality(Qt.WindowModality.ApplicationModal)
        setting_page.resize(800, 550)
        setting_page.setMinimumSize(QSize(800, 550))
        setting_page.setMaximumSize(QSize(800, 550))
        setting_page.setStyleSheet(u"background-color: white;")
        self.page_layout = QWidget(setting_page)
        self.page_layout.setObjectName(u"page_layout")
        self.gridLayout = QGridLayout(self.page_layout)
        self.gridLayout.setObjectName(u"gridLayout")
        self.setting_bottom = QWidget(self.page_layout)
        self.setting_bottom.setObjectName(u"setting_bottom")
        self.horizontalLayout_6 = QHBoxLayout(self.setting_bottom)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.bottom_spacer)

        self.cancel_button = QPushButton(self.setting_bottom)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMinimumSize(QSize(75, 21))
        self.cancel_button.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.cancel_button)

        self.apply_button = QPushButton(self.setting_bottom)
        self.apply_button.setObjectName(u"apply_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.apply_button.sizePolicy().hasHeightForWidth())
        self.apply_button.setSizePolicy(sizePolicy1)
        self.apply_button.setMinimumSize(QSize(75, 21))
        self.apply_button.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.apply_button)


        self.gridLayout.addWidget(self.setting_bottom, 1, 0, 1, 2)

        self.menubar = QWidget(self.page_layout)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setMinimumSize(QSize(150, 0))
        self.menubar.setMaximumSize(QSize(150, 16777215))
        self.menubar.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.menubar)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.color_button = QPushButton(self.menubar)
        self.color_button.setObjectName(u"color_button")
        font = QFont()
        font.setPointSize(12)
        self.color_button.setFont(font)
        self.color_button.setStyleSheet(u"QPushButton { border-left-width: 2px; border-top-right-radius: 3px; border-bottom-right-radius: 3px;  text-align: left; padding-left: 8px;} QPushButton:hover { color: lightblue; }")
        self.color_button.setCheckable(True)
        self.color_button.setChecked(True)
        self.color_button.setAutoExclusive(True)
        self.color_button.setFlat(True)

        self.verticalLayout.addWidget(self.color_button)

        self.sc_button = QPushButton(self.menubar)
        self.sc_button.setObjectName(u"sc_button")
        self.sc_button.setFont(font)
        self.sc_button.setStyleSheet(u"QPushButton { border-left-width: 2px; border-top-right-radius: 3px; border-bottom-right-radius: 3px;  text-align: left; padding-left: 8px;} QPushButton:hover { color: lightblue; }")
        self.sc_button.setCheckable(True)
        self.sc_button.setAutoExclusive(True)
        self.sc_button.setFlat(True)

        self.verticalLayout.addWidget(self.sc_button)

        self.lang_button = QPushButton(self.menubar)
        self.lang_button.setObjectName(u"lang_button")
        self.lang_button.setFont(font)
        self.lang_button.setStyleSheet(u"QPushButton { border-left-width: 2px; border-top-right-radius: 3px; border-bottom-right-radius: 3px;  text-align: left; padding-left: 8px;} QPushButton:hover { color: lightblue; }")
        self.lang_button.setCheckable(True)
        self.lang_button.setAutoExclusive(True)
        self.lang_button.setFlat(True)

        self.verticalLayout.addWidget(self.lang_button)

        self.log_button = QPushButton(self.menubar)
        self.log_button.setObjectName(u"log_button")
        self.log_button.setFont(font)
        self.log_button.setStyleSheet(u"QPushButton { border-left-width: 2px; border-top-right-radius: 3px; border-bottom-right-radius: 3px;  text-align: left; padding-left: 8px;} QPushButton:hover { color: lightblue;  }")
        self.log_button.setCheckable(True)
        self.log_button.setAutoExclusive(True)
        self.log_button.setFlat(True)

        self.verticalLayout.addWidget(self.log_button)

        self.network_button = QPushButton(self.menubar)
        self.network_button.setObjectName(u"network_button")
        self.network_button.setFont(font)
        self.network_button.setStyleSheet(u"QPushButton { border-left-width: 2px; border-top-right-radius: 3px; border-bottom-right-radius: 3px;  text-align: left; padding-left: 8px;} QPushButton:hover { color: lightblue;  }")
        self.network_button.setCheckable(True)
        self.network_button.setAutoExclusive(True)
        self.network_button.setFlat(True)

        self.verticalLayout.addWidget(self.network_button)

        self.version_Button = QPushButton(self.menubar)
        self.version_Button.setObjectName(u"version_Button")
        self.version_Button.setFont(font)
        self.version_Button.setCheckable(True)
        self.version_Button.setAutoExclusive(True)
        self.version_Button.setFlat(True)

        self.verticalLayout.addWidget(self.version_Button)

        self.menu_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.menu_spacer)


        self.gridLayout.addWidget(self.menubar, 0, 0, 1, 1)

        self.body_layout = QVBoxLayout()
        self.body_layout.setObjectName(u"body_layout")

        self.gridLayout.addLayout(self.body_layout, 0, 1, 1, 1)

        setting_page.setCentralWidget(self.page_layout)

        self.retranslateUi(setting_page)

        QMetaObject.connectSlotsByName(setting_page)
    # setupUi

    def retranslateUi(self, setting_page):
        setting_page.setWindowTitle(QCoreApplication.translate("setting_page", u"Settings", None))
        self.cancel_button.setText(QCoreApplication.translate("setting_page", u"Cancel", None))
        self.apply_button.setText(QCoreApplication.translate("setting_page", u"Apply", None))
        self.color_button.setText(QCoreApplication.translate("setting_page", u"Color Theme", None))
        self.sc_button.setText(QCoreApplication.translate("setting_page", u"Shortcuts", None))
        self.lang_button.setText(QCoreApplication.translate("setting_page", u"Language", None))
        self.log_button.setText(QCoreApplication.translate("setting_page", u"Log Settings", None))
        self.network_button.setText(QCoreApplication.translate("setting_page", u"Network Settings", None))
        self.version_Button.setText(QCoreApplication.translate("setting_page", u"Information", None))
    # retranslateUi

