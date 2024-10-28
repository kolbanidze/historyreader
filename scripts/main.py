from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QPainter, QPixmap, QBrush
from PyQt5.QtWidgets import *
import json
from datetime import datetime
import os

PATH_FONT_EVOLVENTA = "data\\fonts\\Evolventa.otf"
PATH_FONT_LUMBERJACK = "data\\fonts\\Lumberjack.otf"
PATH_ICON_MAIN_MENU = "data\\icons\\main_menu.png"
PATH_ICON_MAIN_PROFILE = "data\\icons\\main_profile.png"
PATH_JSON_HOME = "data\\json\\home.json"
PATH_JSON_TICKETS = "data\\json\\bilety.json"
PATH_STYLESHEET_HOME = "scripts\\style\\home.css"
PATH_STYLESHEET_TICKET = "scripts\\style\\ticket.css"
PATH_STYLESHEET_TICKETS_LIST = "scripts\\style\\tickets_list.css"
PATH_TICKET_IMAGE = "data\\images\\ticket_{}.png"

class TicketDetailWindow(QDialog):
    def __init__(self, ticket):
        super().__init__()
        self.ticket = ticket
        self.setWindowTitle(f"Билет №{ticket['Number']}")
        self.setMinimumSize(400, 300)

        # Главный макет для билета и теста
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Прокручиваемая область для текста билета
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Текст билета
        ticket_text = QLabel(ticket['Text'])
        ticket_text.setOpenExternalLinks(True)
        ticket_text.setWordWrap(True)
        self.scroll_area.setWidget(ticket_text)

        # Кнопка для запуска теста
        self.start_test_button = QPushButton("Начать тест")
        self.start_test_button.clicked.connect(self.start_test)

        # Добавляем прокрутку и кнопку в макет
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.start_test_button)

    def start_test(self):
        # Удаляем виджет с текстом билета и кнопку
        self.scroll_area.deleteLater()
        self.start_test_button.deleteLater()

        # Загружаем тестовые данные
        self.test_data = self.ticket["Test"]
        self.current_question_index = 0
        self.user_answers = []

        # Вопрос и ответы
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.answer_buttons = []
        self.answers_layout = QVBoxLayout()
        for i in range(4):
            btn = QRadioButton()
            self.answer_buttons.append(btn)
            self.answers_layout.addWidget(btn)
        self.layout.addLayout(self.answers_layout)

        # Кнопки "Далее" и "Завершить тест"
        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        self.finish_button = QPushButton("Завершить тест")
        self.finish_button.clicked.connect(self.finish_test)
        self.finish_button.setVisible(False)
        self.layout.addWidget(self.finish_button)

        # Показ первого вопроса
        self.show_question(0)

    def show_question(self, index):
        """Отображает текущий вопрос и варианты ответов"""
        question_data = self.test_data[index]
        self.question_label.setText(question_data["Question"])

        # Обновляем текст кнопок для ответов
        for i, answer_text in enumerate(question_data["Answers"]):
            self.answer_buttons[i].setText(answer_text)
            self.answer_buttons[i].setVisible(True)
            self.answer_buttons[i].setChecked(False)

        # Скрываем неиспользуемые кнопки
        for i in range(len(question_data["Answers"]), len(self.answer_buttons)):
            self.answer_buttons[i].setVisible(False)

        # Показ кнопок навигации
        self.next_button.setVisible(index < len(self.test_data) - 1)
        self.finish_button.setVisible(index == len(self.test_data) - 1)

    def next_question(self):
        """Сохраняет ответ и переходит к следующему вопросу"""
        self.save_answer()
        self.current_question_index += 1
        if self.current_question_index < len(self.test_data):
            self.show_question(self.current_question_index)

    def save_answer(self):
        """Сохраняет выбранный ответ пользователя для текущего вопроса"""
        for btn in self.answer_buttons:
            if btn.isChecked():
                self.user_answers.append(btn.text())
                return
        self.user_answers.append(None)  # Если ответ не выбран

    def finish_test(self):
        """Завершает тест и показывает результаты"""
        self.save_answer()
        correct_answers = sum(
            1 for user_answer, question_data in zip(self.user_answers, self.test_data)
            if user_answer == question_data["CorrectAnswer"]
        )

        QMessageBox.information(
            self, "Результат теста",
            f"Вы ответили правильно на {correct_answers} из {len(self.test_data)} вопросов."
        )

        # Сохраняем результат
        self.save_test_result(correct_answers, len(self.test_data))
        self.accept()

    def save_test_result(self, correct_answers, total_questions):
        """Сохраняет результаты в stats.json"""
        result = {
            "Bilet": self.ticket["Number"],
            "Time": datetime.now().isoformat(),
            "CorrectAnswers": correct_answers,
            "TotalAnswers": total_questions
        }

        try:
            with open("stats.json", "r", encoding="utf-8") as f:
                stats_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            stats_data = []

        stats_data.append(result)
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=4)

