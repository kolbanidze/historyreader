from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QPainter, QPixmap, QBrush
from PyQt5.QtWidgets import *
import json
from datetime import datetime

PATH_FONT_EVOLVENTA = "data\\fonts\\Evolventa.otf"
PATH_FONT_LUMBERJACK = "data\\fonts\\Lumberjack.otf"
PATH_ICON_MAIN_MENU = "data\\icons\\main_menu.png"
PATH_ICON_MAIN_PROFILE = "data\\icons\\main_profile.png"
PATH_JSON_HOME = "data\\json\\home.json"
PATH_JSON_TICKET = "data\\json\\ticket.json"
PATH_JSON_TICKETS = "data\\json\\bilety.json"
PATH_STYLESHEET_AUTHORISATION = "scripts\\style\\authorisation.css"
PATH_STYLESHEET_HOME = "scripts\\style\\home.css"
PATH_STYLESHEET_PROFILE = "scripts\\style\\profile.css"
PATH_STYLESHEET_TEST = "scripts\\style\\test.css"
PATH_STYLESHEET_TICKET = "scripts\\style\\ticket.css"
PATH_STYLESHEET_TICKETS_LIST = "scripts\\style\\tickets_list.css"
PATH_TICKET_IMAGE = "data\\images\\ticket_{}.png"

