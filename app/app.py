import os
import pathlib
import random
import shelve
import sys
from pathlib import Path

import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *
from ui.custom_objects import AnimationShadowEffect
from ui.login import Ui_LoginWindow
from ui.quizz import Ui_MainWindow
from ui.table import Ui_TableWindow

file_path = str(Path(__file__).parent).replace("\\", "/") + "/"

with shelve.open(file_path + "data") as file:
    api_url = file["api_url"]


class TimerThread(QThread):
    def __init__(self, minutes: int, parent=None):
        QThread.__init__(self, parent)
        self.time = [minutes, 0]

    def run(self):

        while self.time[0] >= 0 and self.time[1] >= 0:
            if self.time[0] == 0 and self.time[1] - 1 == -1:
                break
            if self.time[1] - 1 == -1:
                self.time[0] -= 1
                self.time[1] = 59
            else:
                self.time[1] -= 1

            if self.time[0] < 1:
                if self.time[1] % 2 == 1:
                    stylesheet = "color: red;"
                else:
                    stylesheet = "color: black;"
                window.ui.label.setStyleSheet(stylesheet)
            minute_str = str(self.time[0]) if self.time[0] >= 10 else f"0{self.time[0]}"
            second_str = str(self.time[1]) if self.time[1] >= 10 else f"0{self.time[1]}"
            self.time_str = minute_str + ":" + second_str
            self.sleep(1)

            window.ui.label.setText(self.time_str)
        window.ui.finish_thread_btn.click()


class AuthorizationRequestThread(QThread):
    def __init__(
        self,
        name,
        surname,
        parent=None,
    ):
        QThread.__init__(self, parent)
        self.name = name
        self.surname = surname

    def run(self):
        enable_chars = ("qwertyuiopasdfghjklzxcvbnm", "1234567890")
        password = ""
        username = (
            (self.name + self.surname)
            .lower()
            .replace("ý", "y")
            .replace("ž", "zh")
            .replace("ä", "a")
            .replace("ç", "ch")
            .replace("ş", "sh")
            .replace("ň", "n")
            .replace("ö", "o")
            .replace("ü", "u")
        )
        for i in range(random.randint(8, 12)):
            in_choice = random.randint(0, 1)
            if in_choice == 0:
                letter_id = random.randint(0, 25)
                password += random.choice(
                    (
                        enable_chars[0][letter_id].upper(),
                        enable_chars[0][letter_id].lower(),
                    )
                )
            else:
                password += enable_chars[1][random.randint(0, 9)]
        try:
            user_url = f"{api_url}/api/v1/auth/users/"
            journal_url = f"{api_url}/api/v1/auth-journal/create"
            login_url = f"{api_url}/api/v1/auth/token/login"

            payload = {
                "first_name": self.name,
                "last_name": self.surname,
                "username": username,
                "password": password,
                "email": "stub@email.com",
            }
            payload_dub = {
                "name": self.name,
                "surname": self.surname,
                "username": username,
                "password": password,
            }

            files = []
            headers = {}

            self.user_response = requests.request(
                "POST", user_url, headers=headers, data=payload, files=files
            ).json()

            if (
                self.user_response["username"][0]
                == "A user with that username already exists."
                or self.user_response["username"][0]
                == "Пользователь с таким именем уже существует."
            ):
                url = f"{api_url}/api/v1/auth-journal/" + username
                response = requests.request(
                    "GET", url, headers=headers, files=files
                ).json()
                login_payload = {
                    "username": response[0]["username"],
                    "password": response[0]["password"],
                }
            else:
                response = requests.request(
                    "POST", journal_url, headers=headers, data=payload_dub, files=files
                ).json()
                login_payload = {
                    "username": response["username"],
                    "password": response["password"],
                }

            self.login_response = requests.request(
                "POST", login_url, headers=headers, data=login_payload, files=files
            ).json()
            MainWindow.token = "Token " + self.login_response["auth_token"]
            self.connection_exception = False
        except requests.exceptions.ConnectionError:
            self.connection_exception = True


