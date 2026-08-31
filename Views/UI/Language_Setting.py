# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Language_Setting.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_language_setting(object):
    def setupUi(self, language_setting):
        if not language_setting.objectName():
            language_setting.setObjectName(u"language_setting")
        language_setting.resize(524, 369)
        language_setting.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(language_setting)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption = QLabel(language_setting)
        self.caption.setObjectName(u"caption")
        font = QFont()
        font.setPointSize(11)
        self.caption.setFont(font)

        self.verticalLayout.addWidget(self.caption)

        self.language_select = QComboBox(language_setting)
        self.language_select.addItem("")
        self.language_select.addItem("")
        self.language_select.setObjectName(u"language_select")
        self.language_select.setMinimumSize(QSize(150, 0))
        self.language_select.setMaximumSize(QSize(150, 16777215))

        self.verticalLayout.addWidget(self.language_select)

        self.comment = QLabel(language_setting)
        self.comment.setObjectName(u"comment")

        self.verticalLayout.addWidget(self.comment)

        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottom_spacer)


        self.retranslateUi(language_setting)

        QMetaObject.connectSlotsByName(language_setting)
    # setupUi

    def retranslateUi(self, language_setting):
        language_setting.setWindowTitle(QCoreApplication.translate("language_setting", u"Form", None))
        self.caption.setText(QCoreApplication.translate("language_setting", u"Set display language.", None))
        self.language_select.setItemText(0, QCoreApplication.translate("language_setting", u"English", None))
        self.language_select.setItemText(1, QCoreApplication.translate("language_setting", u"Japanese", None))

        self.comment.setText(QCoreApplication.translate("language_setting", u"The application will be displayed in this language.", None))
    # retranslateUi