class StatisticsDialog(QDialog):
    def __init__(self, correct_count, incorrect_count, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Результаты теста")

        # Устанавливаем макет
        layout = QVBoxLayout()

        # Создаем метки для правильных и неправильных ответов
        self.label_correct = QLabel(f"Правильные ответы: {correct_count}")
        self.label_incorrect = QLabel(f"Неправильные ответы: {incorrect_count}")
        self.label_stats = QLabel(f"Итого: {round(100*correct_count/(correct_count+incorrect_count), 2)}% верных ответов.")

        # Кнопка для закрытия окна
        self.btn_close = QPushButton("Закрыть")
        self.btn_close.clicked.connect(self.accept)  # Закрываем окно при нажатии на кнопку

        # Добавляем элементы в макет
        layout.addWidget(self.label_correct)
        layout.addWidget(self.label_incorrect)
        layout.addWidget(self.label_stats)
        layout.addWidget(self.btn_close)

        # Устанавливаем макет в диалоговое окно
        self.setLayout(layout)


# Screen with profile details
class ProfileScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Background
        self.w_background = QWidget()
        self.vb_background = QVBoxLayout()

        # Header
        self.w_header = QWidget()
        self.vb_header = QVBoxLayout()
        self.pb_back = QPushButton("Back")
        self.l_profile_name = QLabel()
        self.l_profile_score = QLabel()

        # Body
        self.sa_body = QScrollArea()
        self.w_body = QWidget()
        self.g_body = QGridLayout()
        self.w_tests = list()

        # Background layout
        self.vb_background.addWidget(self.w_header, stretch=1)
        self.vb_background.addWidget(self.sa_body, stretch=9)
        self.w_background.setLayout(self.vb_background)

        # Background properties
        self.w_background.setProperty("class", "Background")
        self.vb_background.setContentsMargins(0, 0, 0, 0)
        self.vb_background.setSpacing(0)

        # Header layout
        self.vb_header.addWidget(self.pb_back, alignment=Qt.AlignLeft)
        self.vb_header.addWidget(self.l_profile_name, alignment=Qt.AlignCenter)
        self.vb_header.addWidget(self.l_profile_score, alignment=Qt.AlignLeft)
        self.w_header.setLayout(self.vb_header)

        # Header properties
        self.pb_back.setProperty("class", "HeaderButton")
        self.l_profile_name.setText("1 Профиль")
        self.l_profile_name.setProperty("class", "ProfileName")
        self.l_profile_score.setText("0 баллов")
        self.l_profile_score.setProperty("class", "ProfileScore")

        # Body layout
        self.w_body.setLayout(self.g_body)

        # Body properties
        self.sa_body.setProperty("class", "saBody")
        self.sa_body.setWidgetResizable(True)
        self.sa_body.setWidget(self.w_body)
        for i in range(25):
            # Test
            w_test = QWidget()
            hb_test = QHBoxLayout()
            l_test_number = QLabel()
            l_test_score = QLabel()

            # Test layout
            hb_test.addWidget(l_test_number, alignment=Qt.AlignCenter)
            hb_test.addWidget(l_test_score, alignment=Qt.AlignCenter)
            w_test.setLayout(hb_test)

            # Test properties
            w_test.setProperty("class", "Test")
            self.w_tests.append(w_test)

            # Grid layout
            r = i // 4
            c = i % 4
            self.g_body.addWidget(w_test, r, c)

            # Test properties
            l_test_number.setText(str(i + 1))
            l_test_number.setProperty("class", "TestNumber")
            l_test_score.setText("0%")
            l_test_score.setProperty("class", "TestScore")

        # Stylesheet
        with open(PATH_STYLESHEET_PROFILE, "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(self.w_background)

# Screen with profiles list
class AuthorisationScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Background
        self.w_background = QWidget()
        self.vb_background = QVBoxLayout()

        # Header
        self.l_header = QLabel()

        # Body
        self.w_body = QWidget()
        self.vb_body = QVBoxLayout()
        self.pb_profiles = list()

        # Background layout
        self.vb_background.addWidget(self.l_header, stretch=1, alignment=Qt.AlignCenter)
        self.vb_background.addWidget(self.w_body, stretch=9, alignment=Qt.AlignCenter)
        self.w_background.setLayout(self.vb_background)

        # Background properties
        self.w_background.setProperty("class", "Background")
        self.vb_background.setContentsMargins(0, 0, 0, 0)
        self.vb_background.setSpacing(0)

        # Header properties
        self.l_header.setProperty("class", "Header")
        self.l_header.setText("Виртуальный билетник")

        # Body layout
        self.w_body.setLayout(self.vb_body)

        # Body properties
        for i in range(3):
            pb_profile = QPushButton()
            self.pb_profiles.append(pb_profile)

            pb_profile.setProperty("class", "Profile")
            pb_profile.setText(f"{i + 1} Профиль")

        for pb in self.pb_profiles:
            self.vb_body.addWidget(pb)

            # Stylesheet
            with open(PATH_STYLESHEET_AUTHORISATION, "r") as f:
                self.setStyleSheet(f.read())

        self.setCentralWidget(self.w_background)

# Widget with test question
class QuestionWidget(QWidget):
    def __init__(self, ticket):
        super().__init__()
        self.ticket = ticket
        # Body
        self.vb_body = QVBoxLayout()
        self.l_label = QLabel()
        self.rb_options = list()

        # Body layout
        self.vb_body.addWidget(self.l_label)
        for i in ticket["Answers"]:
            rb_option = QRadioButton()
            self.rb_options.append(rb_option)

            rb_option.setText(i)
            self.vb_body.addWidget(rb_option)
        self.setLayout(self.vb_body)

        self.l_label.setText(ticket["Question"])

    def get_answer(self):
        for i in self.rb_options:
            if i.isChecked():
                return i.text()

# Screen with test
class TestScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ticket_index = None

        # JSON
        self.tickets = list()
        with open(PATH_JSON_TICKETS, "r", encoding="utf-8") as f:
            self.tickets = json.loads(f.read())

        # Background
        self.w_background = QWidget()
        self.vb_background = QVBoxLayout()

        # Header
        self.w_header = QWidget()
        self.w_header_top = QWidget()
        self.vb_header = QVBoxLayout()
        self.hb_header_top = QHBoxLayout()
        self.pb_back = QPushButton("Back")
        self.pb_home = QPushButton("Home")
        self.l_ticket_title = QLabel()

        # Body
        self.sa_body = QScrollArea()
        self.w_body = QWidget()
        self.vb_body = QVBoxLayout()
        self.w_questions = list()

        # Background layout
        self.vb_background.addWidget(self.w_header)
        self.vb_background.addWidget(self.sa_body)
        self.w_background.setLayout(self.vb_background)

        # Background properties
        self.w_background.setProperty("class", "Background")
        self.vb_background.setContentsMargins(0, 0, 0, 0)
        self.vb_background.setSpacing(0)

        # Header layout
        self.vb_header.addWidget(self.w_header_top)
        self.vb_header.addWidget(self.l_ticket_title, alignment=Qt.AlignCenter)
        self.w_header.setLayout(self.vb_header)
        self.hb_header_top.addWidget(self.pb_back, alignment=Qt.AlignLeft)
        self.hb_header_top.addWidget(self.pb_home, alignment=Qt.AlignRight)
        self.w_header_top.setLayout(self.hb_header_top)

        # Header properties
        self.vb_header.setContentsMargins(0, 0, 0, 0)
        self.vb_header.setSpacing(0)
        self.pb_back.setProperty("class", "HeaderButton")
        self.pb_home.setProperty("class", "HeaderButton")
        self.l_ticket_title.setProperty("class", "TicketTitle")

        # Body properties
        self.sa_body.setProperty("class", "saBody")
        self.sa_body.setWidgetResizable(True)
        self.sa_body.setWidget(self.w_body)

        # Check Button
        self.pb_check = QPushButton("Проверить тест")  # Кнопка для проверки теста
        self.pb_check.clicked.connect(self.check_test)  # Связываем сигнал с методом проверки

        # Stylesheet
        with open(PATH_STYLESHEET_TEST, "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(self.w_background)

    def set_ticket_index(self, ticket_index):
        self.ticket_index = ticket_index
        self.ticket = self.tickets[self.ticket_index]

        for question in self.w_questions:
            self.vb_body.removeWidget(question)
            question.deleteLater()  # Удаляем виджет, чтобы освободить память
        self.w_questions.clear()  # Очищаем список вопросов

        # Body layout
        for i in self.ticket["Test"]:
            w_question = QuestionWidget(i)
            self.w_questions.append(w_question)

            self.vb_body.addWidget(w_question)
        self.w_body.setLayout(self.vb_body)
        self.vb_body.addWidget(self.pb_check)

    def check_test(self):
        correct_answers = 0
        incorrect_answers = 0
        total_answers = len(self.ticket["Test"])
        answers = []
        for i in self.w_questions:
            answers.append(i.get_answer())
        for i in range(total_answers):
            if answers[i] == self.ticket["Test"][i]["CorrectAnswer"]:
                correct_answers += 1
            else:
                incorrect_answers += 1
        # print(f"Правильных ответов: {correct_answers}\nНеправильных ответов: {incorrect_answers}\nИтого: {100*correct_answers/total_answers}%.")
        StatisticsDialog(correct_answers, incorrect_answers, self).exec_()

# Screen with ticket content
class TicketScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # JSON
        self.strings = dict()
        self.tickets = list()
        with open(PATH_JSON_TICKET, "r", encoding="utf-8") as f:
            self.strings = json.loads(f.read())
        with open(PATH_JSON_TICKETS, "r", encoding="utf-8") as f:
            self.tickets = json.loads(f.read())

        # Background
        self.w_background = QWidget()
        self.vb_background = QVBoxLayout()

        # Header
        self.w_header = QWidget()
        self.w_header_top = QWidget()
        self.vb_header = QVBoxLayout()
        self.hb_header_top = QHBoxLayout()
        self.pb_back = QPushButton("Back")
        self.pb_home = QPushButton("Home")
        self.l_ticket_title = QLabel()

        # Body
        self.sa_body = QScrollArea()
        self.l_ticket_content = QLabel()

        # Footer
        self.pb_test = QPushButton(self.strings["test"])

        # Background layout
        self.vb_background.addWidget(self.w_header)
        self.vb_background.addWidget(self.sa_body)
        self.vb_background.addWidget(self.pb_test)
        self.w_background.setLayout(self.vb_background)

        # Background properties
        self.w_background.setProperty("class", "Background")
        self.vb_background.setContentsMargins(0, 0, 0, 0)
        self.vb_background.setSpacing(0)

        # Header layout
        self.vb_header.addWidget(self.w_header_top)
        self.vb_header.addWidget(self.l_ticket_title, alignment=Qt.AlignCenter)
        self.w_header.setLayout(self.vb_header)
        self.hb_header_top.addWidget(self.pb_back, alignment=Qt.AlignLeft)
        self.hb_header_top.addWidget(self.pb_home, alignment=Qt.AlignRight)
        self.w_header_top.setLayout(self.hb_header_top)

        # Header properties
        self.vb_header.setContentsMargins(0, 0, 0, 0)
        self.vb_header.setSpacing(0)
        self.pb_back.setProperty("class", "HeaderButton")
        self.pb_home.setProperty("class", "HeaderButton")
        self.l_ticket_title.setProperty("class", "TicketTitle")

        # Body properties
        self.sa_body.setProperty("class", "saBody")
        self.sa_body.setWidgetResizable(True)
        self.sa_body.setWidget(self.l_ticket_content)
        self.l_ticket_content.setWordWrap(True)

        # Footer properties
        self.pb_test.setProperty("class", "FooterButton")

        # Stylesheet
        with open(PATH_STYLESHEET_TICKET, "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(self.w_background)

    def refresh(self):
        ticket = self.tickets[self.ticket_index]
        self.l_ticket_title.setText(self.strings["ticket_title"].format(ticket.get("Number")))
        self.l_ticket_content.setText(ticket.get("Text"))

# Screen with tickets list
class TicketsListScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Background
        self.w_background = QWidget()
        self.vb_background = QVBoxLayout()

        # Header
        self.w_header = QWidget()
        self.hb_header = QHBoxLayout()
        self.pb_profile = QPushButton()
        self.pb_home = QPushButton("Home")

        # Body
        self.sa_body = QScrollArea()
        self.w_body = QWidget()
        self.g_body = QGridLayout()
        self.w_tickets = list()

        # Background layout
        self.vb_background.addWidget(self.w_header, stretch=1)
        self.vb_background.addWidget(self.sa_body, stretch=9)
        self.w_background.setLayout(self.vb_background)

        # Background properties
        self.w_background.setProperty("class", "Background")
        self.vb_background.setContentsMargins(0, 0, 0, 0)
        self.vb_background.setSpacing(0)

        # Header layout
        self.hb_header.addWidget(self.pb_profile, alignment=Qt.AlignLeft)
        self.hb_header.addWidget(self.pb_home, alignment=Qt.AlignRight)
        self.w_header.setLayout(self.hb_header)

        # Header properties
        self.pb_profile.setProperty("class", "HeaderButton")
        self.pb_profile.setIcon(QIcon(PATH_ICON_MAIN_PROFILE))
        self.pb_profile.setIconSize(QSize(60, 60))
        self.pb_home.setProperty("class", "HeaderButton")

        # Body layout
        self.w_body.setLayout(self.g_body)

        # Body properties
        self.sa_body.setProperty("class", "saBody")
        self.sa_body.setWidgetResizable(True)
        self.sa_body.setWidget(self.w_body)
        for i in range(25):
            # Ticket
            w_ticket = QWidget()
            hb_ticket = QHBoxLayout()
            l_ticket_image = QLabel()
            l_ticket_number = QLabel()

            # Ticket layout
            hb_ticket.addWidget(l_ticket_number, alignment=Qt.AlignCenter)
            hb_ticket.addWidget(l_ticket_image, alignment=Qt.AlignRight)
            w_ticket.setLayout(hb_ticket)

            # Ticket properties
            self.w_tickets.append(w_ticket)

            # Grid layout
            r = i // 4
            c = i % 4
            self.g_body.addWidget(w_ticket, r, c)

            # Round image
            pm_image = QPixmap(PATH_TICKET_IMAGE.format(i + 1)).scaled(200, 150)
            rad = 40
            pm_rounded = QPixmap(pm_image.size())
            pm_rounded.fill(QColor("transparent"))
            p = QPainter(pm_rounded)
            p.setRenderHint(QPainter.Antialiasing)
            p.setBrush(QBrush(pm_image))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(pm_image.rect(), rad, rad)
            p.end()

            # Ticket properties
            l_ticket_image.setPixmap(pm_rounded)
            l_ticket_image.setProperty("class", "TicketImage")
            w_ticket.setProperty("class", "Ticket")
            l_ticket_number.setText(str(i + 1))
            l_ticket_number.setProperty("class", "TicketNumber")

        # Stylesheet
        with open(PATH_STYLESHEET_TICKETS_LIST, "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(self.w_background)

# Screen with interesting facts
class HomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        # JSON
        self.strings = dict()
        with open(PATH_JSON_HOME, "r", encoding="utf-8") as f:
            self.strings = json.loads(f.read())

        # Background
        self.w_background = QWidget(parent=self)
        self.vb_background = QVBoxLayout()

        # Header
        self.w_header = QWidget()
        self.hb_header = QHBoxLayout()
        self.pb_menu = QPushButton()
        self.pb_profile = QPushButton()
        self.le_search = QLineEdit()

        # Body
        self.sa_body = QScrollArea()
        self.l_body_header = QLabel(self.strings["this_is_interesting"])
        self.w_body = QWidget()
        self.vb_body = QVBoxLayout()

        # Facts
        self.w_facts = list()

        # Footer
        self.pb_tickets_list = QPushButton(self.strings["tickets_list"])

        # Background layout
        self.vb_background.addWidget(self.w_header, stretch=1)
        self.vb_background.addWidget(self.sa_body, stretch=8)
        self.vb_background.addWidget(self.pb_tickets_list, stretch=1)
        self.w_background.setLayout(self.vb_background)

        # Background properties
        self.w_background.setProperty("class", "Background")
        self.vb_background.setContentsMargins(0, 0, 0, 0)
        self.vb_background.setSpacing(0)

        # Header layout
        self.hb_header.addWidget(self.pb_profile, stretch=1)
        self.hb_header.addWidget(self.le_search, stretch=8)
        self.hb_header.addWidget(self.pb_menu, stretch=1)
        self.w_header.setLayout(self.hb_header)

        # Header properties
        self.pb_profile.setProperty("class", "HeaderButton")
        self.pb_profile.setIcon(QIcon(PATH_ICON_MAIN_PROFILE))
        self.pb_profile.setIconSize(QSize(60, 60))
        self.pb_menu.setProperty("class", "HeaderButton")
        self.pb_menu.setIcon(QIcon(PATH_ICON_MAIN_MENU))
        self.pb_menu.setIconSize(QSize(60, 60))
        self.le_search.setProperty("class", "Search")
        self.le_search.setPlaceholderText(self.strings["search"])

        # Body layout
        self.vb_body.addWidget(self.l_body_header)
        for i in range(3):
            w_fact = QWidget()
            if i < 2:
                w_fact.setProperty("class", "Fact")
            self.w_facts.append(w_fact)

            hb_fact = QHBoxLayout()
            l_fact_image = QLabel()
            l_fact_image.setPixmap(QPixmap(f"data\\images\\fact_{i + 1}.png"))
            l_fact_image.setAlignment(Qt.AlignCenter)
            l_fact_text = QLabel(self.strings.get(f"fact_{i + 1}_text", ""))
            l_fact_text.setProperty("class", "FactText")
            l_fact_text.setWordWrap(True)
            if i % 2 == 0:
                hb_fact.addWidget(l_fact_image, stretch=1)
                hb_fact.addWidget(l_fact_text, stretch=9, alignment=Qt.AlignTop)
            else:
                hb_fact.addWidget(l_fact_text, stretch=9, alignment=Qt.AlignTop)
                hb_fact.addWidget(l_fact_image, stretch=1)

            w_fact.setLayout(hb_fact)
            self.vb_body.addWidget(w_fact)
        self.w_body.setLayout(self.vb_body)

        # Body properties
        self.w_body.setProperty("class", "wBody")
        self.l_body_header.setProperty("class", "BodyHeader")
        self.sa_body.setProperty("class", "saBody")
        self.sa_body.setWidgetResizable(True)
        self.sa_body.setWidget(self.w_body)
        self.vb_body.setContentsMargins(0, 0, 0, 0)

        # Footer Properties
        self.pb_tickets_list.setProperty("class", "TicketsList")

        # Stylesheet
        with open(PATH_STYLESHEET_HOME, "r") as f:
            self.setStyleSheet(f.read())

        self.setCentralWidget(self.w_background)

class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Load fonts
        QFontDatabase.addApplicationFont(PATH_FONT_EVOLVENTA)
        QFontDatabase.addApplicationFont(PATH_FONT_LUMBERJACK)

        # Screens
        self.s_authorisation = AuthorisationScreen()
        self.s_home = HomeScreen()
        self.s_profile = ProfileScreen()
        self.s_tickets_list = TicketsListScreen()
        self.s_ticket = TicketScreen()
        self.s_test = TestScreen()

        # Screens properties
        for pb in self.s_authorisation.pb_profiles:
            pb.clicked.connect(self.authorisation_profile)
        self.s_home.pb_tickets_list.clicked.connect(self.home_pb_tickets_list)
        self.s_home.pb_profile.clicked.connect(self.home_pb_profile)
        self.s_profile.pb_back.clicked.connect(self.profile_pb_back)
        self.s_tickets_list.pb_home.clicked.connect(self.tickets_list_pb_home)

        for i in range(25):
            self.s_tickets_list.w_tickets[i].mousePressEvent = lambda event, index=i: self.tickets_list_w_ticket(index)

        self.s_ticket.pb_back.clicked.connect(self.ticket_pb_back)
        self.s_ticket.pb_home.clicked.connect(self.ticket_pb_home)
        self.s_ticket.pb_test.clicked.connect(self.ticket_pb_test)
        self.s_test.pb_back.clicked.connect(self.test_pb_back)

        # Properties
        self.setWindowTitle(self.s_home.strings["window_title"])
        self.resize(1200, 700)
        self.addWidget(self.s_authorisation)
        self.addWidget(self.s_home)
        self.addWidget(self.s_profile)
        self.addWidget(self.s_tickets_list)
        self.addWidget(self.s_ticket)
        self.addWidget(self.s_test)

        self.setCurrentWidget(self.s_authorisation)

    # Select profile
    def authorisation_profile(self):
        self.setCurrentWidget(self.s_home)

    # Move to tickets list screen
    def home_pb_tickets_list(self):
        self.setCurrentWidget(self.s_tickets_list)

    # Move to profile screen
    def home_pb_profile(self):
        self.setCurrentWidget(self.s_profile)

    # Move to home screen
    def profile_pb_back(self):
        self.setCurrentWidget(self.s_home)

    # Move to ticket list screen
    def ticket_pb_back(self):
        self.setCurrentWidget(self.s_tickets_list)

    # Move to home screen
    def ticket_pb_home(self):
        self.setCurrentWidget(self.s_home)

    # Move to test screen
    def ticket_pb_test(self):
        # Переход на экран теста с передачей индекса билета
        ticket_index = self.s_ticket.ticket_index  # Получаем индекс билета
        self.s_test.set_ticket_index(ticket_index)  # Устанавливаем индекс в s_test
        self.setCurrentWidget(self.s_test)  # Переходим на экран теста

    # Move to ticket screen
    def tickets_list_w_ticket(self, ticket_index: int):
        self.s_ticket.ticket_index = ticket_index
        self.s_ticket.refresh()
        self.setCurrentWidget(self.s_ticket)

    # Move to home screen
    def tickets_list_pb_home(self):
        self.setCurrentWidget(self.s_home)

    # Move to ticket screen
    def test_pb_back(self):
        self.setCurrentWidget(self.s_ticket)

if __name__ == "__main__":
    app = QApplication([])
    MainWidget = MainWidget()
    MainWidget.show()
    app.exec()
