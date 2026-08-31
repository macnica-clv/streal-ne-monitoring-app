# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Color_Setting.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_color_setting_tab(object):
    def setupUi(self, color_setting_tab):
        if not color_setting_tab.objectName():
            color_setting_tab.setObjectName(u"color_setting_tab")
        color_setting_tab.resize(599, 379)
        color_setting_tab.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(color_setting_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption = QLabel(color_setting_tab)
        self.caption.setObjectName(u"caption")
        self.caption.setMinimumSize(QSize(0, 0))
        self.caption.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(11)
        self.caption.setFont(font)

        self.verticalLayout.addWidget(self.caption)

        self.theme_area = QWidget(color_setting_tab)
        self.theme_area.setObjectName(u"theme_area")
        self.theme_area.setMinimumSize(QSize(0, 60))
        self.theme_area.setMaximumSize(QSize(16777215, 60))
        self.verticalLayout_2 = QVBoxLayout(self.theme_area)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.theme_label = QLabel(self.theme_area)
        self.theme_label.setObjectName(u"theme_label")

        self.verticalLayout_2.addWidget(self.theme_label)

        self.theme_select = QComboBox(self.theme_area)
        self.theme_select.addItem("")
        self.theme_select.addItem("")
        self.theme_select.addItem("")
        self.theme_select.setObjectName(u"theme_select")
        self.theme_select.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout_2.addWidget(self.theme_select)


        self.verticalLayout.addWidget(self.theme_area)

        self.preview_area = QWidget(color_setting_tab)
        self.preview_area.setObjectName(u"preview_area")
        self.verticalLayout_3 = QVBoxLayout(self.preview_area)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.preview_label = QLabel(self.preview_area)
        self.preview_label.setObjectName(u"preview_label")

        self.verticalLayout_3.addWidget(self.preview_label)

        self.preview_image = QLabel(self.preview_area)
        self.preview_image.setObjectName(u"preview_image")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_image.sizePolicy().hasHeightForWidth())
        self.preview_image.setSizePolicy(sizePolicy)
        self.preview_image.setMinimumSize(QSize(0, 200))
        self.preview_image.setMaximumSize(QSize(300, 300))

        self.verticalLayout_3.addWidget(self.preview_image)


        self.verticalLayout.addWidget(self.preview_area)

        self.tab_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.tab_spacer)


        self.retranslateUi(color_setting_tab)

        QMetaObject.connectSlotsByName(color_setting_tab)
    # setupUi

    def retranslateUi(self, color_setting_tab):
        color_setting_tab.setWindowTitle(QCoreApplication.translate("color_setting_tab", u"Form", None))
        self.caption.setText(QCoreApplication.translate("color_setting_tab", u"Set the screen color theme.", None))
        self.theme_label.setText(QCoreApplication.translate("color_setting_tab", u"Select Color", None))
        self.theme_select.setItemText(0, QCoreApplication.translate("color_setting_tab", u"Normal", None))
        self.theme_select.setItemText(1, QCoreApplication.translate("color_setting_tab", u"Light", None))
        self.theme_select.setItemText(2, QCoreApplication.translate("color_setting_tab", u"Dark", None))

        self.preview_label.setText(QCoreApplication.translate("color_setting_tab", u"Sample", None))
        self.preview_image.setText("")
    # retranslateUi

