# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logintMZlAb.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import icons_rc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .custom_objects import PushButton


class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 623)
        MainWindow.setStyleSheet("background-color: #e1e1e1;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(
            "*{\n"
            "	border: none;\n"
            "	background-color: transparent;\n"
            "}\n"
            "#centralwidget{\n"
            "	background-color: #e1e1e1;\n"
            "}\n"
            "#side_menu{\n"
            "	background-color: #b3cdcd;\n"
            "	border-radius: 20px;\n"
            "}\n"
            "QPushButton{\n"
            "	padding: 10px;\n"
            "	background-color: #e1e1e1;\n"
            "	border-radius: 5px;\n"
            "	border: none;\n"
            "}\n"
            "#box{\n"
            "	background-color: #b3cdcd;\n"
            "	border-radius: 20px;\n"
            "}"
        )
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setSpacing(7)
        self.central_layout.setObjectName("central_layout")
        self.central_layout.setContentsMargins(11, 11, 11, 11)
        self.l_main_body = QFrame(self.centralwidget)
        self.l_main_body.setObjectName("l_main_body")
        self.l_main_body.setFrameShape(QFrame.StyledPanel)
        self.l_main_body.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.l_main_body)
        self.verticalLayout.setObjectName("verticalLayout")
        self.box = QFrame(self.l_main_body)
        self.box.setObjectName("box")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box.sizePolicy().hasHeightForWidth())
        self.box.setSizePolicy(sizePolicy)
        self.box.setMinimumSize(QSize(400, 450))
        self.box.setFrameShape(QFrame.StyledPanel)
        self.box.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.box)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name_frame = QFrame(self.box)
        self.name_frame.setObjectName("name_frame")
        self.name_frame.setMinimumSize(QSize(250, 0))
        self.name_frame.setFrameShape(QFrame.StyledPanel)
        self.name_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.name_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.name_label = QLabel(self.name_frame)
        self.name_label.setObjectName("name_label")
        font = QFont()
        font.setPointSize(14)
        self.name_label.setFont(font)

        self.verticalLayout_3.addWidget(
            self.name_label, 0, Qt.AlignHCenter | Qt.AlignBottom
        )

        self.name_input = QLineEdit(self.name_frame)
        self.name_input.setObjectName("name_input")
        self.name_input.setFont(font)
        self.name_input.setStyleSheet(
            "background-color: white;\n"
            "background-color: white;\n"
            "padding: 10px;\n"
            "border-radius: 25px;\n"
            "border: 1px solid #e1e1e1;"
        )

        self.verticalLayout_3.addWidget(self.name_input)

        self.verticalLayout_2.addWidget(
            self.name_frame, 0, Qt.AlignHCenter | Qt.AlignBottom
        )

        self.surname_frame = QFrame(self.box)
        self.surname_frame.setObjectName("surname_frame")
        self.surname_frame.setMinimumSize(QSize(250, 0))
        self.surname_frame.setFrameShape(QFrame.StyledPanel)
        self.surname_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.surname_frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.surname_label = QLabel(self.surname_frame)
        self.surname_label.setObjectName("surname_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.surname_label.sizePolicy().hasHeightForWidth()
        )
        self.surname_label.setSizePolicy(sizePolicy1)
        self.surname_label.setFont(font)

        self.verticalLayout_4.addWidget(self.surname_label, 0, Qt.AlignHCenter)

        self.surname_input = QLineEdit(self.surname_frame)
        self.surname_input.setObjectName("surname_input")
        self.surname_input.setFont(font)
        self.surname_input.setStyleSheet(
            "background-color: white;\n"
            "padding: 10px;\n"
            "border-radius: 25px;\n"
            "border: 1px solid #e1e1e1;"
        )

        self.verticalLayout_4.addWidget(self.surname_input)

        self.verticalLayout_2.addWidget(
            self.surname_frame, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.frame = QFrame(self.box)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.about_label = QLabel(self.frame)
        self.about_label.setObjectName("about_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.about_label.sizePolicy().hasHeightForWidth())
        self.about_label.setSizePolicy(sizePolicy2)
        self.about_label.setFont(font)

        self.verticalLayout_6.addWidget(self.about_label, 0, Qt.AlignHCenter)

        self.about_input = QLineEdit(self.frame)
        self.about_input.setObjectName("about")
        self.about_input.setFont(font)
        self.about_input.setStyleSheet(
            "background-color: white;\n"
            "padding: 10px;\n"
            "border-radius: 25px;\n"
            "border: 1px solid #e1e1e1;"
        )

        self.verticalLayout_6.addWidget(self.about_input)

        self.verticalLayout_2.addWidget(self.frame, 0, Qt.AlignHCenter)

        self.accept_frame = QFrame(self.box)
        self.accept_frame.setObjectName("accept_frame")
        self.accept_frame.setFrameShape(QFrame.StyledPanel)
        self.accept_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.accept_frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.accept_btn = PushButton(self.accept_frame)
        self.accept_btn.setObjectName("accept_btn")
        font1 = QFont()
        font1.setPointSize(12)
        self.accept_btn.setFont(font1)
        self.accept_btn.setStyleSheet(
            "padding: 16px;\n"
            "padding-left: 25px;\n"
            "padding-right: 25px;\n"
            "border-radius: 25px;"
        )

        self.verticalLayout_5.addWidget(self.accept_btn)

        self.verticalLayout_2.addWidget(
            self.accept_frame, 0, Qt.AlignHCenter | Qt.AlignTop
        )

        self.verticalLayout.addWidget(self.box, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        self.central_layout.addWidget(self.l_main_body)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        MainWindow.setWindowFilePath("")
        self.name_label.setText(QCoreApplication.translate("MainWindow", "Ady:", None))
        self.surname_label.setText(
            QCoreApplication.translate("MainWindow", "Famili\u00fdasy:", None)
        )
        self.about_label.setText(
            QCoreApplication.translate("MainWindow", "Edara:", None)
        )
        self.accept_btn.setText(
            QCoreApplication.translate("MainWindow", "Tassyklamak", None)
        )

    # retranslateUi
