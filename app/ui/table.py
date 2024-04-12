import icons_rc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_TableWindow(object):
    def setupUi(self, TableWindow):
        if not TableWindow.objectName():
            TableWindow.setObjectName("TableWindow")
        font = QFont()
        font.setPointSize(14)
        TableWindow.setFont(font)
        TableWindow.setStyleSheet("background-color: #e1e1e1;")
        self.centralwidget = QWidget(TableWindow)
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
            "#container_t{\n"
            "	background-color: #b3cdcd;\n"
            "	border-radius: 20px;\n"
            "}"
        )
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setSpacing(7)
        self.central_layout.setObjectName("central_layout")
        self.central_layout.setContentsMargins(11, 11, 11, 11)
        self.t_main_body = QFrame(self.centralwidget)
        self.t_main_body.setObjectName("t_main_body")
        self.t_main_body.setFrameShape(QFrame.StyledPanel)
        self.t_main_body.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.t_main_body)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container_t = QFrame(self.t_main_body)
        self.container_t.setObjectName("container_t")
        self.container_t.setMinimumSize(QSize(600, 560))
        self.container_t.setFrameShape(QFrame.StyledPanel)
        self.container_t.setFrameShadow(QFrame.Raised)
        self.t_container_layout = QVBoxLayout(self.container_t)
        self.t_container_layout.setObjectName("t_container_layout")
        self.t_body = QFrame(self.container_t)
        self.t_body.setObjectName("t_body")
        self.t_body.setStyleSheet(
            "QPushButton{\n"
            "	border-radius: none;\n"
            "}\n"
            "QPushButton:hover{\n"
            "            background-color: #ffffff;\n"
            "}"
        )
        self.t_body.setFrameShape(QFrame.StyledPanel)
        self.t_body.setFrameShadow(QFrame.Raised)
        self.t_body_layout = QVBoxLayout(self.t_body)
        self.t_body_layout.setSpacing(0)
        self.t_body_layout.setObjectName("t_body_layout")
        self.challenge_label = QLabel(self.t_body)
        self.challenge_label.setObjectName("challenge_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.challenge_label.sizePolicy().hasHeightForWidth()
        )
        self.challenge_label.setSizePolicy(sizePolicy)
        self.challenge_label.setFont(font)
        self.challenge_label.setAlignment(Qt.AlignCenter)

        self.t_body_layout.addWidget(
            self.challenge_label, 0, Qt.AlignHCenter | Qt.AlignTop
        )

        self.c_btn1 = QPushButton(self.t_body)
        self.c_btn1.setObjectName("c_btn1")
        self.c_btn1.setFont(font)

        self.t_body_layout.addWidget(self.c_btn1)

        self.c_btn2 = QPushButton(self.t_body)
        self.c_btn2.setObjectName("c_btn2")
        self.c_btn2.setFont(font)

        self.t_body_layout.addWidget(self.c_btn2)

        self.c_btn3 = QPushButton(self.t_body)
        self.c_btn3.setObjectName("c_btn3")
        self.c_btn3.setFont(font)

        self.t_body_layout.addWidget(self.c_btn3)

        self.c_btn4 = QPushButton(self.t_body)
        self.c_btn4.setObjectName("c_btn4")
        self.c_btn4.setFont(font)

        self.t_body_layout.addWidget(self.c_btn4)

        self.c_btn5 = QPushButton(self.t_body)
        self.c_btn5.setObjectName("c_btn5")
        self.c_btn5.setFont(font)

        self.t_body_layout.addWidget(self.c_btn5)

        self.c_btn6 = QPushButton(self.t_body)
        self.c_btn6.setObjectName("c_btn6")
        self.c_btn6.setFont(font)

        self.t_body_layout.addWidget(self.c_btn6)

        self.c_btn7 = QPushButton(self.t_body)
        self.c_btn7.setObjectName("c_btn7")
        self.c_btn7.setFont(font)

        self.t_body_layout.addWidget(self.c_btn7)

        self.c_btn8 = QPushButton(self.t_body)
        self.c_btn8.setObjectName("c_btn8")
        self.c_btn8.setFont(font)

        self.t_body_layout.addWidget(self.c_btn8)

        self.t_pagination_block = QFrame(self.t_body)
        self.t_pagination_block.setObjectName("t_pagination_block")
        self.t_pagination_block.setStyleSheet(
            "QPushButton{\n"
            "	padding: 10px;\n"
            "	background-color: #e1e1e1;\n"
            "	border-radius: 5px;\n"
            "	border: none;\n"
            "}"
        )
        self.t_pagination_block.setFrameShape(QFrame.StyledPanel)
        self.t_pagination_block.setFrameShadow(QFrame.Raised)
        self.t_pagination_layout = QHBoxLayout(self.t_pagination_block)
        self.t_pagination_layout.setObjectName("t_pagination_layout")
        self.t_prev_btn = QPushButton(self.t_pagination_block)
        self.t_prev_btn.setObjectName("t_prev_btn")
        icon = QIcon()
        icon.addFile(
            ":/icons/bootstrap-icons/chevron-left.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.t_prev_btn.setIcon(icon)

        self.t_pagination_layout.addWidget(self.t_prev_btn)

        self.t_next_btn = QPushButton(self.t_pagination_block)
        self.t_next_btn.setObjectName("t_next_btn")
        icon1 = QIcon()
        icon1.addFile(
            ":/icons/bootstrap-icons/chevron-right.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.t_next_btn.setIcon(icon1)

        self.t_pagination_layout.addWidget(self.t_next_btn)

        self.t_body_layout.addWidget(
            self.t_pagination_block, 0, Qt.AlignHCenter | Qt.AlignBottom
        )

        self.t_container_layout.addWidget(self.t_body)

        self.verticalLayout.addWidget(
            self.container_t, 0, Qt.AlignHCenter | Qt.AlignVCenter
        )

        self.central_layout.addWidget(self.t_main_body)

        TableWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TableWindow)

        QMetaObject.connectSlotsByName(TableWindow)

    # setupUi

    def retranslateUi(self, TableWindow):
        TableWindow.setWindowTitle(
            QCoreApplication.translate("TableWindow", "MainWindow", None)
        )
        TableWindow.setWindowFilePath("")
        self.challenge_label.setText(
            QCoreApplication.translate(
                "TableWindow",
                "Gatna\u015fmak isle\u00fd\u00e4n \u00fdary\u015fy\u0148yzy sa\u00fdla\u0148:",
                None,
            )
        )
        self.c_btn1.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 1", None)
        )
        self.c_btn2.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 2", None)
        )
        self.c_btn3.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 3", None)
        )
        self.c_btn4.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 4", None)
        )
        self.c_btn5.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 5", None)
        )
        self.c_btn6.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 6", None)
        )
        self.c_btn7.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 7", None)
        )
        self.c_btn8.setText(
            QCoreApplication.translate("TableWindow", "\u00ddary\u015f 8", None)
        )
        self.t_prev_btn.setText("")
        self.t_next_btn.setText("")

    # retranslateUi
