# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Shortcut_Setting.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_sc_setting_tab(object):
    def setupUi(self, sc_setting_tab):
        if not sc_setting_tab.objectName():
            sc_setting_tab.setObjectName(u"sc_setting_tab")
        sc_setting_tab.resize(563, 303)
        sc_setting_tab.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(sc_setting_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.caption = QLabel(sc_setting_tab)
        self.caption.setObjectName(u"caption")
        font = QFont()
        font.setPointSize(11)
        self.caption.setFont(font)

        self.verticalLayout.addWidget(self.caption)

        self.start_config = QWidget(sc_setting_tab)
        self.start_config.setObjectName(u"start_config")
        self.start_config.setMinimumSize(QSize(400, 0))
        self.start_config.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout = QHBoxLayout(self.start_config)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.start_label = QLabel(self.start_config)
        self.start_label.setObjectName(u"start_label")

        self.horizontalLayout.addWidget(self.start_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.start_edit = QLineEdit(self.start_config)
        self.start_edit.setObjectName(u"start_edit")
        self.start_edit.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.start_edit)

        self.start_config_clear = QPushButton(self.start_config)
        self.start_config_clear.setObjectName(u"start_config_clear")
        self.start_config_clear.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.start_config_clear)

        self.start_config_restore = QPushButton(self.start_config)
        self.start_config_restore.setObjectName(u"start_config_restore")
        self.start_config_restore.setMinimumSize(QSize(60, 0))
        self.start_config_restore.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.start_config_restore)


        self.verticalLayout.addWidget(self.start_config)

        self.stop_config = QWidget(sc_setting_tab)
        self.stop_config.setObjectName(u"stop_config")
        self.stop_config.setMinimumSize(QSize(400, 0))
        self.stop_config.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.stop_config)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.stop_label = QLabel(self.stop_config)
        self.stop_label.setObjectName(u"stop_label")

        self.horizontalLayout_2.addWidget(self.stop_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.stop_edit = QLineEdit(self.stop_config)
        self.stop_edit.setObjectName(u"stop_edit")
        self.stop_edit.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.stop_edit)

        self.stop_config_clear = QPushButton(self.stop_config)
        self.stop_config_clear.setObjectName(u"stop_config_clear")
        self.stop_config_clear.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.stop_config_clear)

        self.stop_config_restore = QPushButton(self.stop_config)
        self.stop_config_restore.setObjectName(u"stop_config_restore")
        self.stop_config_restore.setMinimumSize(QSize(60, 0))
        self.stop_config_restore.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.stop_config_restore)


        self.verticalLayout.addWidget(self.stop_config)

        self.auto_range_config = QWidget(sc_setting_tab)
        self.auto_range_config.setObjectName(u"auto_range_config")
        self.auto_range_config.setMinimumSize(QSize(400, 0))
        self.auto_range_config.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout_3 = QHBoxLayout(self.auto_range_config)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.auto_range_label = QLabel(self.auto_range_config)
        self.auto_range_label.setObjectName(u"auto_range_label")

        self.horizontalLayout_3.addWidget(self.auto_range_label)

        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.auto_range_edit = QLineEdit(self.auto_range_config)
        self.auto_range_edit.setObjectName(u"auto_range_edit")
        self.auto_range_edit.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.auto_range_edit)

        self.auto_range_config_clear = QPushButton(self.auto_range_config)
        self.auto_range_config_clear.setObjectName(u"auto_range_config_clear")
        self.auto_range_config_clear.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.auto_range_config_clear)

        self.auto_range_config_restore = QPushButton(self.auto_range_config)
        self.auto_range_config_restore.setObjectName(u"auto_range_config_restore")
        self.auto_range_config_restore.setMinimumSize(QSize(60, 0))
        self.auto_range_config_restore.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.auto_range_config_restore)


        self.verticalLayout.addWidget(self.auto_range_config)

        self.save_config = QWidget(sc_setting_tab)
        self.save_config.setObjectName(u"save_config")
        self.save_config.setMinimumSize(QSize(400, 0))
        self.save_config.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.save_config)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.save_label = QLabel(self.save_config)
        self.save_label.setObjectName(u"save_label")

        self.horizontalLayout_4.addWidget(self.save_label)

        self.horizontalSpacer_4 = QSpacerItem(59, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.save_edit = QLineEdit(self.save_config)
        self.save_edit.setObjectName(u"save_edit")
        self.save_edit.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_4.addWidget(self.save_edit)

        self.save_config_clear = QPushButton(self.save_config)
        self.save_config_clear.setObjectName(u"save_config_clear")
        self.save_config_clear.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.save_config_clear)

        self.save_config_restore = QPushButton(self.save_config)
        self.save_config_restore.setObjectName(u"save_config_restore")
        self.save_config_restore.setMinimumSize(QSize(60, 0))
        self.save_config_restore.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.save_config_restore)


        self.verticalLayout.addWidget(self.save_config)

        self.capture_config = QWidget(sc_setting_tab)
        self.capture_config.setObjectName(u"capture_config")
        self.capture_config.setMinimumSize(QSize(400, 0))
        self.capture_config.setMaximumSize(QSize(400, 16777215))
        self.horizontalLayout_5 = QHBoxLayout(self.capture_config)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.capture_label = QLabel(self.capture_config)
        self.capture_label.setObjectName(u"capture_label")

        self.horizontalLayout_5.addWidget(self.capture_label)

        self.horizontalSpacer_5 = QSpacerItem(42, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.capture_edit = QLineEdit(self.capture_config)
        self.capture_edit.setObjectName(u"capture_edit")
        self.capture_edit.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_5.addWidget(self.capture_edit)

        self.capture_config_clear = QPushButton(self.capture_config)
        self.capture_config_clear.setObjectName(u"capture_config_clear")
        self.capture_config_clear.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.capture_config_clear)

        self.capture_config_restore = QPushButton(self.capture_config)
        self.capture_config_restore.setObjectName(u"capture_config_restore")
        self.capture_config_restore.setMinimumSize(QSize(60, 0))
        self.capture_config_restore.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.capture_config_restore)


        self.verticalLayout.addWidget(self.capture_config)

        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottom_spacer)


        self.retranslateUi(sc_setting_tab)

        QMetaObject.connectSlotsByName(sc_setting_tab)
    # setupUi

    def retranslateUi(self, sc_setting_tab):
        sc_setting_tab.setWindowTitle(QCoreApplication.translate("sc_setting_tab", u"Form", None))
        self.caption.setText(QCoreApplication.translate("sc_setting_tab", u"Set keyboard shortcuts.", None))
        self.start_label.setText(QCoreApplication.translate("sc_setting_tab", u"Start", None))
        self.start_config_clear.setText(QCoreApplication.translate("sc_setting_tab", u"Clear", None))
        self.start_config_restore.setText(QCoreApplication.translate("sc_setting_tab", u"Restore", None))
        self.stop_label.setText(QCoreApplication.translate("sc_setting_tab", u"Stop", None))
        self.stop_config_clear.setText(QCoreApplication.translate("sc_setting_tab", u"Clear", None))
        self.stop_config_restore.setText(QCoreApplication.translate("sc_setting_tab", u"Restore", None))
        self.auto_range_label.setText(QCoreApplication.translate("sc_setting_tab", u"Auto Range", None))
        self.auto_range_config_clear.setText(QCoreApplication.translate("sc_setting_tab", u"Clear", None))
        self.auto_range_config_restore.setText(QCoreApplication.translate("sc_setting_tab", u"Restore", None))
        self.save_label.setText(QCoreApplication.translate("sc_setting_tab", u"Save", None))
        self.save_config_clear.setText(QCoreApplication.translate("sc_setting_tab", u"Clear", None))
        self.save_config_restore.setText(QCoreApplication.translate("sc_setting_tab", u"Restore", None))
        self.capture_label.setText(QCoreApplication.translate("sc_setting_tab", u"Capture", None))
        self.capture_config_clear.setText(QCoreApplication.translate("sc_setting_tab", u"Clear", None))
        self.capture_config_restore.setText(QCoreApplication.translate("sc_setting_tab", u"Restore", None))
    # retranslateUi

