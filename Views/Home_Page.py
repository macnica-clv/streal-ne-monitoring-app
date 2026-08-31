# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Home_Page.ui'
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
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)
from Views import resources_rc

class Ui_home_page(object):
    def setupUi(self, home_page):
        if not home_page.objectName():
            home_page.setObjectName(u"home_page")
        home_page.resize(990, 553)
        home_page.setStyleSheet(u"background-color: rgb(200, 200, 200)")
        self.gridLayout = QGridLayout(home_page)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.connect_settings = QQuickWidget(home_page)
        self.connect_settings.setObjectName(u"connect_settings")
        self.connect_settings.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_settings.sizePolicy().hasHeightForWidth())
        self.connect_settings.setSizePolicy(sizePolicy)
        self.connect_settings.setMinimumSize(QSize(500, 390))
        self.connect_settings.setSource(QUrl(u"qrc:/qml/qml/ConnectionSetting.qml"))

        self.gridLayout.addWidget(self.connect_settings, 1, 1, 1, 1)

        self.bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.bottom_spacer, 3, 1, 1, 2)

        self.right_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.right_spacer, 1, 4, 2, 1)

        self.home_title = QWidget(home_page)
        self.home_title.setObjectName(u"home_title")
        self.home_title.setStyleSheet(u"background-color: rgb(240, 240, 240); color: black;")
        self.horizontalLayout_2 = QHBoxLayout(self.home_title)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.title_icon = QPushButton(self.home_title)
        self.title_icon.setObjectName(u"title_icon")
        self.title_icon.setEnabled(False)
        icon = QIcon()
        icon.addFile(u":/HomePages/Images/Pages/HomePage/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.title_icon.setIcon(icon)
        self.title_icon.setIconSize(QSize(40, 40))
        self.title_icon.setFlat(True)

        self.horizontalLayout_2.addWidget(self.title_icon)

        self.title_body = QLabel(self.home_title)
        self.title_body.setObjectName(u"title_body")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.title_body.sizePolicy().hasHeightForWidth())
        self.title_body.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(30)
        font.setBold(False)
        self.title_body.setFont(font)

        self.horizontalLayout_2.addWidget(self.title_body)

        self.title_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.title_spacer)


        self.gridLayout.addWidget(self.home_title, 0, 0, 1, 5)

        self.left_spacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.left_spacer, 1, 0, 2, 1)

        self.connect_status = QQuickWidget(home_page)
        self.connect_status.setObjectName(u"connect_status")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.connect_status.sizePolicy().hasHeightForWidth())
        self.connect_status.setSizePolicy(sizePolicy2)
        self.connect_status.setMinimumSize(QSize(400, 390))
        self.connect_status.setSource(QUrl(u"qrc:/qml/qml/ConnectionStatus.qml"))

        self.gridLayout.addWidget(self.connect_status, 1, 3, 1, 1)

        self.message_info = QWidget(home_page)
        self.message_info.setObjectName(u"message_info")
        sizePolicy2.setHeightForWidth(self.message_info.sizePolicy().hasHeightForWidth())
        self.message_info.setSizePolicy(sizePolicy2)
        self.message_info.setMinimumSize(QSize(0, 50))
        self.message_info.setStyleSheet(u"background-color: rgb(240, 240, 240);")
        self.horizontalLayout = QHBoxLayout(self.message_info)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.info_icon = QPushButton(self.message_info)
        self.info_icon.setObjectName(u"info_icon")
        icon1 = QIcon()
        icon1.addFile(u":/HomePages/Images/Pages/HomePage/information-circle-sharp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.info_icon.setIcon(icon1)
        self.info_icon.setIconSize(QSize(32, 32))
        self.info_icon.setFlat(True)

        self.horizontalLayout.addWidget(self.info_icon)

        self.message_body = QLabel(self.message_info)
        self.message_body.setObjectName(u"message_body")
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.message_body.setFont(font1)
        self.message_body.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.message_body)

        self.message_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.message_spacer)


        self.gridLayout.addWidget(self.message_info, 2, 1, 1, 3)


        self.retranslateUi(home_page)

        QMetaObject.connectSlotsByName(home_page)
    # setupUi

    def retranslateUi(self, home_page):
        self.title_icon.setText("")
        self.title_body.setText(QCoreApplication.translate("home_page", u"HOME", None))
        self.info_icon.setText("")
        self.message_body.setText(QCoreApplication.translate("home_page", u"Please connect the evaluation kit.", None))
        pass
    # retranslateUi

