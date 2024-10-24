import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QDockWidget, QVBoxLayout, QLabel, QMainWindow,
                             QPushButton, QScrollArea, QStackedWidget, QListWidget,
                             QButtonGroup, QRadioButton, QMessageBox, QWidget, QGridLayout)

MAIN_WINDOW_TITLE = "Беларусь История"
LINE_EDIT_MAIN_WINDOW_PLACEHOLDER = "Искать..."

# TODO: вернуть поиск, продумать статистику, изменить дизайн

history_folder = "History"
images_folder = os.path.join(history_folder, "Images")
json_file = os.path.join(history_folder, "bilety.json")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.resize(1136, 639)

        self.createSideMenu()

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.initMainPage()
        self.stack.setCurrentIndex(0)

    def createSideMenu(self):
        self.dock = QDockWidget("Меню", self)
        self.dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)

        self.list_widget = QListWidget()
        self.list_widget.addItems(["Билеты", "Тесты"])
        self.list_widget.currentItemChanged.connect(self.changePage)

        menu_layout.addWidget(self.list_widget)
        menu_widget.setLayout(menu_layout)

        self.dock.setWidget(menu_widget)

    def changePage(self, current, previous):
        if current:
            if current.text() == "Билеты":
                self.stack.setCurrentIndex(0)
            elif current.text() == "Тесты":
                self.initTestsPage()
                self.stack.setCurrentIndex(1)

    def initMainPage(self):
        mainPage = QWidget()
        mainLayout = QVBoxLayout(mainPage)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.ticket_container = QWidget()
        self.grid = QGridLayout(self.ticket_container)
        self.grid.setSpacing(10)

        with open(json_file, 'r', encoding='utf-8') as file:
            self.bilety = json.load(file)

        self.displayTickets(self.bilety, is_test=False)

        self.scroll_area.setWidget(self.ticket_container)

        mainLayout.addWidget(self.scroll_area)
        self.stack.addWidget(mainPage)

    def initTestsPage(self):
        testsPage = QWidget()
        testsLayout = QVBoxLayout(testsPage)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.test_container = QWidget()
        self.grid = QGridLayout(self.test_container)
        self.grid.setSpacing(10)

        with open(json_file, 'r', encoding='utf-8') as file:
            self.bilety = json.load(file)

        self.displayTickets(self.bilety, is_test=True)

        self.scroll_area.setWidget(self.test_container)
        testsLayout.addWidget(self.scroll_area)

        self.stack.addWidget(testsPage)

    def displayTickets(self, tickets, is_test=False):
        # Очистка текущих элементов сетки
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for ticket in tickets:
            ticket_number = ticket['Number']
            image_path = os.path.join(images_folder, f"{ticket_number}.jpeg")

            lbl_image = QLabel()
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path).scaled(150, 100, Qt.KeepAspectRatio)
            else:
                pixmap = QPixmap(150, 100)
                pixmap.fill(Qt.lightGray)
            lbl_image.setPixmap(pixmap)

            lbl_number = QLabel(f"Билет {ticket_number}")
            lbl_number.setStyleSheet("font-size: 18px; font-weight: bold;")

            vbox = QVBoxLayout()
            vbox.addWidget(lbl_image)
            vbox.addWidget(lbl_number)

            ticket_widget = QWidget()
            ticket_widget.setLayout(vbox)

            if is_test:
                # Если мы в разделе тестов, то по клику откроется тест
                ticket_widget.mousePressEvent = lambda event, num=ticket_number: self.startTest(num)
            else:
                # Если в разделе билетов, то откроется просмотр темы
                ticket_widget.mousePressEvent = lambda event, num=ticket_number: self.openTicketPage(num)

            self.grid.addWidget(ticket_widget, (ticket_number - 1) // 3, (ticket_number - 1) % 3)

    def openTicketPage(self, ticket_number):
        ticketPage = QWidget()
        ticketLayout = QVBoxLayout(ticketPage)

        with open(json_file, 'r', encoding='utf-8') as file:
            bilety = json.load(file)
        ticket = next(item for item in bilety if item['Number'] == ticket_number)

        image_path = os.path.join(images_folder, f"{ticket_number}.jpeg")

        lbl_image = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
        else:
            pixmap = QPixmap(300, 200)
            pixmap.fill(Qt.lightGray)
        lbl_image.setPixmap(pixmap)

        lbl_number = QLabel(f"Билет {ticket_number}")
        lbl_number.setStyleSheet("font-size: 24px; font-weight: bold;")

        lbl_text = QLabel(ticket['Text'])
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet("font-size: 18px;")

        btn_back = QPushButton("Назад")
        btn_back.clicked.connect(self.goBackToMain)

        ticketLayout.addWidget(lbl_image)
        ticketLayout.addWidget(lbl_number)
        ticketLayout.addWidget(lbl_text)
        ticketLayout.addWidget(btn_back)

        self.stack.addWidget(ticketPage)
        self.stack.setCurrentWidget(ticketPage)

    def startTest(self, ticket_number):
        testPage = QWidget()
        testLayout = QVBoxLayout(testPage)

        with open(json_file, 'r', encoding='utf-8') as file:
            bilety = json.load(file)
        ticket = next(item for item in bilety if item['Number'] == ticket_number)

        lbl_number = QLabel(f"Тест по билету {ticket_number}")
        lbl_number.setStyleSheet("font-size: 24px; font-weight: bold;")
        testLayout.addWidget(lbl_number)

        self.answer_groups = []

        for i, question in enumerate(ticket['Test']):
            lbl_question = QLabel(f"{i + 1}. {question['Question']}")
            lbl_question.setStyleSheet("font-size: 18px;")
            testLayout.addWidget(lbl_question)

            btn_group = QButtonGroup(testPage)
            for answer in question['Answers']:
                radio_btn = QRadioButton(answer)
                btn_group.addButton(radio_btn)
                testLayout.addWidget(radio_btn)

            self.answer_groups.append((btn_group, question['CorrectAnswer']))

        btn_submit = QPushButton("Завершить тест")
        btn_submit.clicked.connect(self.submitTest)
        testLayout.addWidget(btn_submit)

        self.stack.addWidget(testPage)
        self.stack.setCurrentWidget(testPage)

    def submitTest(self):
        correct_answers = 0
        total_questions = len(self.answer_groups)
        wrong_answers = []

        for btn_group, correct_answer in self.answer_groups:
            selected_btn = btn_group.checkedButton()
            if selected_btn and selected_btn.text() == correct_answer:
                correct_answers += 1
            else:
                wrong_answers.append(correct_answer)

        result_msg = QMessageBox()
        result_msg.setWindowTitle("Результат теста")

        if wrong_answers:
            incorrect_info = "\n".join([f"Правильный ответ: {answer}" for answer in wrong_answers])
            result_msg.setText(f"Вы правильно ответили на {correct_answers} из {total_questions} вопросов.\n\nНеверные ответы:\n{incorrect_info}")
        else:
            result_msg.setText(f"Все ответы правильные! Вы ответили верно на {correct_answers} из {total_questions} вопросов.")

        result_msg.exec()
        self.goBackToMain()

    def goBackToMain(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