class ChallengeListRequestThread(QThread):
    def __init__(self, auth_token: str, parent=None):
        QThread.__init__(self, parent)
        self.token = auth_token

    def run(self):
        url = f"{api_url}/api/v1/challengelist/"

        payload = {}
        files = []
        headers = {"Authorization": self.token}

        try:
            QMainWindow.challenge_list = requests.request(
                "GET", url, headers=headers, data=payload, files=files
            ).json()
            self.connection_exception = False
        except requests.exceptions.ConnectionError:
            self.connection_exception = True


class MainWindow(QMainWindow):
    stylesheet = """
        QPushButton{
            padding: 10px;
            background-color: #e1e1e1;
            border: none;
        }
        QPushButton:hover{
            background-color: #ffffff;
            effect = QtWidgets.QGraphicsDropShadowEffect(QPushButton);
            effect.setOffset(0, 0);
            effect.setBlurRadius(20);
            effect.setColor(QColor(57, 219, 255));
            QPushButton.setGraphicsEffect(effect);
        }
        """
    accept_stylesheet = """
        QPushButton{    
            padding: 16px;
            padding-left: 25px;
            padding-right: 25px;
            border-radius: 25px;
        }
        QPushButton:hover{
            background-color: #ffffff;
            effect = QtWidgets.QGraphicsDropShadowEffect(QPushButton);
            effect.setOffset(0, 0);
            effect.setBlurRadius(20);
            effect.setColor(QColor(57, 219, 255));
            QPushButton.setGraphicsEffect(effect);
        }
        """

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.finish = pyqtSignal(str)

    def create_login_ui(self):
        self.login_ui = Ui_LoginWindow()
        self.login_ui.setupUi(self)
        self.login_ui.accept_btn.setStyleSheet(self.accept_stylesheet)
        self.accept_btn_ani = AnimationShadowEffect(
            Qt.GlobalColor.green, self.login_ui.accept_btn
        )

        self.login_ui.accept_btn.hover.connect(self.accept_hover)
        self.login_ui.accept_btn.setGraphicsEffect(self.accept_btn_ani)

        self.login_ui.accept_btn.clicked.connect(self.accept)

    def create_table_ui(self):
        self.table_ui = Ui_TableWindow()
        self.table_ui.setupUi(self)

        self.table_ui.page = 0

        self.table_ui.btns_list = (
            self.table_ui.c_btn1,
            self.table_ui.c_btn2,
            self.table_ui.c_btn3,
            self.table_ui.c_btn4,
            self.table_ui.c_btn5,
            self.table_ui.c_btn6,
            self.table_ui.c_btn7,
            self.table_ui.c_btn8,
        )

        self.table_ui.paginated_challenge_list = [[]]
        j = 0
        for i in self.challenge_list:
            self.table_ui.paginated_challenge_list[j].append(i)
            if len(self.table_ui.paginated_challenge_list[j]) == 8:
                self.table_ui.paginated_challenge_list.append([])
                j += 1
        if self.table_ui.paginated_challenge_list[j] == []:
            self.table_ui.paginated_challenge_list.pop(j)

        if len(self.table_ui.paginated_challenge_list[self.table_ui.page]) < 8:
            for btn in self.table_ui.btns_list[
                len(self.table_ui.paginated_challenge_list[self.table_ui.page]) : 8
            ]:
                btn.setHidden(True)

        for i in range(len(self.table_ui.paginated_challenge_list[self.table_ui.page])):
            self.table_ui.btns_list[i].setText(
                self.table_ui.paginated_challenge_list[self.table_ui.page][i]["name"]
            )

        self.table_ui.t_prev_btn.clicked.connect(self.prev_table_page)
        self.table_ui.t_next_btn.clicked.connect(self.next_table_page)

        self.table_ui.c_btn1.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn1.text())
        )
        self.table_ui.c_btn2.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn2.text())
        )
        self.table_ui.c_btn3.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn3.text())
        )
        self.table_ui.c_btn4.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn4.text())
        )
        self.table_ui.c_btn5.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn5.text())
        )
        self.table_ui.c_btn6.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn6.text())
        )
        self.table_ui.c_btn7.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn7.text())
        )
        self.table_ui.c_btn8.clicked.connect(
            lambda: self.choose_challenge(self.table_ui.c_btn8.text())
        )

    def create_main_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.side_menu.setHidden(True)
        self.menu_status = False

        self.ui.toggle_btn.clicked.connect(self.toggle_menu)

        self.ui.page = 0
        print(self.ui.page)

        self.ui.btns_list = (
            self.ui.btn1,
            self.ui.btn2,
            self.ui.btn3,
            self.ui.btn4,
            self.ui.btn5,
            self.ui.btn6,
            self.ui.btn7,
            self.ui.btn8,
            self.ui.btn9,
            self.ui.btn10,
        )

        self.ui.paginated_question_list = [[]]
        random.shuffle(self.selected_challenge)
        j = 0
        for i in self.selected_challenge:
            i["is_answered"] = False
            self.ui.paginated_question_list[j].append(i)
            if len(self.ui.paginated_question_list[j]) == 10:
                self.ui.paginated_question_list.append([])
                j += 1

        if self.ui.paginated_question_list[j] == []:
            self.ui.paginated_question_list.pop(j)

        if len(self.ui.paginated_question_list[self.ui.page]) < 10:
            for btn in self.ui.btns_list[
                len(self.ui.paginated_question_list[self.ui.page]) : 10
            ]:
                btn.setHidden(True)

        for i in range(len(self.ui.paginated_question_list[self.ui.page])):
            label = (self.ui.page * 10) + (i + 1)
            self.ui.btns_list[i].setText(f"Sorag {label}")

        self.ui.question.setText(
            self.ui.paginated_question_list[self.ui.page][0]["question"]
        )

        question_id = self.ui.paginated_question_list[self.ui.page][0]["id"]

        self.current_answers = requests.request(
            "GET",
            url=f"{api_url}/api/v1/answerfilter/{question_id}/",
            headers={"Authorization": self.token},
        ).json()
        random.shuffle(self.current_answers)

        label_tuple = (self.ui.btn_a, self.ui.btn_b, self.ui.btn_c, self.ui.btn_d)

        for index in range(len(self.current_answers)):
            label_tuple[index].setText(self.current_answers[index]["answer"])

        self.ui.question_id.setText("Sorag №1")

        self.ui.next_btn.setStyleSheet(self.stylesheet)
        self.ui.prev_btn.setStyleSheet(self.stylesheet)
        self.ui.next_question.setStyleSheet(self.stylesheet)

        self.next_question_ani = AnimationShadowEffect(
            Qt.GlobalColor.green, self.ui.next_btn
        )

        self.ui.finish_thread_btn = QPushButton()
        self.ui.finish_thread_btn.clicked.connect(self.finish_thread)

        self.ui.next_question.hover.connect(self.button_question_hover)
        self.ui.next_question.setGraphicsEffect(self.next_question_ani)

        self.ui.btn_a.clicked.connect(self.select_a)
        self.ui.btn_b.clicked.connect(self.select_b)
        self.ui.btn_c.clicked.connect(self.select_c)
        self.ui.btn_d.clicked.connect(self.select_d)

        self.ui.prev_btn.clicked.connect(self.prev_question_page)
        self.ui.next_btn.clicked.connect(self.next_question_page)

        self.ui.btn1.clicked.connect(lambda: self.select_question(self.ui.btn1.text()))
        self.ui.btn2.clicked.connect(lambda: self.select_question(self.ui.btn2.text()))
        self.ui.btn3.clicked.connect(lambda: self.select_question(self.ui.btn3.text()))
        self.ui.btn4.clicked.connect(lambda: self.select_question(self.ui.btn4.text()))
        self.ui.btn5.clicked.connect(lambda: self.select_question(self.ui.btn5.text()))
        self.ui.btn6.clicked.connect(lambda: self.select_question(self.ui.btn6.text()))
        self.ui.btn7.clicked.connect(lambda: self.select_question(self.ui.btn7.text()))
        self.ui.btn8.clicked.connect(lambda: self.select_question(self.ui.btn8.text()))
        self.ui.btn9.clicked.connect(lambda: self.select_question(self.ui.btn9.text()))
        self.ui.btn10.clicked.connect(
            lambda: self.select_question(self.ui.btn10.text())
        )
        self.ui.next_question.clicked.connect(
            lambda: self.next_question(self.ui.question_id.text())
        )

    def select_question(self, question: str):
        question_index = int(question.split()[1]) - 1

        self.ui.question_id.setText(f"Sorag №{question_index + 1}")

        self.ui.question.setText(
            self.ui.paginated_question_list[self.ui.page][question_index]["question"]
        )

        question_id = self.ui.paginated_question_list[self.ui.page][question_index][
            "id"
        ]

        url = f"{api_url}/api/v1/answerfilter/{question_id}/"
        headers = {"Authorization": self.token}

        self.current_answers = requests.request("GET", url=url, headers=headers).json()
        random.shuffle(self.current_answers)

        try:
            label_tuple = (self.ui.btn_a, self.ui.btn_b, self.ui.btn_c, self.ui.btn_d)

            for index in range(len(self.current_answers)):
                label_tuple[index].setText(self.current_answers[index]["answer"])
        except:
            pass

    def prev_question_page(self):
        self.ui.page -= 1 if self.ui.page > 0 else 0

        for btn in self.ui.btns_list:
            btn.setHidden(False)
        if len(self.ui.paginated_question_list[self.ui.page]) < 10:
            for btn in self.ui.btns_list[
                len(self.ui.paginated_question_list[self.ui.page]) : 10
            ]:
                btn.setHidden(True)

        for i in range(len(self.ui.paginated_question_list[self.ui.page])):
            label = (self.ui.page * 10) + (i + 1)
            self.ui.btns_list[i].setText(f"Sorag {label}")

    def next_question_page(self):
        self.ui.page += (
            1 if self.ui.page < len(self.ui.paginated_question_list) - 1 else 0
        )

        for btn in self.ui.btns_list:
            btn.setHidden(False)

        if len(self.ui.paginated_question_list[self.ui.page]) < 10:
            for btn in self.ui.btns_list[
                len(self.ui.paginated_question_list[self.ui.page]) : 10
            ]:
                btn.setHidden(True)

        for i in range(len(self.ui.paginated_question_list[self.ui.page])):
            label = (self.ui.page * 10) + (i + 1)
            self.ui.btns_list[i].setText(f"Sorag {label}")

    def select_a(self):
        self.ui.btn_b.setChecked(False)
        self.ui.btn_c.setChecked(False)
        self.ui.btn_d.setChecked(False)

    def select_b(self):
        self.ui.btn_a.setChecked(False)
        self.ui.btn_c.setChecked(False)
        self.ui.btn_d.setChecked(False)

    def select_c(self):
        self.ui.btn_b.setChecked(False)
        self.ui.btn_a.setChecked(False)
        self.ui.btn_d.setChecked(False)

    def select_d(self):
        self.ui.btn_b.setChecked(False)
        self.ui.btn_c.setChecked(False)
        self.ui.btn_a.setChecked(False)

    def set_text(self, text):
        self.ui.label.setText(text)

    def next_question(self, question: str):

        is_answered = True

        question_index = int(question.split("№")[1]) - 1

        self.ui.paginated_question_list[self.ui.page][question_index][
            "is_answered"
        ] = True

        while is_answered:
            try:
                question_index += 1
                is_answered = self.ui.paginated_question_list[self.ui.page][
                    question_index
                ]["is_answered"]
            except IndexError:
                question_index = 0
                if self.ui.page + 1 == len(self.ui.paginated_question_list):
                    print("that's all")
                else:
                    self.ui.page += 1
                    is_answered = self.ui.paginated_question_list[self.ui.page][
                        question_index
                    ]["is_answered"]

        self.ui.question.setText(
            self.ui.paginated_question_list[self.ui.page][question_index]["question"]
        )

        question_id = self.ui.paginated_question_list[self.ui.page][question_index][
            "id"
        ]

        self.current_answers = requests.request(
            "GET",
            url=f"{api_url}/api/v1/answerfilter/{question_id}/",
            headers={"Authorization": self.token},
        ).json()
        random.shuffle(self.current_answers)

        label_tuple = (self.ui.btn_a, self.ui.btn_b, self.ui.btn_c, self.ui.btn_d)

        for index in range(len(self.current_answers)):
            label_tuple[index].setText(self.current_answers[index]["answer"])

        self.ui.question_id.setText(f"Sorag №{question_index + 1}")

    def choose_challenge(self, challenge_name):
        del self.table_ui

        for challenge in self.challenge_list:
            if challenge["name"] == challenge_name:
                selected_challenge_id = challenge["id"]

        url = f"{api_url}/api/v1/questionfilter/{selected_challenge_id}/"
        headers = {"Authorization": self.token}

        self.selected_challenge = requests.request(
            "GET", url=url, headers=headers
        ).json()

        self.create_main_ui()

        self.time = [2, 0]
        minute_str = str(self.time[0]) if self.time[0] >= 10 else f"0{self.time[0]}"
        second_str = "00"
        self.time_str = minute_str + ":" + second_str
        self.ui.label.setText(self.time_str)

        self.ui.label.setText(self.time_str)

        self.timer_thread = TimerThread(2)
        self.timer_thread.start(QThread.Priority.InheritPriority)

    def prev_table_page(self):
        self.table_ui.page -= 1 if self.table_ui.page > 0 else 0

        for btn in self.table_ui.btns_list:
            btn.setHidden(False)
        if len(self.table_ui.paginated_challenge_list[self.table_ui.page]) < 8:
            for btn in self.table_ui.btns_list[
                len(self.table_ui.paginated_challenge_list[self.table_ui.page]) : 8
            ]:
                btn.setHidden(True)

        for i in range(len(self.table_ui.paginated_challenge_list[self.table_ui.page])):
            self.table_ui.btns_list[i].setText(
                self.table_ui.paginated_challenge_list[self.table_ui.page][i]["name"]
            )

    def next_table_page(self):
        self.table_ui.page += (
            1
            if self.table_ui.page < len(self.table_ui.paginated_challenge_list) - 1
            else 0
        )

        for btn in self.table_ui.btns_list:
            btn.setHidden(False)

        if len(self.table_ui.paginated_challenge_list[self.table_ui.page]) < 8:
            for btn in self.table_ui.btns_list[
                len(self.table_ui.paginated_challenge_list[self.table_ui.page]) : 8
            ]:
                btn.setHidden(True)

        for i in range(len(self.table_ui.paginated_challenge_list[self.table_ui.page])):
            self.table_ui.btns_list[i].setText(
                self.table_ui.paginated_challenge_list[self.table_ui.page][i]["name"]
            )

    def finish_thread(self):
        timeout_window()

    def accept(self):
        name = self.login_ui.name_input.text()
        surname = self.login_ui.surname_input.text()
        cyrillic = "ёйцукенгшщзхъфывапролджэячсмитьбю"
        symbols = ".,/\\`'[]()!@#$%^&*№:;{}<>?+=-_" + '"'
        filling_error = False
        for char in name.lower() + surname.lower():
            if char in symbols or char in cyrillic:
                filling_error = True
                break
        if filling_error:
            message = "Girizen maglumatlaryňyzda kabul\nedilmeýän simwollar ulanylypdyr!\nTäzeden synanyşmagyňyzy haýyş\nedýäris!"
            self.login_ui.name_input.setText("")
            self.login_ui.surname_input.setText("")
            modal_info_window(message)
        elif name == "" or surname == "":
            if name == "" and surname == "":
                message = "Adyňyzy we familiýaňyzy\ngirizmegiňizi haýyş edýäris!"
            elif name == "" and not surname == "":
                message = "Adyňyzy girizmegiňizi\nhaýyş edýäris!"
            elif surname == "" and not name == "":
                message = "Familiýaňyzy girizmegiňizi\nhaýyş edýäris!"
            modal_info_window(message)
        else:
            self.auth_request_thread = AuthorizationRequestThread(name, surname)
            self.auth_request_thread.start(QThread.Priority.InheritPriority)
            while self.auth_request_thread.isFinished() == False:
                pass
            if self.auth_request_thread.connection_exception:
                message = "Serwer bilen baglanyşyk pursatynda\nnäsazlyk ýüze çykdy! Ethernet\nkabeliňizi barlaň ýa-da\nadministratorlara ýüz tutuň!"
                modal_info_window(message)
            else:
                self.challenge_list_request_thread = ChallengeListRequestThread(
                    self.token
                )
                self.challenge_list_request_thread.start(
                    QThread.Priority.InheritPriority
                )
                while self.challenge_list_request_thread.isFinished() == False:
                    pass
                if self.challenge_list_request_thread.connection_exception:
                    message = "Serwer bilen baglanyşyk pursatynda\nnäsazlyk ýüze çykdy! Ethernet\nkabeliňizi barlaň ýa-da\nadministratorlara ýüz tutuň!"
                    modal_info_window(message)
                else:
                    del self.login_ui
                    self.create_table_ui()

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        if e.key() == 16777220 and self.login_ui.name_input.hasFocus():
            self.login_ui.surname_input.setFocus(Qt.FocusReason.ShortcutFocusReason)
        elif e.key() == 16777220 and self.login_ui.surname_input.hasFocus():
            self.login_ui.accept_btn.click()
        QMainWindow.keyPressEvent(self, e)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        try:
            if self.ui.menu_status == False:
                self.ui.side_menu.setHidden(True)
        except:
            pass

        QMainWindow.resizeEvent(self, e)

    def toggle_menu(self):
        self.menu_status = True if self.menu_status == False else False

        if self.menu_status == False:

            self.eff = QGraphicsOpacityEffect()
            self.eff.setOpacity(1.0)
            self.ui.side_menu.setGraphicsEffect(self.eff)

            self.op_anim = QPropertyAnimation(
                self.eff, b"opacity", duration=500, startValue=1.0, endValue=0.0
            )

            self.pos_anim = QPropertyAnimation(
                self.ui.side_menu,
                b"pos",
                duration=500,
                startValue=QPoint(11, 11),
                endValue=QPoint(-41, 11),
            )
            toggle_icon = QIcon()
            toggle_icon.addFile(
                ":/icons/bootstrap-icons/list.svg", QSize(), QIcon.Normal, QIcon.Off
            )
            self.ui.toggle_btn.setIcon(toggle_icon)
            self.op_anim.setEasingCurve(QEasingCurve.InOutCubic)
            self.pos_anim.setEasingCurve(QEasingCurve.InOutCubic)

            self.block_pos_anim = QPropertyAnimation(
                self.ui.main_body,
                b"pos",
                duration=500,
                startValue=QPoint(179, 11),
                endValue=QPoint(11, 11),
            )
            self.block_pos_anim.setEasingCurve(QEasingCurve.InOutCubic)

            self.size_anim = QPropertyAnimation(
                self.ui.main_body,
                b"size",
                startValue=QSize(self.ui.main_body.size()),
                endValue=QSize(
                    self.ui.main_body.size().width() + 130,
                    self.ui.main_body.size().height(),
                ),
            )

            self.size_anim.setEasingCurve(QEasingCurve.InOutCubic)

        else:
            self.eff = QGraphicsOpacityEffect()
            self.eff.setOpacity(0.0)
            self.ui.side_menu.setGraphicsEffect(self.eff)

            self.op_anim = QPropertyAnimation(
                self.eff, b"opacity", duration=500, startValue=0.0, endValue=1.0
            )

            self.pos_anim = QPropertyAnimation(
                self.ui.side_menu,
                b"pos",
                duration=500,
                startValue=QPoint(-41, 11),
                endValue=QPoint(11, 11),
            )
            toggle_icon = QIcon()
            toggle_icon.addFile(
                ":/icons/bootstrap-icons/chevron-double-left.svg",
                QSize(),
                QIcon.Normal,
                QIcon.Off,
            )
            self.ui.toggle_btn.setIcon(toggle_icon)
            self.op_anim.setEasingCurve(QEasingCurve.InOutCubic)
            self.pos_anim.setEasingCurve(QEasingCurve.InOutCubic)

            QTimer.singleShot(500, lambda: self.ui.side_menu.setHidden(False))

            self.block_pos_anim = QPropertyAnimation(
                self.ui.main_body,
                b"pos",
                duration=500,
                startValue=QPoint(11, 11),
                endValue=QPoint(169, 11),
            )

            self.size_anim = QPropertyAnimation(
                self.ui.main_body,
                b"size",
                startValue=QSize(self.ui.main_body.size()),
                endValue=QSize(
                    self.ui.main_body.size().width() - 130,
                    self.ui.main_body.size().height(),
                ),
            )

            self.size_anim.setEasingCurve(QEasingCurve.InOutCubic)

            self.block_pos_anim.setEasingCurve(QEasingCurve.InOutCubic)

        self.group = QParallelAnimationGroup(self.ui.side_menu)
        self.group.addAnimation(self.op_anim)
        self.group.addAnimation(self.pos_anim)
        self.group.start(QAbstractAnimation.DeleteWhenStopped)
        self.group1 = QParallelAnimationGroup(self.ui.main_body)
        self.group1.addAnimation(self.size_anim)
        self.group1.addAnimation(self.block_pos_anim)
        self.group1.start(QAbstractAnimation.DeleteWhenStopped)

    def button_question_hover(self, hover):
        if hover == "enterEvent":
            self.next_question_ani.start()
        elif hover == "leaveEvent":
            self.next_question_ani.stop()

    def accept_hover(self, hover):
        if hover == "enterEvent":
            self.accept_btn_ani.start()
        elif hover == "leaveEvent":
            self.accept_btn_ani.stop()


