# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resulteopHzR.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import icons_rc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_ResultWindow(object):
    def setupUi(self, ResultWindow):
        if not ResultWindow.objectName():
            ResultWindow.setObjectName("ResultWindow")
        ResultWindow.setStyleSheet("background-color: #e1e1e1;")
        self.centralwidget = QWidget(ResultWindow)
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
            "#main_body{\n"
            "	background-color: #b3cdcd;\n"
            "	border-radius: 20px;\n"
            "}"
        )
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setSpacing(7)
        self.central_layout.setObjectName("central_layout")
        self.central_layout.setContentsMargins(11, 11, 11, 11)
        self.body = QFrame(self.centralwidget)
        self.body.setObjectName("body")
        self.body.setFrameShape(QFrame.StyledPanel)
        self.body.setFrameShadow(QFrame.Raised)
        self.contain_body_layout = QVBoxLayout(self.body)
        self.contain_body_layout.setSpacing(0)
        self.contain_body_layout.setObjectName("contain_body_layout")
        self.contain_body_layout.setContentsMargins(0, 0, 0, 0)
        self.brand_label_frame = QFrame(self.body)
        self.brand_label_frame.setObjectName("brand_label_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.brand_label_frame.sizePolicy().hasHeightForWidth()
        )
        self.brand_label_frame.setSizePolicy(sizePolicy)
        self.brand_label_frame.setFrameShape(QFrame.StyledPanel)
        self.brand_label_frame.setFrameShadow(QFrame.Raised)
        self.brand_name_layout = QVBoxLayout(self.brand_label_frame)
        self.brand_name_layout.setSpacing(0)
        self.brand_name_layout.setObjectName("brand_name_layout")
        self.brand_name_layout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(self.brand_label_frame)
        self.header.setObjectName("header")
        self.header.setMinimumSize(QSize(0, 50))
        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setFrameShadow(QFrame.Raised)
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setObjectName("header_layout")
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.header)
        self.label.setObjectName("label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.header_layout.addWidget(self.label)

        self.brand_name_layout.addWidget(self.header)

        self.contain_body_layout.addWidget(self.brand_label_frame)

        self.container = QFrame(self.body)
        self.container.setObjectName("container")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.container.sizePolicy().hasHeightForWidth())
        self.container.setSizePolicy(sizePolicy1)
        self.container.setFrameShape(QFrame.StyledPanel)
        self.container.setFrameShadow(QFrame.Raised)
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setObjectName("container_layout")
        self.main_body = QFrame(self.container)
        self.main_body.setObjectName("main_body")
        sizePolicy.setHeightForWidth(self.main_body.sizePolicy().hasHeightForWidth())
        self.main_body.setSizePolicy(sizePolicy)
        self.main_body.setStyleSheet("padding-left: 20px;\n" "padding-right: 20px;")
        self.main_body.setFrameShape(QFrame.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Raised)
        self.body_layout = QVBoxLayout(self.main_body)
        self.body_layout.setObjectName("body_layout")
        self.label_frame = QFrame(self.main_body)
        self.label_frame.setObjectName("label_frame")
        self.label_frame.setStyleSheet("padding: 0;")
        self.label_frame.setFrameShape(QFrame.StyledPanel)
        self.label_frame.setFrameShadow(QFrame.Raised)
        self.question_layout = QVBoxLayout(self.label_frame)
        self.question_layout.setSpacing(0)
        self.question_layout.setObjectName("question_layout")
        self.question_layout.setContentsMargins(0, 0, 0, 0)
        self.body_label = QLabel(self.label_frame)
        self.body_label.setObjectName("body_label")
        font1 = QFont()
        font1.setPointSize(12)
        self.body_label.setFont(font1)
        self.body_label.setStyleSheet("margin: 15px;")

        self.question_layout.addWidget(
            self.body_label, 0, Qt.AlignHCenter | Qt.AlignTop
        )

        self.body_layout.addWidget(self.label_frame)

        self.wrapper_frame = QFrame(self.main_body)
        self.wrapper_frame.setObjectName("wrapper_frame")
        sizePolicy1.setHeightForWidth(
            self.wrapper_frame.sizePolicy().hasHeightForWidth()
        )
        self.wrapper_frame.setSizePolicy(sizePolicy1)
        self.wrapper_frame.setStyleSheet(
            "padding: 0;\n"
            "background-color: #e1e1e1;\n"
            "border-radius: 20px;\n"
            "border: none;"
        )
        self.wrapper_frame.setFrameShape(QFrame.StyledPanel)
        self.wrapper_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.wrapper_frame)
        self.horizontalLayout.setSpacing(11)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.chart_frame = QFrame(self.wrapper_frame)
        self.chart_frame.setObjectName("chart_frame")
        self.chart_frame.setFrameShape(QFrame.StyledPanel)
        self.chart_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.chart_frame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout.addWidget(self.chart_frame)

        self.labels_frame = QFrame(self.wrapper_frame)
        self.labels_frame.setObjectName("labels_frame")
        self.labels_frame.setStyleSheet("")
        self.labels_frame.setFrameShape(QFrame.StyledPanel)
        self.labels_frame.setFrameShadow(QFrame.Raised)
        self.labels_frame.setMinimumSize(QSize(521, 460))
        self.verticalLayout_2 = QVBoxLayout(self.labels_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.result_label1 = QLabel(self.labels_frame)
        self.result_label1.setObjectName("result_label1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.result_label1.sizePolicy().hasHeightForWidth()
        )
        self.result_label1.setSizePolicy(sizePolicy2)
        self.result_label1.setStyleSheet("margin-left: 10px;")

        self.verticalLayout_2.addWidget(self.result_label1)

        self.result_label2 = QLabel(self.labels_frame)
        self.result_label2.setObjectName("result_label2")
        sizePolicy2.setHeightForWidth(
            self.result_label2.sizePolicy().hasHeightForWidth()
        )
        self.result_label2.setSizePolicy(sizePolicy2)
        self.result_label2.setStyleSheet("margin-left: 10px;")

        self.verticalLayout_2.addWidget(self.result_label2)

        self.result_label3 = QLabel(self.labels_frame)
        self.result_label3.setObjectName("result_label3")
        sizePolicy2.setHeightForWidth(
            self.result_label3.sizePolicy().hasHeightForWidth()
        )
        self.result_label3.setSizePolicy(sizePolicy2)
        self.result_label3.setStyleSheet("margin-left: 10px;")

        self.verticalLayout_2.addWidget(self.result_label3)

        self.horizontalLayout.addWidget(self.labels_frame)

        self.body_layout.addWidget(self.wrapper_frame)

        self.container_layout.addWidget(self.main_body)

        self.contain_body_layout.addWidget(self.container)

        self.central_layout.addWidget(self.body)

        ResultWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ResultWindow)

        QMetaObject.connectSlotsByName(ResultWindow)

    # setupUi

    def retranslateUi(self, ResultWindow):
        ResultWindow.setWindowTitle(
            QCoreApplication.translate("ResultWindow", "IT meýdança Quizz", None)
        )
        ResultWindow.setWindowFilePath("")
        self.label.setText(
            QCoreApplication.translate("ResultWindow", "Challenge name", None)
        )
        self.body_label.setText(
            QCoreApplication.translate(
                "ResultWindow", "\u00ddary\u015f netijeleri", None
            )
        )
        self.result_label1.setText(
            QCoreApplication.translate("ResultWindow", "TextLabel", None)
        )
        self.result_label2.setText(
            QCoreApplication.translate("ResultWindow", "TextLabel", None)
        )
        self.result_label3.setText(
            QCoreApplication.translate("ResultWindow", "TextLabel", None)
        )

    # retranslateUi
