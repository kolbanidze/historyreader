from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFontDatabase, QIcon, QPixmap
from PyQt5.QtWidgets import *
import json
from datetime import datetime
import os

ICON_MAIN_MENU = "data\\icons\\main_menu.png"
ICON_MAIN_PROFILE = "data\\icons\\main_profile.png"
MAIN_WINDOW_TITLE = "(НАЗВАНИЕ ПРОЕКТА)"
LABEL_BODY_HEADER_TEXT = "Это интересно"
LINE_EDIT_MAIN_WINDOW_PLACEHOLDER = "Искать..."
PUSH_BUTTON_TICKETS_LIST_TEXT = "Список Билетов"


class TicketDetailWindow(QDialog):
    def __init__(self, ticket):
        super().__init__()
        self.setWindowTitle(f"Билет №{ticket['Number']}")
        self.setMinimumSize(400, 300)

        # Создаем разметку для отображения текста билета
        self.layout = QVBoxLayout()

        # Область прокрутки для текста билета
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Разрешаем виджету изменять размеры внутри области прокрутки

        # Текст билета с поддержкой HTML
        ticket_text = ticket['Text']  # Текст билета с тегами
        text_label = QLabel(ticket_text)
        text_label.setOpenExternalLinks(True)  # Для ссылок (если будут)
        text_label.setWordWrap(True)  # Перенос строк
        text_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Выравнивание текста по верхнему краю

        # Добавляем QLabel с текстом билета в виджет прокрутки
        scroll_area.setWidget(text_label)

        # Добавляем область прокрутки в основной макет
        self.layout.addWidget(scroll_area)
        self.setLayout(self.layout)

class TestWindow(QDialog):
    def __init__(self, test_data):
        super().__init__()
        self.setWindowTitle(f"Тест для билета №{test_data['Number']}")
        self.setMinimumSize(600, 400)

        self.test_data = test_data["Test"]
        self.ticket_number = test_data["Number"]
        self.current_question_index = 0
        self.user_answers = []

        # Основная разметка
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Вопрос
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        # Варианты ответов
        self.answer_buttons = []
        self.answers_layout = QVBoxLayout()
        for i in range(4):  # Максимум 4 ответа
            btn = QRadioButton()
            self.answer_buttons.append(btn)
            self.answers_layout.addWidget(btn)
        self.layout.addLayout(self.answers_layout)

        # Кнопки "Далее" и "Завершить"
        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        self.finish_button = QPushButton("Завершить тест")
        self.finish_button.clicked.connect(self.finish_test)
        self.finish_button.setVisible(False)
        self.layout.addWidget(self.finish_button)

        self.show_question(self.current_question_index)

    def show_question(self, index):
        """Отображает текущий вопрос и варианты ответов"""
        question_data = self.test_data[index]
        self.question_label.setText(question_data["Question"])

        # Обновляем текст для кнопок с ответами
        for i, answer_text in enumerate(question_data["Answers"]):
            self.answer_buttons[i].setText(answer_text)
            self.answer_buttons[i].setVisible(True)
            self.answer_buttons[i].setChecked(False)
        # Скрываем неиспользуемые кнопки
        for i in range(len(question_data["Answers"]), len(self.answer_buttons)):
            self.answer_buttons[i].setVisible(False)

        # Если это последний вопрос, показываем кнопку "Завершить"
        self.next_button.setVisible(index < len(self.test_data) - 1)
        self.finish_button.setVisible(index == len(self.test_data) - 1)

    def next_question(self):
        """Переход к следующему вопросу и сохранение ответа"""
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
        # Если ответ не выбран, сохраняем None
        self.user_answers.append(None)

    def finish_test(self):
        """Завершает тест, показывает результаты и сохраняет их в stats.json"""
        self.save_answer()
        correct_answers = sum(1 for user_answer, question_data in zip(self.user_answers, self.test_data)
                              if user_answer == question_data["CorrectAnswer"])

        QMessageBox.information(
            self,
            "Результат теста",
            f"Вы ответили правильно на {correct_answers} из {len(self.test_data)} вопросов."
        )

        # Сохраняем результаты в stats.json
        self.save_test_result(correct_answers, len(self.test_data))
        self.accept()

    def save_test_result(self, correct_answers, total_questions):
        """Сохраняет результат теста в stats.json"""
        result = {
            "Bilet": self.ticket_number,
            "Time": datetime.now().isoformat(),
            "CorrectAnswers": correct_answers,
            "TotalAnswers": total_questions
        }

        # Чтение текущих данных из stats.json
        try:
            with open("stats.json", "r", encoding="utf-8") as f:
                stats_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            stats_data = []

        # Добавление нового результата
        stats_data.append(result)

        # Сохранение обновленных данных
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=4)


