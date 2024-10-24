import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget, QGridLayout, QScrollArea,
                             QStackedWidget)

MAIN_WINDOW_TITLE = "Беларусь История"
LINE_EDIT_MAIN_WINDOW_PLACEHOLDER = "Искать..."

# Путь к папке History и файлу bilety.json
history_folder = "History"
images_folder = os.path.join(history_folder, "Images")
json_file = os.path.join(history_folder, "bilety.json")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget(self)  # Для переключения между страницами
        self.setCentralWidget(self.stack)

        self.initMainPage()  # Главная страница
        self.stack.setCurrentIndex(0)  # Открыть главную страницу по умолчанию

        # Настройки окна
        self.resize(1136, 639)
        self.setWindowTitle(MAIN_WINDOW_TITLE)

    # Создание главного меню с превью билетов
    def initMainPage(self):
        # Главная страница с превью билетов
        mainPage = QWidget()
        mainLayout = QVBoxLayout(mainPage)

        # Поле поиска
        self.leSearch = QLineEdit()
        self.leSearch.setPlaceholderText(LINE_EDIT_MAIN_WINDOW_PLACEHOLDER)
        self.leSearch.setStyleSheet(
            "background-color: darkGray; border: 3px solid black; border-radius: 40px;"
            "font-size: 32px; height: 40px; padding-left: 20px"
        )
        self.leSearch.textChanged.connect(self.filterTickets)

        # Прокручиваемая область для билетов
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.ticket_container = QWidget()
        self.grid = QGridLayout(self.ticket_container)
        self.grid.setSpacing(10)

        # Загрузка билетов из bilety.json
        with open(json_file, 'r', encoding='utf-8') as file:
            self.bilety = json.load(file)

        self.displayTickets(self.bilety)  # Отображаем все билеты

        # Прокручиваемая область для билетов
        self.scroll_area.setWidget(self.ticket_container)

        # Добавление элементов на главную страницу
        mainLayout.addWidget(self.leSearch)
        mainLayout.addWidget(self.scroll_area)

        self.stack.addWidget(mainPage)  # Добавляем главную страницу в стек

    # Фильтрация билетов по тексту поиска
    def filterTickets(self, text):
        filtered_tickets = [ticket for ticket in self.bilety if text.lower() in ticket['Text'].lower()]
        self.displayTickets(filtered_tickets)

    # Отображение билетов в сетке
    def displayTickets(self, tickets):
        # Очищаем текущую сетку
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Создание превью билетов
        for ticket in tickets:
            ticket_number = ticket['Number']
            # Путь к картинке
            image_path = os.path.join(images_folder, f"{ticket_number}.jpeg")

            # Картинка для превью
            lbl_image = QLabel()
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path).scaled(150, 100, Qt.KeepAspectRatio)
            else:
                pixmap = QPixmap(150, 100)  # Заглушка для отсутствующих картинок
                pixmap.fill(Qt.lightGray)
            lbl_image.setPixmap(pixmap)

            # Номер билета
            lbl_number = QLabel(f"Билет {ticket_number}")
            lbl_number.setStyleSheet("font-size: 18px; font-weight: bold;")

            # Вёрстка для каждого билета
            vbox = QVBoxLayout()
            vbox.addWidget(lbl_image)
            vbox.addWidget(lbl_number)

            # Контейнер для билета
            ticket_widget = QWidget()
            ticket_widget.setLayout(vbox)
            ticket_widget.mousePressEvent = lambda event, num=ticket_number: self.openTicketPage(num)

            # Добавляем билет в сетку
            self.grid.addWidget(ticket_widget, (ticket_number - 1) // 3, (ticket_number - 1) % 3)

    # Страница с полной версией билета
    def openTicketPage(self, ticket_number):
        ticketPage = QWidget()
        ticketLayout = QVBoxLayout(ticketPage)

        # Загрузка данных билета
        with open(json_file, 'r', encoding='utf-8') as file:
            bilety = json.load(file)
        ticket = next(item for item in bilety if item['Number'] == ticket_number)
        ticket_text = ticket['Text']

        # Путь к картинке
        image_path = os.path.join(images_folder, f"{ticket_number}.jpeg")

        # Картинка билета
        lbl_image = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(300, 200, Qt.KeepAspectRatio)
        else:
            pixmap = QPixmap(300, 200)  # Заглушка для отсутствующих картинок
            pixmap.fill(Qt.lightGray)
        lbl_image.setPixmap(pixmap)

        # Номер билета
        lbl_number = QLabel(f"Билет {ticket_number}")
        lbl_number.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Текст билета
        lbl_text = QLabel(ticket_text)
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet("font-size: 18px;")

        # Кнопка "Назад"
        btn_back = QPushButton("Назад")
        btn_back.clicked.connect(self.goBackToMain)

        # Добавляем элементы на страницу билета
        ticketLayout.addWidget(lbl_image)
        ticketLayout.addWidget(lbl_number)
        ticketLayout.addWidget(lbl_text)
        ticketLayout.addWidget(btn_back)

        self.stack.addWidget(ticketPage)  # Добавляем страницу билета в стек
        self.stack.setCurrentWidget(ticketPage)  # Переход на страницу билета

    # Возвращение на главную страницу
    def goBackToMain(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