def modal_info_window(message: str):
    global modal_window
    modal_window = QWidget(window, Qt.WindowType.FramelessWindowHint)
    modal_window.setFixedSize(400, 200)
    modal_window.setWindowModality(Qt.WindowModality.WindowModal)
    modal_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
    modal_window.move(
        window.geometry().center() - modal_window.rect().center() - QPoint(4, 30)
    )
    vbox = QVBoxLayout(modal_window)
    stylesheet = """
        background-color: #d55c5c;
        border-radius: 20px;
        border: 1px solid white;
    """
    btn_stylesheet = """
        padding: 10px;
        background-color: white;
        border-radius: 15px;
    """
    label_stylesheet = """
        color: white;
        border: none;
    """
    font = QFont()
    font.setPointSize(14)
    modal_window.setLayout(vbox)
    modal_window.setStyleSheet(stylesheet)
    label = QLabel(message)
    label.setStyleSheet(label_stylesheet)
    label.setFont(font)
    label.setAlignment(Qt.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    ok_btn = QPushButton("OK")
    ok_btn.setStyleSheet(btn_stylesheet)
    ok_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    ok_btn.setFont(font)
    vbox.addWidget(label)
    vbox.addWidget(ok_btn, 0, Qt.AlignHCenter | Qt.AlignVCenter)
    ok_btn.clicked.connect(lambda: modal_window.close())
    modal_window.show()


def timeout_window():
    global modal_window
    message = "Wagt doldy!\nÇykyşyňyzy tassyklaň"
    modal_window = QWidget(window, Qt.WindowType.FramelessWindowHint)
    modal_window.setFixedSize(400, 200)
    modal_window.setWindowModality(Qt.WindowModality.WindowModal)
    modal_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
    modal_window.move(
        window.geometry().center() - modal_window.rect().center() - QPoint(4, 30)
    )
    vbox = QVBoxLayout(modal_window)
    stylesheet = """
        background-color: white;
        border-radius: 20px;
        border: 1px solid #7a7a7a;
    """
    btn_stylesheet = """
        padding: 10px;
        background-color: 7a7a7a;
        border-radius: 15px;
    """
    label_stylesheet = """
        color: black;
        border: none;
    """
    font = QFont()
    font.setPointSize(14)
    modal_window.setLayout(vbox)
    modal_window.setStyleSheet(stylesheet)
    label = QLabel(message)
    label.setStyleSheet(label_stylesheet)
    label.setFont(font)
    label.setAlignment(Qt.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    ok_btn = QPushButton("Çykyş")
    ok_btn.setStyleSheet(btn_stylesheet)
    ok_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    ok_btn.setFont(font)
    vbox.addWidget(label)
    vbox.addWidget(ok_btn, 0, Qt.AlignHCenter | Qt.AlignVCenter)
    ok_btn.clicked.connect(lambda: app.quit())
    modal_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.create_login_ui()
    window.show()
    sys.exit(app.exec_())