class TestMenuWindow(QMainWindow):
    def __init__(self, tickets, parent=None):
        super().__init__(parent)
        self.tickets = tickets
        self.setWindowTitle("Меню тестов")
        self.setMinimumSize(800, 600)

        # Сетка для тестов
        self.gridTests = QGridLayout()
        self.gridTests.setSpacing(10)

        # Создаем основной виджет
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.gridTests)
        self.setCentralWidget(self.centralWidget)

        # Обновляем отображение тестов и добавляем обработчик на изменение размера
        self.update_test_display()
        self.resizeEvent = self.on_resize

    def create_test_widget(self, ticket, image_width):
        test_widget = QWidget()
        test_layout = QVBoxLayout()

        # Загружаем изображение теста
        test_image_path = os.path.join("data", "images", f"ticket_{ticket['Number']}.png")
        test_image = QLabel()
        test_image.setPixmap(QPixmap(test_image_path).scaled(image_width, int(image_width * 0.67), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        test_image.setAlignment(Qt.AlignCenter)
        test_image.setCursor(Qt.PointingHandCursor)

        # Сигнал для открытия теста
        test_image.mousePressEvent = lambda event: self.open_test(ticket)

        # Номер теста
        test_label = QLabel(f"Тест №{ticket['Number']}")
        test_label.setAlignment(Qt.AlignCenter)
        test_label.setProperty("class", "TestLabel")

        # Добавляем в разметку
        test_layout.addWidget(test_image)
        test_layout.addWidget(test_label)
        test_widget.setLayout(test_layout)
        return test_widget

    def open_test(self, ticket):
        """Открытие окна для прохождения теста"""
        test_window = TestWindow(ticket)
        test_window.exec_()

    def update_test_display(self):
        # Очищаем сетку перед добавлением новых тестов
        for i in reversed(range(self.gridTests.count())):
            widget = self.gridTests.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Рассчитываем количество колонок в зависимости от ширины окна
        grid_width = self.centralWidget.width()
        column_count = max(1, grid_width // 200)  # Например, 200 пикселей на колонку
        image_width = (grid_width - 10 * (column_count + 1)) // column_count

        # Обновляем отображение тестов с учетом количества колонок
        for i, ticket in enumerate(self.tickets):
            test_widget = self.create_test_widget(ticket, image_width)
            row = i // column_count
            col = i % column_count
            self.gridTests.addWidget(test_widget, row, col)

    def on_resize(self, event):
        self.update_test_display()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont("data\\fonts\\Evolventa.otf")
        QFontDatabase.addApplicationFont("data\\fonts\\Lumberjack.otf")

        # Загрузка JSON данных
        with open("data\\json\\main.json", "r", encoding="utf-8") as f:
            self.strings = json.loads(f.read())
        with open("data\\json\\bilety.json", "r", encoding="utf-8") as f:
            self.tickets = json.loads(f.read())

        # Основной фон и макет
        self.wBackground = QWidget()
        self.wBackground.setProperty("class", "Background")
        self.vbBackground = QVBoxLayout()
        self.vbBackground.setContentsMargins(0, 0, 0, 0)

        # Header
        self.wHeader = QWidget()
        self.hbHeader = QHBoxLayout()
        self.pbProfile = QPushButton()
        self.pbProfile.setProperty("class", "Profile")
        self.pbProfile.setIcon(QIcon(ICON_MAIN_PROFILE))
        self.pbProfile.setIconSize(QSize(60, 60))
        self.pbMenu = QPushButton()
        self.pbMenu.setProperty("class", "Menu")
        self.pbMenu.setIcon(QIcon(ICON_MAIN_MENU))
        self.pbMenu.setIconSize(QSize(60, 60))
        self.leSearch = QLineEdit()
        self.leSearch.setProperty("class", "Search")
        self.hbHeader.addWidget(self.pbProfile, stretch=1)
        self.hbHeader.addWidget(self.pbMenu, stretch=1)
        self.hbHeader.addWidget(self.leSearch, stretch=8)
        self.wHeader.setLayout(self.hbHeader)

        # Scrollable Body
        self.saBody = QScrollArea()
        self.saBody.setProperty("class", "saBody")
        self.wBody = QWidget()
        self.vbBody = QVBoxLayout()
        self.vbBody.setContentsMargins(0, 0, 0, 0)
        self.lBodyHeader = QLabel(LABEL_BODY_HEADER_TEXT)
        self.lBodyHeader.setProperty("class", "BodyHeader")
        self.vbBody.addWidget(self.lBodyHeader)

        # "Это интересно" секция
        self.wFacts = list()
        self.hbFacts = list()
        self.lFactImages = list()
        self.lFactTexts = list()
        for i in range(3):
            wFact = QWidget()
            if i < 2:
                wFact.setProperty("class", "Fact")
            self.wFacts.append(wFact)

            hbFact = QHBoxLayout()
            lFactImage = QLabel()
            lFactImage.setPixmap(QPixmap(f"data\\images\\fact_{i + 1}.png"))
            lFactImage.setAlignment(Qt.AlignCenter)
            lFactText = QLabel(self.strings.get(f"fact_{i + 1}_text", ""))
            lFactText.setProperty("class", "FactText")
            lFactText.setWordWrap(True)
            if i % 2 == 0:
                hbFact.addWidget(lFactImage, stretch=1)
                hbFact.addWidget(lFactText, stretch=9, alignment=Qt.AlignTop)
            else:
                hbFact.addWidget(lFactText, stretch=9, alignment=Qt.AlignTop)
                hbFact.addWidget(lFactImage, stretch=1)

            wFact.setLayout(hbFact)
            self.vbBody.addWidget(wFact)

        # Сетка билетов
        self.gridTickets = QGridLayout()
        self.gridTickets.setSpacing(10)
        self.update_ticket_display(self.tickets)  # Первоначальное отображение всех билетов

        # Добавление сетки билетов в макет
        self.vbBody.addLayout(self.gridTickets)
        self.wBody.setLayout(self.vbBody)
        self.saBody.setWidgetResizable(True)
        self.saBody.setWidget(self.wBody)

        # Footer Button
        self.pbTicketsList = QPushButton(PUSH_BUTTON_TICKETS_LIST_TEXT)
        self.pbTicketsList.setProperty("class", "TicketsList")

        # Background Layout
        self.vbBackground.addWidget(self.wHeader, stretch=1)
        self.vbBackground.addWidget(self.saBody, stretch=8)
        self.vbBackground.addWidget(self.pbTicketsList, stretch=1)
        self.vbBackground.setSpacing(0)
        self.wBackground.setLayout(self.vbBackground)

        # Main Window Settings
        self.leSearch.setPlaceholderText(LINE_EDIT_MAIN_WINDOW_PLACEHOLDER)
        self.resize(1136, 639)
        self.setMaximumWidth(1136)
        self.setMaximumHeight(639)
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setCentralWidget(self.wBackground)

        # Load Styles
        with open("scripts\\main.css", "r") as f:
            self.setStyleSheet(f.read())

        # Подключение обработчика для строки поиска
        self.leSearch.textChanged.connect(self.filter_tickets)

        # Подключение обработчика для кнопки меню
        self.pbMenu.clicked.connect(self.open_test_menu)

    def create_ticket_widget(self, ticket):
        ticket_widget = QWidget()
        ticket_layout = QVBoxLayout()

        # Load ticket image
        ticket_image_path = os.path.join("data", "images", f"ticket_{ticket['Number']}.png")
        ticket_image = QLabel()
        ticket_image.setPixmap(QPixmap(ticket_image_path).scaled(150, 100, Qt.KeepAspectRatio))
        ticket_image.setAlignment(Qt.AlignCenter)
        ticket_image.setCursor(Qt.PointingHandCursor)  # Указатель при наведении

        # Сигнал для открытия окна с деталями билета
        ticket_image.mousePressEvent = lambda event: self.open_ticket_detail(ticket)

        # Ticket number label
        ticket_label = QLabel(f"Билет №{ticket['Number']}")
        ticket_label.setAlignment(Qt.AlignCenter)
        ticket_label.setProperty("class", "TicketLabel")

        # Add to layout
        ticket_layout.addWidget(ticket_image)
        ticket_layout.addWidget(ticket_label)
        ticket_widget.setLayout(ticket_layout)
        return ticket_widget

    def open_ticket_detail(self, ticket):
        detail_window = TicketDetailWindow(ticket)
        detail_window.exec_()  # Отображение окна как модального

    def update_ticket_display(self, tickets):
        # Очищаем сетку перед добавлением новых билетов
        for i in reversed(range(self.gridTickets.count())):
            widget = self.gridTickets.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Удаляем старые виджеты
        # Обновляем отображение билетов
        for i, ticket in enumerate(tickets):
            ticket_widget = self.create_ticket_widget(ticket)
            row = i // 3
            col = i % 3
            self.gridTickets.addWidget(ticket_widget, row, col)

    def filter_tickets(self, search_text):
        search_text = search_text.lower()  # Приводим текст к нижнему регистру
        filtered_tickets = [ticket for ticket in self.tickets if
                            search_text in ticket['Text'].lower() or search_text in str(ticket['Number'])]
        self.update_ticket_display(filtered_tickets)

    def open_test_menu(self):
        self.testMenuWindow = TestMenuWindow(self.tickets, self)
        self.testMenuWindow.show()  # Открываем окно меню тестов


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
