# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_Window.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from Views import resources_rc

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1200, 800)
        main_window.setMinimumSize(QSize(1200, 800))
        self.window_body = QWidget(main_window)
        self.window_body.setObjectName(u"window_body")
        self.window_layout = QVBoxLayout(self.window_body)
        self.window_layout.setSpacing(0)
        self.window_layout.setObjectName(u"window_layout")
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.body_area = QWidget(self.window_body)
        self.body_area.setObjectName(u"body_area")
        self.body_layout = QHBoxLayout(self.body_area)
        self.body_layout.setSpacing(0)
        self.body_layout.setObjectName(u"body_layout")
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar = QWidget(self.body_area)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setMinimumSize(QSize(50, 0))
        self.toolbar.setMaximumSize(QSize(50, 16777215))
        self.toolbar.setStyleSheet(u"background-color: rgb(220, 220, 220);")
        self.toolbar_layout = QVBoxLayout(self.toolbar)
        self.toolbar_layout.setSpacing(6)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.toolbar_layout.setContentsMargins(0, 5, 0, 5)
        self.home_button = QPushButton(self.toolbar)
        self.home_button.setObjectName(u"home_button")
        self.home_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";}\n"
"QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon = QIcon()
        icon.addFile(u":/ToolBar/Images/ToolBar/Home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(26, 32))
        self.home_button.setFlat(True)

        self.toolbar_layout.addWidget(self.home_button)

        self.label = QLabel(self.toolbar)
        self.label.setObjectName(u"label")
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toolbar_layout.addWidget(self.label)

        self.chart_button = QPushButton(self.toolbar)
        self.chart_button.setObjectName(u"chart_button")
        self.chart_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";}\n"
"QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon1 = QIcon()
        icon1.addFile(u":/ToolBar/Images/ToolBar/wave-saw-tool.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.chart_button.setIcon(icon1)
        self.chart_button.setIconSize(QSize(26, 32))
        self.chart_button.setFlat(True)

        self.toolbar_layout.addWidget(self.chart_button)

        self.label_2 = QLabel(self.toolbar)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toolbar_layout.addWidget(self.label_2)

        self.manual_button = QPushButton(self.toolbar)
        self.manual_button.setObjectName(u"manual_button")
        self.manual_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";}\n"
"QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon2 = QIcon()
        icon2.addFile(u":/ToolBar/Images/ToolBar/book.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.manual_button.setIcon(icon2)
        self.manual_button.setIconSize(QSize(26, 32))
        self.manual_button.setFlat(True)

        self.toolbar_layout.addWidget(self.manual_button)

        self.label_3 = QLabel(self.toolbar)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toolbar_layout.addWidget(self.label_3)

        self.toolbar_spacer = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.toolbar_layout.addItem(self.toolbar_spacer)

        self.setting_button = QPushButton(self.toolbar)
        self.setting_button.setObjectName(u"setting_button")
        self.setting_button.setStyleSheet(u"QPushButton:hover {background-color: \"#AAAAAA\"; color: \"#FFFFFF\";}\n"
"QPushButton:pressed {background-color: \"#666666\"; color: \"#FFFFFF\";}")
        icon3 = QIcon()
        icon3.addFile(u":/ToolBar/Images/ToolBar/gear-fill.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setting_button.setIcon(icon3)
        self.setting_button.setIconSize(QSize(23, 26))
        self.setting_button.setFlat(True)

        self.toolbar_layout.addWidget(self.setting_button)


        self.body_layout.addWidget(self.toolbar)

        self.page_area = QWidget(self.body_area)
        self.page_area.setObjectName(u"page_area")
        self.page_area.setStyleSheet(u"")
        self.page_layout = QVBoxLayout(self.page_area)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.body_layout.addWidget(self.page_area)


        self.window_layout.addWidget(self.body_area)

        self.status_bar = QWidget(self.window_body)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setMinimumSize(QSize(0, 30))
        self.status_bar.setMaximumSize(QSize(16777215, 30))
        self.status_bar.setStyleSheet(u"background-color: rgb(100, 100, 100);")
        self.statusbar_layout = QHBoxLayout(self.status_bar)
        self.statusbar_layout.setObjectName(u"statusbar_layout")
        self.statusbar_layout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalSpacer = QSpacerItem(873, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.statusbar_layout.addItem(self.horizontalSpacer)

        self.sensor_status = QQuickWidget(self.status_bar)
        self.sensor_status.setObjectName(u"sensor_status")
        self.sensor_status.setMinimumSize(QSize(250, 0))
        self.sensor_status.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.sensor_status.setSource(QUrl(u"qrc:/qml/qml/SensorStatus.qml"))

        self.statusbar_layout.addWidget(self.sensor_status)


        self.window_layout.addWidget(self.status_bar)

        main_window.setCentralWidget(self.window_body)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"App", None))
        self.home_button.setText("")
        self.label.setText(QCoreApplication.translate("main_window", u"Home", None))
        self.chart_button.setText("")
        self.label_2.setText(QCoreApplication.translate("main_window", u"Measure", None))
        self.manual_button.setText("")
        self.label_3.setText(QCoreApplication.translate("main_window", u"Manual", None))
        self.setting_button.setText("")
    # retranslateUi

