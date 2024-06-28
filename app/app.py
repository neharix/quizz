import datetime
import os
import random
import shelve
import sys
from pathlib import Path

import requests
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *
from ui.custom_objects import AnimationShadowEffect
from ui.login import Ui_LoginWindow
from ui.quizz import Ui_MainWindow
from ui.result import Ui_ResultWindow
from ui.table import Ui_TableWindow

with shelve.open(str(Path(__file__).parent).replace("\\", "/") + "/data") as file:
    api_url = file["api_url"]

try:
    os.mkdir("C:/quizz_cache")
except:
    pass


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
                try:
                    window.ui.label.setStyleSheet(stylesheet)
                except:
                    pass

            minute_str = str(self.time[0]) if self.time[0] >= 10 else f"0{self.time[0]}"
            second_str = str(self.time[1]) if self.time[1] >= 10 else f"0{self.time[1]}"
            self.time_str = minute_str + ":" + second_str
            self.sleep(1)
            try:
                window.ui.label.setText(self.time_str)
            except:
                pass
        window.ui.finish_thread_btn.click()


class AuthorizationRequestThread(QThread):
    def __init__(self, name, surname, parent=None, about=None):
        QThread.__init__(self, parent)
        self.name = name
        self.surname = surname
        self.about = about

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

                profile_payload = {
                    "about": self.about if self.about != "" else "Default",
                    "user": self.user_response["id"],
                }

                profile_response = requests.request(
                    "POST",
                    f"{api_url}/api/v1/create_profile/",
                    headers={},
                    data=profile_payload,
                ).json()

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
            window.token = "Token " + self.login_response["auth_token"]
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
            window.challenge_list = requests.request(
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

        try:
            if len(self.table_ui.paginated_challenge_list[self.table_ui.page]) < 8:
                for btn in self.table_ui.btns_list[
                    len(self.table_ui.paginated_challenge_list[self.table_ui.page]) : 8
                ]:
                    btn.setHidden(True)

            for i in range(
                len(self.table_ui.paginated_challenge_list[self.table_ui.page])
            ):
                self.table_ui.btns_list[i].setText(
                    self.table_ui.paginated_challenge_list[self.table_ui.page][i][
                        "name"
                    ]
                )
        except IndexError:
            for btn in self.table_ui.btns_list:
                btn.setHidden(True)

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

        self.answers_type = [None, None, None, None]

        self.ui.toggle_btn.clicked.connect(self.toggle_menu)

        self.selected_answer = None

        self.ui.page = 0

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

        self.status_bar = {"answered": 0, "unanswered": len(self.selected_challenge)}
        self.ui.unanswered.setText(
            f"Jogap berilmedik: {self.status_bar.get('unanswered')}"
        )
        self.ui.answered.setText(f"Jogap berilen: 0")

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

        self.question_image_path = None

        if self.ui.paginated_question_list[self.ui.page][0]["is_image"]:
            response = requests.get(
                f"{api_url}/{self.ui.paginated_question_list[self.ui.page][0]['image']}"
            )
            file_name = self.ui.paginated_question_list[self.ui.page][0]["image"].split(
                "/"
            )[3]
            with open(f"C:/quizz_cache/{file_name}", "wb") as file:
                file.write(response.content)
            self.ui.question.setText(f"Suraty görmek üçin sag düwmä basyň")
            self.question_image_path = self.ui.paginated_question_list[self.ui.page][0][
                "image"
            ]
        else:
            self.ui.question.setText(
                self.ui.paginated_question_list[self.ui.page][0]["question"]
            )
        self.question_index = 0
        question_id = self.ui.paginated_question_list[self.ui.page][0]["id"]

        self.current_answers = requests.request(
            "GET",
            url=f"{api_url}/api/v1/answerfilter/{question_id}/",
            headers={"Authorization": self.token},
        ).json()
        random.shuffle(self.current_answers)

        if len(self.current_answers) == 3:
            self.label_tuple = (self.ui.btn_a, self.ui.btn_b, self.ui.btn_c)
            self.ui.btn_d.setEnabled(False)
            self.ui.btn_d.setHidden(True)
            self.ui.frame_d.setEnabled(False)
            self.ui.frame_d.setHidden(True)
        elif len(self.current_answers) == 4:
            self.label_tuple = (
                self.ui.btn_a,
                self.ui.btn_b,
                self.ui.btn_c,
                self.ui.btn_d,
            )
            self.ui.btn_d.setEnabled(True)
            self.ui.btn_d.setHidden(False)
            self.ui.frame_d.setEnabled(True)
            self.ui.frame_d.setHidden(False)

        for index in range(len(self.current_answers)):
            if self.current_answers[index]["is_image"]:
                response = requests.get(
                    f"{api_url}/{self.current_answers[index]['image']}"
                )
                file_name = self.current_answers[index]["image"].split("/")[3]
                with open(f"C:/quizz_cache/{file_name}", "wb") as file:
                    file.write(response.content)
                self.answers_type[index] = "image"
                self.label_tuple[index].setText(
                    f"{index + 1}. Suraty görmek üçin sag düwmä basyň"
                )
            else:
                self.answers_type[index] = "text"
                self.label_tuple[index].setText(self.current_answers[index]["answer"])

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

        self.ui.prev_btn.clicked.connect(self.prev_question_page)
        self.ui.next_btn.clicked.connect(self.next_question_page)

        self.ui.btn_a.clicked.connect(self.select_a)
        self.ui.btn_b.clicked.connect(self.select_b)
        self.ui.btn_c.clicked.connect(self.select_c)
        self.ui.btn_d.clicked.connect(self.select_d)

        self.ui.question.redirect.connect(self.question_redirect)

        self.ui.btn_a.redirect.connect(self.redirect_a)
        self.ui.btn_b.redirect.connect(self.redirect_b)
        self.ui.btn_c.redirect.connect(self.redirect_c)
        self.ui.btn_d.redirect.connect(self.redirect_d)

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

        self.default_stylesheet = """
        background-color: #e1e1e1;
        border-radius: 20px;
        border: none;
        """

        self.selected_stylesheet = """
        background-color: #ffffff;
        border-radius: 20px;
        border: none;
        """

    def create_result_ui(self):
        self.result_ui = Ui_ResultWindow()
        self.result_ui.setupUi(self)

        challenge_id = self.challenge_data[0]["id"]

        headers = {"Authorization": self.token}
        url = f"{api_url}/api/v1/useranswers/{challenge_id}/"
        challenge_url = f"{api_url}/api/v1/challenge/{challenge_id}/"

        response = requests.request("GET", url, headers=headers).json()
        challenge_data = requests.request("GET", challenge_url, headers=headers).json()

        self.result_ui.label.setText(challenge_data[0]["name"])

        true_answer = 0
        false_answer = 0

        for obj in response:
            if obj["is_true"]:
                true_answer += 1
            else:
                false_answer += 1

        self.result_ui.result_label1.setText(f"Dogry jogaplar: {true_answer}")
        self.result_ui.result_label2.setText(f"Ýalňyş jogaplar: {false_answer}")
        self.result_ui.result_label3.setText("")

        chartView = QChartView(self.createPieChart(true_answer, false_answer))
        self.result_ui.verticalLayout.addWidget(chartView)

    def createPieChart(self, true_answers: int, false_answers: int):
        chart = QChart()
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        total = true_answers + false_answers

        try:
            true_percent = round((true_answers / total) * 100)
        except ZeroDivisionError:
            true_percent = 0

        try:
            false_percent = round((false_answers / total) * 100)
        except:
            false_percent = 0

        series = QPieSeries()
        serie1 = QPieSlice(
            f"Dogry: {true_percent}%", true_percent, color=QColor("#63e870")
        )
        serie1.setLabelVisible(True)
        serie1.setPen(QPen(Qt.GlobalColor.gray))

        serie2 = QPieSlice(
            f"Yalňyş: {false_percent}%", false_percent, color=QColor("#e86363")
        )
        serie2.setLabelVisible(True)
        serie2.setPen(QPen(Qt.GlobalColor.gray))

        series.append(serie1)
        series.append(serie2)

        chart.addSeries(series)

        return chart

    def question_redirect(self):
        if self.ui.paginated_question_list[self.ui.page][self.question_index][
            "is_image"
        ]:
            file_name = self.question_image_path.split("/")[3]
            image_window(f"C:/quizz_cache/{file_name}")

    def redirect_a(self):
        if self.current_answers[0]["is_image"]:
            file_name = self.current_answers[0]["image"].split("/")[3]
            image_window(f"C:/quizz_cache/{file_name}")
        if self.answers_type[0] == "image":
            self.selected_answer = self.current_answers[0]["id"]
        elif self.answers_type[0] == "text":
            self.selected_answer = self.ui.btn_a.text()
        self.ui.frame_a.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_b.setStyleSheet(self.default_stylesheet)
        self.ui.frame_c.setStyleSheet(self.default_stylesheet)
        self.ui.frame_d.setStyleSheet(self.default_stylesheet)

    def redirect_b(self):
        if self.current_answers[1]["is_image"]:
            file_name = self.current_answers[1]["image"].split("/")[3]
            image_window(f"C:/quizz_cache/{file_name}")
        if self.answers_type[1] == "image":
            self.selected_answer = self.current_answers[1]["id"]
        elif self.answers_type[1] == "text":
            self.selected_answer = self.ui.btn_b.text()
        self.ui.frame_b.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_a.setStyleSheet(self.default_stylesheet)
        self.ui.frame_c.setStyleSheet(self.default_stylesheet)
        self.ui.frame_d.setStyleSheet(self.default_stylesheet)

    def redirect_c(self):
        if self.current_answers[2]["is_image"]:
            file_name = self.current_answers[2]["image"].split("/")[3]
            image_window(f"C:/quizz_cache/{file_name}")
        if self.answers_type[2] == "image":
            self.selected_answer = self.current_answers[2]["id"]
        elif self.answers_type[2] == "text":
            self.selected_answer = self.ui.btn_c.text()
        self.ui.frame_c.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_a.setStyleSheet(self.default_stylesheet)
        self.ui.frame_b.setStyleSheet(self.default_stylesheet)
        self.ui.frame_d.setStyleSheet(self.default_stylesheet)

    def redirect_d(self):
        if self.current_answers[3]["is_image"]:
            file_name = self.current_answers[3]["image"].split("/")[3]
            image_window(f"C:/quizz_cache/{file_name}")
        if self.answers_type[3] == "image":
            self.selected_answer = self.current_answers[3]["id"]
        elif self.answers_type[3] == "text":
            self.selected_answer = self.ui.btn_d.text()
        self.ui.frame_d.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_a.setStyleSheet(self.default_stylesheet)
        self.ui.frame_b.setStyleSheet(self.default_stylesheet)
        self.ui.frame_c.setStyleSheet(self.default_stylesheet)

    def select_a(self):
        if self.answers_type[0] == "image":
            self.selected_answer = int(self.current_answers[0]["id"])
        elif self.answers_type[0] == "text":
            self.selected_answer = self.ui.btn_a.text()
        self.ui.frame_a.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_b.setStyleSheet(self.default_stylesheet)
        self.ui.frame_c.setStyleSheet(self.default_stylesheet)
        self.ui.frame_d.setStyleSheet(self.default_stylesheet)

    def select_b(self):
        if self.answers_type[1] == "image":
            self.selected_answer = int(self.current_answers[1]["id"])
        elif self.answers_type[1] == "text":
            self.selected_answer = self.ui.btn_b.text()
        self.ui.frame_b.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_a.setStyleSheet(self.default_stylesheet)
        self.ui.frame_c.setStyleSheet(self.default_stylesheet)
        self.ui.frame_d.setStyleSheet(self.default_stylesheet)

    def select_c(self):
        if self.answers_type[2] == "image":
            self.selected_answer = int(self.current_answers[2]["id"])
        elif self.answers_type[2] == "text":
            self.selected_answer = self.ui.btn_c.text()
        self.ui.frame_c.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_a.setStyleSheet(self.default_stylesheet)
        self.ui.frame_b.setStyleSheet(self.default_stylesheet)
        self.ui.frame_d.setStyleSheet(self.default_stylesheet)

    def select_d(self):
        if self.answers_type[3] == "image":
            self.selected_answer = int(self.current_answers[3]["id"])
        elif self.answers_type[3] == "text":
            self.selected_answer = self.ui.btn_d.text()
        self.ui.frame_d.setStyleSheet(self.selected_stylesheet)
        self.ui.frame_a.setStyleSheet(self.default_stylesheet)
        self.ui.frame_b.setStyleSheet(self.default_stylesheet)
        self.ui.frame_c.setStyleSheet(self.default_stylesheet)

    def select_question(self, question: str):
        question_index = (int(question.split()[1]) % 10) - 1

        question_status = self.ui.paginated_question_list[self.ui.page][question_index][
            "is_answered"
        ]

        if question_status:
            return 0

        else:
            self.ui.question_id.setText(
                f"Sorag №{(self.ui.page * 10) + question_index + 1}"
            )

            self.ui.question.setText(
                self.ui.paginated_question_list[self.ui.page][question_index][
                    "question"
                ]
            )

            question_id = self.ui.paginated_question_list[self.ui.page][question_index][
                "id"
            ]

            if self.ui.paginated_question_list[self.ui.page][question_index][
                "is_image"
            ]:
                response = requests.get(
                    f"{api_url}/{self.ui.paginated_question_list[self.ui.page][question_index]['image']}"
                )
                file_name = self.ui.paginated_question_list[self.ui.page][
                    question_index
                ]["image"].split("/")[3]
                with open(f"C:/quizz_cache/{file_name}", "wb") as file:
                    file.write(response.content)
                self.ui.question.setText(f"Suraty görmek üçin sag düwmä basyň")
                self.question_image_path = self.ui.paginated_question_list[
                    self.ui.page
                ][question_index]["image"]
            else:
                self.ui.question.setText(
                    self.ui.paginated_question_list[self.ui.page][question_index][
                        "question"
                    ]
                )

            self.current_answers = requests.request(
                "GET",
                url=f"{api_url}/api/v1/answerfilter/{question_id}/",
                headers={"Authorization": self.token},
            ).json()
            random.shuffle(self.current_answers)

            if len(self.current_answers) == 3:
                self.label_tuple = (self.ui.btn_a, self.ui.btn_b, self.ui.btn_c)
                self.ui.btn_d.setEnabled(False)
                self.ui.btn_d.setHidden(True)
                self.ui.frame_d.setEnabled(False)
                self.ui.frame_d.setHidden(True)
            elif len(self.current_answers) == 4:
                self.label_tuple = (
                    self.ui.btn_a,
                    self.ui.btn_b,
                    self.ui.btn_c,
                    self.ui.btn_d,
                )
                self.ui.btn_d.setEnabled(True)
                self.ui.btn_d.setHidden(False)
                self.ui.frame_d.setEnabled(True)
                self.ui.frame_d.setHidden(False)

            for index in range(len(self.current_answers)):
                if self.current_answers[index]["is_image"]:
                    response = requests.get(
                        f"{api_url}/{self.current_answers[index]['image']}"
                    )
                    file_name = self.current_answers[index]["image"].split("/")[3]
                    with open(f"C:/quizz_cache/{file_name}", "wb") as file:
                        file.write(response.content)
                    self.answers_type[index] = "image"
                    self.label_tuple[index].setText(
                        f"{index + 1}. Suraty görmek üçin sag düwmä basyň"
                    )
                else:
                    self.answers_type[index] = "text"
                    self.label_tuple[index].setText(
                        self.current_answers[index]["answer"]
                    )

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
            if self.ui.paginated_question_list[self.ui.page][i]["is_answered"]:
                self.ui.btns_list[i].setStyleSheet("background-color: #f5f5f5;")
            else:
                self.ui.btns_list[i].setStyleSheet("background-color: #e1e1e1;")
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
            if self.ui.paginated_question_list[self.ui.page][i]["is_answered"]:
                self.ui.btns_list[i].setStyleSheet("background-color: #f5f5f5;")
            else:
                self.ui.btns_list[i].setStyleSheet("background-color: #e1e1e1;")
            self.ui.btns_list[i].setText(f"Sorag {label}")

    def set_text(self, text):
        self.ui.label.setText(text)

    def next_question(self, question: str):
        question_index = (int(question.split("№")[1]) % 10) - 1
        question_id = self.ui.paginated_question_list[self.ui.page][question_index][
            "id"
        ]

        if not self.selected_answer is None:

            self.ui.paginated_question_list[self.ui.page][question_index][
                "is_answered"
            ] = True

            headers = {"Authorization": self.token}

            user = requests.request(
                "GET",
                f"{api_url}/api/v1/auth/users/",
                headers=headers,
            ).json()

            if type(self.selected_answer) == int:
                payload = {
                    "answer": self.selected_answer,
                    "user": user[0]["id"],
                }

                requests.request(
                    "POST",
                    f"{api_url}/api/v1/useranswer_create_by_id/",
                    data=payload,
                    headers=headers,
                )

            elif type(self.selected_answer) == str:
                payload = {
                    "answer": self.selected_answer,
                    "user": user[0]["id"],
                    "question": question_id,
                }

                requests.request(
                    "POST",
                    f"{api_url}/api/v1/useranswer_create/",
                    data=payload,
                    headers=headers,
                )

            self.selected_answer = None

            self.ui.frame_a.setStyleSheet(self.default_stylesheet)
            self.ui.frame_b.setStyleSheet(self.default_stylesheet)
            self.ui.frame_c.setStyleSheet(self.default_stylesheet)
            self.ui.frame_d.setStyleSheet(self.default_stylesheet)

            is_answered = True
            is_finish = False

            while is_answered:
                try:
                    question_index += 1
                    is_answered = self.ui.paginated_question_list[self.ui.page][
                        question_index
                    ]["is_answered"]
                except IndexError:
                    question_index = 0
                    if self.ui.page + 1 == len(self.ui.paginated_question_list):
                        is_finish = True
                        break
                    else:
                        self.ui.page += 1
                        is_answered = self.ui.paginated_question_list[self.ui.page][
                            question_index
                        ]["is_answered"]

            is_destroyed = False

            if is_finish:
                question_index = 0
                is_answered = self.ui.paginated_question_list[self.ui.page][
                    question_index
                ]["is_answered"]

                req_try = 0
                while is_answered:
                    req_try += 1
                    try:
                        for i in range(len(self.ui.paginated_question_list)):
                            for j in range(len(self.ui.paginated_question_list[i])):
                                print("page:" + str(i))
                                print("question:" + str(j))
                                is_answered = self.ui.paginated_question_list[i][j][
                                    "is_answered"
                                ]
                                if is_answered == False:
                                    self.ui.page = i
                                    question_index = j
                                    break
                            if is_answered == False:
                                break

                    except IndexError:
                        question_index = 0
                        if self.ui.page + 1 == len(self.ui.paginated_question_list):
                            self.timer_thread.quit()
                            del self.timer_thread
                            del self.ui

                            end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            headers = {"Authorization": self.token}

                            user = requests.request(
                                "GET",
                                f"{api_url}/api/v1/auth/users/",
                                headers=headers,
                            ).json()

                            test_session_url = f"{api_url}/api/v1/test-session-update/"
                            requests.request(
                                "POST",
                                url=test_session_url,
                                headers=headers,
                                data={
                                    "challenge": int(self.challenge_data[0]["id"]),
                                    "user": int(user[0]["id"]),
                                    "date": end,
                                },
                            ).json()
                            self.create_result_ui()
                            is_destroyed = True
                            break
                        else:
                            self.ui.page += 1
                            is_answered = self.ui.paginated_question_list[self.ui.page][
                                question_index
                            ]["is_answered"]

                    if req_try == len(self.selected_challenge) + 1:
                        question_index = 0
                        if self.ui.page + 1 == len(self.ui.paginated_question_list):
                            self.timer_thread.quit()
                            del self.timer_thread
                            del self.ui

                            end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            headers = {"Authorization": self.token}

                            user = requests.request(
                                "GET",
                                f"{api_url}/api/v1/auth/users/",
                                headers=headers,
                            ).json()

                            test_session_url = f"{api_url}/api/v1/test-session-update/"
                            requests.request(
                                "POST",
                                url=test_session_url,
                                headers=headers,
                                data={
                                    "challenge": int(self.challenge_data[0]["id"]),
                                    "user": int(user[0]["id"]),
                                    "date": end,
                                },
                            ).json()
                            self.create_result_ui()
                            is_destroyed = True
                            break
                        else:
                            self.ui.page += 1
                            is_answered = self.ui.paginated_question_list[self.ui.page][
                                question_index
                            ]["is_answered"]

            if not is_destroyed:

                for btn in self.ui.btns_list:
                    btn.setHidden(False)

                if len(self.ui.paginated_question_list[self.ui.page]) < 10:
                    for btn in self.ui.btns_list[
                        len(self.ui.paginated_question_list[self.ui.page]) : 10
                    ]:
                        btn.setHidden(True)

                for i in range(len(self.ui.paginated_question_list[self.ui.page])):
                    label = (self.ui.page * 10) + (i + 1)
                    if self.ui.paginated_question_list[self.ui.page][i]["is_answered"]:
                        self.ui.btns_list[i].setStyleSheet("background-color: #f5f5f5;")
                    else:
                        self.ui.btns_list[i].setStyleSheet("background-color: #e1e1e1;")
                    self.ui.btns_list[i].setText(f"Sorag {label}")

                self.question_image_path = None

                self.status_bar["answered"] += 1
                self.status_bar["unanswered"] -= 1

                self.ui.answered.setText(
                    f"Jogap berilen: {self.status_bar.get('answered')}"
                )
                self.ui.unanswered.setText(
                    f"Jogap berilmedik: {self.status_bar.get('unanswered')}"
                )

                if self.ui.paginated_question_list[self.ui.page][question_index][
                    "is_image"
                ]:
                    response = requests.get(
                        f"{api_url}/{self.ui.paginated_question_list[self.ui.page][question_index]['image']}"
                    )
                    file_name = self.ui.paginated_question_list[self.ui.page][
                        question_index
                    ]["image"].split("/")[3]
                    with open(f"C:/quizz_cache/{file_name}", "wb") as file:
                        file.write(response.content)
                    self.ui.question.setText(f"Suraty görmek üçin sag düwmä basyň")
                    self.question_image_path = self.ui.paginated_question_list[
                        self.ui.page
                    ][question_index]["image"]
                else:
                    self.ui.question.setText(
                        self.ui.paginated_question_list[self.ui.page][question_index][
                            "question"
                        ]
                    )

                self.question_index = question_index
                question_id = self.ui.paginated_question_list[self.ui.page][
                    question_index
                ]["id"]

                self.current_answers = requests.request(
                    "GET",
                    url=f"{api_url}/api/v1/answerfilter/{question_id}/",
                    headers={"Authorization": self.token},
                ).json()
                random.shuffle(self.current_answers)

                if len(self.current_answers) == 3:
                    self.label_tuple = (self.ui.btn_a, self.ui.btn_b, self.ui.btn_c)
                    self.ui.btn_d.setEnabled(False)
                    self.ui.btn_d.setHidden(True)
                    self.ui.frame_d.setEnabled(False)
                    self.ui.frame_d.setHidden(True)
                elif len(self.current_answers) == 4:
                    self.label_tuple = (
                        self.ui.btn_a,
                        self.ui.btn_b,
                        self.ui.btn_c,
                        self.ui.btn_d,
                    )
                    self.ui.btn_d.setEnabled(True)
                    self.ui.btn_d.setHidden(False)
                    self.ui.frame_d.setEnabled(True)
                    self.ui.frame_d.setHidden(False)

                for index in range(len(self.current_answers)):
                    if self.current_answers[index]["is_image"]:
                        response = requests.get(
                            f"{api_url}/{self.current_answers[index]['image']}"
                        )
                        file_name = self.current_answers[index]["image"].split("/")[3]
                        with open(f"C:/quizz_cache/{file_name}", "wb") as file:
                            file.write(response.content)
                        self.answers_type[index] = "image"
                        self.label_tuple[index].setText(
                            f"{index + 1}. Suraty görmek üçin sag düwmä basyň"
                        )
                    else:
                        self.answers_type[index] = "text"
                        self.label_tuple[index].setText(
                            self.current_answers[index]["answer"]
                        )

                self.ui.question_id.setText(
                    f"Sorag №{(self.ui.page * 10) + question_index + 1}"
                )
        else:
            modal_info_window("Jogap saýlaň")

    def choose_challenge(self, challenge_name):
        del self.table_ui

        for challenge in self.challenge_list:
            if challenge["name"] == challenge_name:
                selected_challenge_id = challenge["id"]

        headers = {"Authorization": self.token}
        test_session_url = f"{api_url}/api/v1/test-session-create/"
        url = f"{api_url}/api/v1/questionfilter/{selected_challenge_id}/"

        user = requests.request(
            "GET",
            f"{api_url}/api/v1/auth/users/",
            headers=headers,
        ).json()

        self.session = requests.request(
            "POST",
            url=test_session_url,
            headers=headers,
            data={"challenge": int(selected_challenge_id), "user": int(user[0]["id"])},
        ).json()

        self.selected_challenge = requests.request(
            "GET", url=url, headers=headers
        ).json()

        challenge_url = f"{api_url}/api/v1/challenge/{selected_challenge_id}/"
        challenge_headers = {"Authorization": self.token}

        self.challenge_data = requests.request(
            "GET", url=challenge_url, headers=challenge_headers
        ).json()

        self.create_main_ui()

        self.time = [self.challenge_data[0]["time_for_event"], 0]
        minute_str = str(self.time[0]) if self.time[0] >= 10 else f"0{self.time[0]}"
        second_str = "00"
        self.time_str = minute_str + ":" + second_str
        self.ui.label.setText(self.time_str)

        self.timer_thread = TimerThread(self.challenge_data[0]["time_for_event"])
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

    def run_timeout(self):
        self.timer_thread.quit()
        del self.timer_thread
        del self.ui
        self.create_result_ui()

    def accept(self):
        name = self.login_ui.name_input.text()
        surname = self.login_ui.surname_input.text()
        about = self.login_ui.about_input.text()

        cyrillic = "ёйцукенгшщзхъфывапролджэячсмитьбю"
        symbols = ".,/\\`'[]()!@#$%^&*№:;{}<>?+=-_" + '"'
        filling_error = False
        for char in name.lower() + surname.lower() + about.lower():
            if char in symbols or char in cyrillic:
                filling_error = True
                break
        if filling_error:
            message = "Girizen maglumatlaryňyzda kabul\nedilmeýän simwollar ulanylypdyr!\nTäzeden synanyşmagyňyzy haýyş\nedýäris!"
            self.login_ui.name_input.setText("")
            self.login_ui.surname_input.setText("")
            self.login_ui.about_input.setText("")
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
            self.auth_request_thread = AuthorizationRequestThread(
                name, surname, about=about
            )
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
            self.login_ui.about_input.setFocus(Qt.FocusReason.ShortcutFocusReason)
        elif e.key() == 16777220 and self.login_ui.about_input.hasFocus():
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
    ok_btn = QPushButton("OK")
    ok_btn.setStyleSheet(btn_stylesheet)
    ok_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    ok_btn.setFont(font)
    vbox.addWidget(label)
    vbox.addWidget(ok_btn, 0, Qt.AlignHCenter | Qt.AlignVCenter)
    ok_btn.clicked.connect(window.run_timeout)
    modal_window.show()


def image_window(pixmap_path: str):
    global image_mod_window
    image_mod_window = QWidget(window)
    image_mod_window.setWindowModality(Qt.WindowModality.WindowModal)
    image_mod_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
    image_mod_window.move(
        window.geometry().center() - image_mod_window.rect().center() - QPoint(75, 120)
    )
    vbox = QVBoxLayout(image_mod_window)
    stylesheet = """
        background-color: white;
        border: 1px solid #7a7a7a;
        border-radius: 20px;
    """
    btn_stylesheet = """
        padding: 10px;
        background-color: #ffffff;
        border-radius: 15px;
    """
    font = QFont()
    font.setPointSize(14)
    image_mod_window.setLayout(vbox)
    image_mod_window.setStyleSheet(stylesheet)
    label = QLabel()
    pixmap = QPixmap(pixmap_path)
    image_mod_window.resize(pixmap.width(), pixmap.height() + 100)
    label.setPixmap(pixmap)
    label.setStyleSheet("border-radius: 0;")
    label.setScaledContents(True)
    label.setFont(font)
    label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    ok_btn = QPushButton("OK")
    ok_btn.setStyleSheet(btn_stylesheet)
    ok_btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
    ok_btn.setFont(font)
    vbox.addWidget(label)
    vbox.addWidget(ok_btn, 0, Qt.AlignHCenter | Qt.AlignBottom)
    ok_btn.clicked.connect(lambda: image_mod_window.close())
    image_mod_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.create_login_ui()
    window.show()

    sys.exit(app.exec_())
