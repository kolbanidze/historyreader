from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFontDatabase, QIcon, QPixmap
from PyQt5.QtWidgets import *
import json
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

        # Текст билета с поддержкой HTML
        ticket_text = ticket['Text']  # Текст билета с тегами
        text_label = QLabel(ticket_text)
        text_label.setOpenExternalLinks(True)  # Для ссылок (если будут)
        text_label.setWordWrap(True)  # Перенос строк

        self.layout.addWidget(text_label)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QFontDatabase.addApplicationFont("data\\fonts\\Evolventa.otf")
        QFontDatabase.addApplicationFont("data\\fonts\\Lumberjack.otf")

        # Загрузка JSON данных
        with open("data\\json\\main.json", "r", encoding="utf-8") as f:
            self.strings = json.loads(f.read())
        with open("History/bilety.json", "r", encoding="utf-8") as f:
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

    def create_ticket_widget(self, ticket):
        ticket_widget = QWidget()
        ticket_layout = QVBoxLayout()

        # Load ticket image
        ticket_image_path = os.path.join("History", "Images", f"{ticket['Number']}.jpeg")
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


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