# Screen with ticket content
class TicketScreen(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.l_ticket_title = QLabel("1 Билет")

        # Body
        self.sa_body = QScrollArea()
        self.l_ticket_content = QLabel()

        # Footer
        self.pb_test = QPushButton("Тест")

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

    def refresh(self, ticket_index: int):
        ticket = self.tickets[ticket_index]
        self.l_ticket_title.setText(f"{ticket.get("Number")} Билет")
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
        self.s_home = HomeScreen()
        self.s_tickets_list = TicketsListScreen()
        self.s_ticket = TicketScreen()

        # Screens properties
        self.s_home.pb_tickets_list.clicked.connect(self.home_pb_tickets_list_clicked)
        self.s_tickets_list.pb_home.clicked.connect(self.tickets_list_pb_home)
        self.s_tickets_list.w_tickets[0].mousePressEvent = lambda event : self.tickets_list_w_ticket(0)
        self.s_tickets_list.w_tickets[1].mousePressEvent = lambda event: self.tickets_list_w_ticket(1)
        self.s_tickets_list.w_tickets[2].mousePressEvent = lambda event: self.tickets_list_w_ticket(2)
        self.s_tickets_list.w_tickets[3].mousePressEvent = lambda event: self.tickets_list_w_ticket(3)
        self.s_tickets_list.w_tickets[4].mousePressEvent = lambda event: self.tickets_list_w_ticket(4)
        self.s_tickets_list.w_tickets[5].mousePressEvent = lambda event: self.tickets_list_w_ticket(5)
        self.s_tickets_list.w_tickets[6].mousePressEvent = lambda event: self.tickets_list_w_ticket(6)
        self.s_tickets_list.w_tickets[7].mousePressEvent = lambda event: self.tickets_list_w_ticket(7)
        self.s_tickets_list.w_tickets[8].mousePressEvent = lambda event: self.tickets_list_w_ticket(8)
        self.s_tickets_list.w_tickets[9].mousePressEvent = lambda event: self.tickets_list_w_ticket(9)
        self.s_tickets_list.w_tickets[10].mousePressEvent = lambda event: self.tickets_list_w_ticket(10)
        self.s_tickets_list.w_tickets[11].mousePressEvent = lambda event: self.tickets_list_w_ticket(11)
        self.s_tickets_list.w_tickets[12].mousePressEvent = lambda event: self.tickets_list_w_ticket(12)
        self.s_tickets_list.w_tickets[13].mousePressEvent = lambda event: self.tickets_list_w_ticket(13)
        self.s_tickets_list.w_tickets[14].mousePressEvent = lambda event: self.tickets_list_w_ticket(14)
        self.s_tickets_list.w_tickets[15].mousePressEvent = lambda event: self.tickets_list_w_ticket(15)
        self.s_tickets_list.w_tickets[16].mousePressEvent = lambda event: self.tickets_list_w_ticket(16)
        self.s_tickets_list.w_tickets[17].mousePressEvent = lambda event: self.tickets_list_w_ticket(17)
        self.s_tickets_list.w_tickets[18].mousePressEvent = lambda event: self.tickets_list_w_ticket(18)
        self.s_tickets_list.w_tickets[19].mousePressEvent = lambda event: self.tickets_list_w_ticket(19)
        self.s_tickets_list.w_tickets[20].mousePressEvent = lambda event: self.tickets_list_w_ticket(20)
        self.s_tickets_list.w_tickets[21].mousePressEvent = lambda event: self.tickets_list_w_ticket(21)
        self.s_tickets_list.w_tickets[22].mousePressEvent = lambda event: self.tickets_list_w_ticket(22)
        self.s_tickets_list.w_tickets[23].mousePressEvent = lambda event: self.tickets_list_w_ticket(23)
        self.s_tickets_list.w_tickets[24].mousePressEvent = lambda event: self.tickets_list_w_ticket(24)
        self.s_ticket.pb_back.clicked.connect(self.ticket_pb_back)
        self.s_ticket.pb_home.clicked.connect(self.ticket_pb_home)

        # Properties
        self.setWindowTitle(self.s_home.strings["window_title"])
        self.resize(1200, 700)
        self.addWidget(self.s_home)
        self.addWidget(self.s_tickets_list)
        self.addWidget(self.s_ticket)

        self.setCurrentWidget(self.s_home)

    # Move to tickets list screen
    def home_pb_tickets_list_clicked(self):
        self.setCurrentWidget(self.s_tickets_list)

    # Move to ticket list screen
    def ticket_pb_back(self):
        self.setCurrentWidget(self.s_tickets_list)

    # Move to home screen
    def ticket_pb_home(self):
        self.setCurrentWidget(self.s_home)

    # Move to ticket screen
    def tickets_list_w_ticket(self, ticket_index: int):
        self.s_ticket.refresh(ticket_index)
        self.setCurrentWidget(self.s_ticket)

    # Move to home screen
    def tickets_list_pb_home(self):
        self.setCurrentWidget(self.s_home)

if __name__ == "__main__":
    app = QApplication([])
    MainWidget = MainWidget()
    MainWidget.show()
    app.exec()
