# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'quizzMoaUhs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import icons_rc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .custom_objects import ClickableLabel, PushButton


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
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
        self.toggle_frame = QFrame(self.header)
        self.toggle_frame.setObjectName("toggle_frame")
        self.toggle_frame.setFrameShape(QFrame.StyledPanel)
        self.toggle_frame.setFrameShadow(QFrame.Raised)
        self.toggle_layout = QVBoxLayout(self.toggle_frame)
        self.toggle_layout.setSpacing(0)
        self.toggle_layout.setObjectName("toggle_layout")
        self.toggle_layout.setContentsMargins(40, 0, 0, 0)
        self.toggle_btn = QPushButton(self.toggle_frame)
        self.toggle_btn.setObjectName("toggle_btn")
        icon = QIcon()
        icon.addFile(
            ":/icons/bootstrap-icons/list.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.toggle_btn.setIcon(icon)

        self.toggle_layout.addWidget(self.toggle_btn, 0, Qt.AlignLeft)

        self.header_layout.addWidget(self.toggle_frame, 0, Qt.AlignLeft)

        self.label = QLabel(self.header)
        self.label.setObjectName("label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)

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
        self.side_menu = QWidget(self.container)
        self.side_menu.setObjectName("side_menu")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.side_menu.sizePolicy().hasHeightForWidth())
        self.side_menu.setSizePolicy(sizePolicy2)
        self.side_menu.setMinimumSize(QSize(0, 0))
        self.side_menu.setMaximumSize(QSize(161, 576))
        self.side_layout = QVBoxLayout(self.side_menu)
        self.side_layout.setObjectName("side_layout")
        self.question_btn_block = QFrame(self.side_menu)
        self.question_btn_block.setObjectName("question_btn_block")
        self.question_btn_block.setFrameShape(QFrame.StyledPanel)
        self.question_btn_block.setFrameShadow(QFrame.Raised)
        self.question_btn_layout = QVBoxLayout(self.question_btn_block)
        self.question_btn_layout.setObjectName("question_btn_layout")
        self.btn1 = QPushButton(self.question_btn_block)
        self.btn1.setObjectName("btn1")
        icon1 = QIcon()
        icon1.addFile(
            ":/icons/bootstrap-icons/question-lg.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.btn1.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn1)

        self.btn2 = QPushButton(self.question_btn_block)
        self.btn2.setObjectName("btn2")
        self.btn2.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn2)

        self.btn3 = QPushButton(self.question_btn_block)
        self.btn3.setObjectName("btn3")
        self.btn3.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn3)

        self.btn4 = QPushButton(self.question_btn_block)
        self.btn4.setObjectName("btn4")
        self.btn4.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn4)

        self.btn5 = QPushButton(self.question_btn_block)
        self.btn5.setObjectName("btn5")
        self.btn5.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn5)

        self.btn6 = QPushButton(self.question_btn_block)
        self.btn6.setObjectName("btn6")
        self.btn6.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn6)

        self.btn7 = QPushButton(self.question_btn_block)
        self.btn7.setObjectName("btn7")
        self.btn7.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn7)

        self.btn8 = QPushButton(self.question_btn_block)
        self.btn8.setObjectName("btn8")
        self.btn8.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn8)

        self.btn9 = QPushButton(self.question_btn_block)
        self.btn9.setObjectName("btn9")
        self.btn9.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn9)

        self.btn10 = QPushButton(self.question_btn_block)
        self.btn10.setObjectName("btn10")
        self.btn10.setIcon(icon1)

        self.question_btn_layout.addWidget(self.btn10)

        self.side_layout.addWidget(self.question_btn_block)

        self.pagination_block = QFrame(self.side_menu)
        self.pagination_block.setObjectName("pagination_block")
        self.pagination_block.setFrameShape(QFrame.StyledPanel)
        self.pagination_block.setFrameShadow(QFrame.Raised)
        self.pagination_layout = QHBoxLayout(self.pagination_block)
        self.pagination_layout.setObjectName("pagination_layout")
        self.prev_btn = QPushButton(self.pagination_block)
        self.prev_btn.setObjectName("prev_btn")
        icon2 = QIcon()
        icon2.addFile(
            ":/icons/bootstrap-icons/chevron-left.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.prev_btn.setIcon(icon2)

        self.pagination_layout.addWidget(self.prev_btn)

        self.next_btn = QPushButton(self.pagination_block)
        self.next_btn.setObjectName("next_btn")
        icon3 = QIcon()
        icon3.addFile(
            ":/icons/bootstrap-icons/chevron-right.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.next_btn.setIcon(icon3)

        self.pagination_layout.addWidget(self.next_btn)

        self.side_layout.addWidget(self.pagination_block, 0, Qt.AlignBottom)

        self.container_layout.addWidget(self.side_menu, 0, Qt.AlignTop)

        self.main_body = QFrame(self.container)
        self.main_body.setObjectName("main_body")
        sizePolicy.setHeightForWidth(self.main_body.sizePolicy().hasHeightForWidth())
        self.main_body.setSizePolicy(sizePolicy)
        self.main_body.setStyleSheet("padding-left: 20px;\n" "padding-right: 20px;")
        self.main_body.setFrameShape(QFrame.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Raised)
        self.body_layout = QVBoxLayout(self.main_body)
        self.body_layout.setObjectName("body_layout")
        self.question_frame = QFrame(self.main_body)
        self.question_frame.setObjectName("question_frame")
        self.question_frame.setStyleSheet("padding: 0;")
        self.question_frame.setFrameShape(QFrame.StyledPanel)
        self.question_frame.setFrameShadow(QFrame.Raised)
        self.question_layout = QVBoxLayout(self.question_frame)
        self.question_layout.setSpacing(0)
        self.question_layout.setObjectName("question_layout")
        self.question_layout.setContentsMargins(0, 0, 0, 0)
        self.question_id = QLabel(self.question_frame)
        self.question_id.setObjectName("question_id")
        font1 = QFont()
        font1.setPointSize(12)
        self.question_id.setFont(font1)
        self.question_id.setStyleSheet("margin: 15px;")

        self.question_layout.addWidget(
            self.question_id, 0, Qt.AlignHCenter | Qt.AlignTop
        )

        self.question = ClickableLabel(self.question_frame)
        self.question.setObjectName("question")
        font2 = QFont()
        font2.setPointSize(16)
        self.question.setFont(font2)
        self.question.setStyleSheet(
            "padding: 20px;\n"
            "padding-bottom: 40px;\n"
            "padding-top: 40px;\n"
            "background-color: white;\n"
            "border-radius: 20px;"
        )

        self.question_layout.addWidget(self.question, 0, Qt.AlignTop)

        self.body_layout.addWidget(self.question_frame)

        self.answers_frame = QFrame(self.main_body)
        self.answers_frame.setObjectName("answers_frame")
        sizePolicy1.setHeightForWidth(
            self.answers_frame.sizePolicy().hasHeightForWidth()
        )
        self.answers_frame.setSizePolicy(sizePolicy1)
        self.answers_frame.setStyleSheet("padding: 0;")
        self.answers_frame.setFrameShape(QFrame.StyledPanel)
        self.answers_frame.setFrameShadow(QFrame.Raised)
        self.answers_layout = QVBoxLayout(self.answers_frame)
        self.answers_layout.setSpacing(11)
        self.answers_layout.setObjectName("answers_layout")
        self.answers_layout.setContentsMargins(0, -1, 0, -1)
        self.frame_a = QFrame(self.answers_frame)
        self.frame_a.setObjectName("frame_a")
        self.frame_a.setStyleSheet(
            "background-color: #e1e1e1;\n" "border-radius: 20px;\n" "border: none;"
        )
        self.frame_a.setFrameShape(QFrame.StyledPanel)
        self.frame_a.setFrameShadow(QFrame.Raised)
        self.layout_a = QVBoxLayout(self.frame_a)
        self.layout_a.setSpacing(0)
        self.layout_a.setObjectName("layout_a")
        self.layout_a.setContentsMargins(11, 0, 0, 0)
        self.btn_a = ClickableLabel(self.frame_a)
        self.btn_a.setObjectName("btn_a")
        font3 = QFont()
        font3.setPointSize(11)
        self.btn_a.setFont(font3)

        self.layout_a.addWidget(self.btn_a)

        self.answers_layout.addWidget(self.frame_a)

        self.frame_b = QFrame(self.answers_frame)
        self.frame_b.setObjectName("frame_b")
        self.frame_b.setStyleSheet(
            "background-color: #e1e1e1;\n" "border-radius: 20px;\n" "border: none;"
        )
        self.frame_b.setFrameShape(QFrame.StyledPanel)
        self.frame_b.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_b)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(11, 0, 0, 0)
        self.btn_b = ClickableLabel(self.frame_b)
        self.btn_b.setObjectName("btn_b")
        self.btn_b.setFont(font3)

        self.horizontalLayout.addWidget(self.btn_b)

        self.answers_layout.addWidget(self.frame_b)

        self.frame_c = QFrame(self.answers_frame)
        self.frame_c.setObjectName("frame_c")
        self.frame_c.setStyleSheet(
            "background-color: #e1e1e1;\n" "border-radius: 20px;\n" "border: none;"
        )
        self.frame_c.setFrameShape(QFrame.StyledPanel)
        self.frame_c.setFrameShadow(QFrame.Raised)
        self.layout = QVBoxLayout(self.frame_c)
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")
        self.layout.setContentsMargins(-1, 0, 0, 0)
        self.btn_c = ClickableLabel(self.frame_c)
        self.btn_c.setObjectName("btn_c")
        self.btn_c.setFont(font3)

        self.layout.addWidget(self.btn_c)

        self.answers_layout.addWidget(self.frame_c)

        self.frame_d = QFrame(self.answers_frame)
        self.frame_d.setObjectName("frame_d")
        self.frame_d.setStyleSheet(
            "background-color: #e1e1e1;\n" "border-radius: 20px;\n" "border: none;"
        )
        self.frame_d.setFrameShape(QFrame.StyledPanel)
        self.frame_d.setFrameShadow(QFrame.Raised)
        self.layout_d = QVBoxLayout(self.frame_d)
        self.layout_d.setSpacing(0)
        self.layout_d.setObjectName("layout_d")
        self.layout_d.setContentsMargins(-1, 0, 0, 0)
        self.btn_d = ClickableLabel(self.frame_d)
        self.btn_d.setObjectName("btn_d")
        self.btn_d.setFont(font3)

        self.layout_d.addWidget(self.btn_d)

        self.answers_layout.addWidget(self.frame_d)

        self.body_layout.addWidget(self.answers_frame)

        self.next_question = PushButton(self.main_body)
        self.next_question.setObjectName("next_question")
        font4 = QFont()
        font4.setPointSize(14)
        self.next_question.setFont(font4)

        self.body_layout.addWidget(
            self.next_question, 0, Qt.AlignRight | Qt.AlignBottom
        )

        self.container_layout.addWidget(self.main_body)

        self.contain_body_layout.addWidget(self.container)

        self.central_layout.addWidget(self.body)

        self.status_bar = QFrame(self.centralwidget)
        self.status_bar.setObjectName("status_bar")
        self.status_bar.setStyleSheet(
            "background-color: #b3cdcd;\n" "border-radius: 20px;"
        )
        self.status_bar.setFrameShape(QFrame.StyledPanel)
        self.status_bar.setFrameShadow(QFrame.Raised)
        self.statusbar_layout = QHBoxLayout(self.status_bar)
        self.statusbar_layout.setObjectName("statusbar_layout")
        self.answered = QLabel(self.status_bar)
        self.answered.setObjectName("answered")
        self.answered.setFont(font3)

        self.statusbar_layout.addWidget(self.answered)

        self.unanswered = QLabel(self.status_bar)
        self.unanswered.setObjectName("unanswered")
        self.unanswered.setFont(font3)

        self.statusbar_layout.addWidget(self.unanswered)

        self.central_layout.addWidget(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        MainWindow.setWindowFilePath("")
        self.toggle_btn.setText("")
        self.label.setText(
            QCoreApplication.translate("MainWindow", "IT meydan\u00e7a Quizz", None)
        )
        self.btn1.setText(QCoreApplication.translate("MainWindow", "Sorag 1", None))
        self.btn2.setText(QCoreApplication.translate("MainWindow", "Sorag 2", None))
        self.btn3.setText(QCoreApplication.translate("MainWindow", "Sorag 3", None))
        self.btn4.setText(QCoreApplication.translate("MainWindow", "Sorag 4", None))
        self.btn5.setText(QCoreApplication.translate("MainWindow", "Sorag 5", None))
        self.btn6.setText(QCoreApplication.translate("MainWindow", "Sorag 6", None))
        self.btn7.setText(QCoreApplication.translate("MainWindow", "Sorag 7", None))
        self.btn8.setText(QCoreApplication.translate("MainWindow", "Sorag 8", None))
        self.btn9.setText(QCoreApplication.translate("MainWindow", "Sorag 9", None))
        self.btn10.setText(QCoreApplication.translate("MainWindow", "Sorag 10", None))
        self.prev_btn.setText("")
        self.next_btn.setText("")
        self.question_id.setText(
            QCoreApplication.translate("MainWindow", "Sorag \u21161", None)
        )
        self.question.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.btn_a.setText(QCoreApplication.translate("MainWindow", "A", None))
        self.btn_b.setText(QCoreApplication.translate("MainWindow", "B", None))
        self.btn_c.setText(QCoreApplication.translate("MainWindow", "C", None))
        self.btn_d.setText(QCoreApplication.translate("MainWindow", "D", None))
        self.next_question.setText("Tassyklamak")
        # if QT_CONFIG(shortcut)
        self.next_question.setShortcut(
            QCoreApplication.translate("MainWindow", "Return", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.answered.setText(
            QCoreApplication.translate("MainWindow", "Jogap berilen:", None)
        )
        self.unanswered.setText(
            QCoreApplication.translate("MainWindow", "Jogap berilmedik:", None)
        )

    # retranslateUi
