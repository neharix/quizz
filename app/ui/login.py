import icons_rc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .custom_objects import PushButton


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(1153, 648)
        LoginWindow.setStyleSheet("background-color: #e1e1e1;")
        self.centralwidget = QWidget(LoginWindow)
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
        self.l_central_layout = QVBoxLayout(self.centralwidget)
        self.l_central_layout.setSpacing(7)
        self.l_central_layout.setObjectName("l_central_layout")
        self.l_central_layout.setContentsMargins(11, 11, 11, 11)
        self.l_main_body = QFrame(self.centralwidget)
        self.l_main_body.setObjectName("l_main_body")
        self.l_main_body.setFrameShape(QFrame.StyledPanel)
        self.l_main_body.setFrameShadow(QFrame.Raised)
        self.l_main_layout = QVBoxLayout(self.l_main_body)
        self.l_main_layout.setObjectName("l_main_layout")
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
        self.box_layout = QVBoxLayout(self.box)
        self.box_layout.setObjectName("box_layout")
        self.name_frame = QFrame(self.box)
        self.name_frame.setObjectName("name_frame")
        self.name_frame.setMinimumSize(QSize(250, 0))
        self.name_frame.setFrameShape(QFrame.StyledPanel)
        self.name_frame.setFrameShadow(QFrame.Raised)
        self.name_layout = QVBoxLayout(self.name_frame)
        self.name_layout.setObjectName("name_layout")
        self.name_label = QLabel(self.name_frame)
        self.name_label.setObjectName("name_label")
        font = QFont()
        font.setPointSize(14)
        self.name_label.setFont(font)

        self.name_layout.addWidget(self.name_label, 0, Qt.AlignHCenter | Qt.AlignBottom)

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

        self.name_layout.addWidget(self.name_input)

        self.box_layout.addWidget(self.name_frame, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.surname_frame = QFrame(self.box)
        self.surname_frame.setObjectName("surname_frame")
        self.surname_frame.setMinimumSize(QSize(250, 0))
        self.surname_frame.setFrameShape(QFrame.StyledPanel)
        self.surname_frame.setFrameShadow(QFrame.Raised)
        self.surname_layout = QVBoxLayout(self.surname_frame)
        self.surname_layout.setObjectName("surname_layout")
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

        self.surname_layout.addWidget(self.surname_label, 0, Qt.AlignHCenter)

        self.surname_input = QLineEdit(self.surname_frame)
        self.surname_input.setObjectName("surname_input")
        self.surname_input.setFont(font)
        self.surname_input.setStyleSheet(
            "background-color: white;\n"
            "padding: 10px;\n"
            "border-radius: 25px;\n"
            "border: 1px solid #e1e1e1;"
        )

        self.surname_layout.addWidget(self.surname_input)

        self.box_layout.addWidget(
            self.surname_frame, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.accept_frame = QFrame(self.box)
        self.accept_frame.setObjectName("accept_frame")
        self.accept_frame.setFrameShape(QFrame.StyledPanel)
        self.accept_frame.setFrameShadow(QFrame.Raised)
        self.accept_layout = QVBoxLayout(self.accept_frame)
        self.accept_layout.setObjectName("accept_layout")
        self.accept_btn = PushButton(self.accept_frame)
        self.accept_btn.setObjectName("accept_btn")
        font1 = QFont()
        font1.setPointSize(12)
        self.accept_btn.setFont(font1)

        self.accept_layout.addWidget(self.accept_btn)

        self.box_layout.addWidget(self.accept_frame, 0, Qt.AlignHCenter | Qt.AlignTop)

        self.l_main_layout.addWidget(self.box, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        self.l_central_layout.addWidget(self.l_main_body)

        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)

    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(
            QCoreApplication.translate("LoginWindow", "MainWindow", None)
        )
        LoginWindow.setWindowFilePath("")
        self.name_label.setText(QCoreApplication.translate("LoginWindow", "Ady:", None))
        self.surname_label.setText(
            QCoreApplication.translate("LoginWindow", "Famili\u00fdasy:", None)
        )
        self.accept_btn.setText(
            QCoreApplication.translate("LoginWindow", "Tassyklamak", None)
        )

    # retranslateUi
