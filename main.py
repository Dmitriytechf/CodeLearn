import sys
import random
import json

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QLabel, QPushButton, QHBoxLayout, QProgressBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from background import BackgroundWidget
from styles import (BUTTON_STYLE, TEXT_STYLE, BUTTON_HEIGHT,
                    BUTTON_WIDTH, DEFINITION_STYLE, RANDOM_BUTTON_SIZE,
                    RANDOM_BUTTON_STYLE, PROGRESS_BAR_STYLE)


class CodeLearnApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CodeLearn - ваш помощник в программировании')
        # Положение окна: setGeometry(x, y, ширина, высота)
        self.setGeometry(550, 70, 700, 900)

        # Загружаем карточки
        self.cards = self.load_cards()
        self.learned = set()           # id изученных карточек
        self.current_card = None       # текущая карточка

        # Центральный виджет
        central_widget = BackgroundWidget('img/fon3.jpg', self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)  # Отступы от краев
        

        # Метка для термина
        self.term_label = QLabel('Начнем обучение?')
        self.term_label.setAlignment(Qt.AlignCenter)
        self.term_label.setFont(QFont('Calibri', 24, QFont.Bold))
        self.term_label.setStyleSheet(TEXT_STYLE)
        layout.addWidget(self.term_label)

        # Метка для определения
        self.def_label = QLabel('')   # пока пустая
        self.def_label.setAlignment(Qt.AlignCenter)
        self.def_label.setFont(QFont('Calibri', 18))
        self.def_label.setWordWrap(True)  # перенос длинных строк
        self.def_label.hide()  # не показываем термин до нажатия кнопки
        self.def_label.setStyleSheet(DEFINITION_STYLE)
        layout.addWidget(self.def_label, alignment=Qt.AlignCenter)
        
        #Основные кнопки
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        button_font = QFont('Arial', 14, QFont.Bold)

        self.show_def_btn = QPushButton('Показать определение')
        self.show_def_btn.clicked.connect(self.show_definition)
        self.show_def_btn.setFont(button_font)
        self.show_def_btn.setFixedHeight(BUTTON_HEIGHT)
        self.show_def_btn.setFixedWidth(BUTTON_WIDTH)
        self.show_def_btn.setStyleSheet(BUTTON_STYLE)
        btn_layout.addWidget(self.show_def_btn)

        self.know_btn = QPushButton('Знаю')
        self.know_btn.clicked.connect(self.mark_known)
        self.know_btn.setFont(button_font)
        self.know_btn.setFixedHeight(BUTTON_HEIGHT)
        self.know_btn.setFixedWidth(BUTTON_WIDTH)
        self.know_btn.setStyleSheet(BUTTON_STYLE)
        btn_layout.addWidget(self.know_btn)

        self.dont_know_btn = QPushButton('Не знаю')
        self.dont_know_btn.clicked.connect(self.next_card)
        self.dont_know_btn.setFont(button_font)
        self.dont_know_btn.setFixedHeight(BUTTON_HEIGHT)
        self.dont_know_btn.setFixedWidth(BUTTON_WIDTH)
        self.dont_know_btn.setStyleSheet(BUTTON_STYLE)
        btn_layout.addWidget(self.dont_know_btn)

        self.restart_btn = QPushButton('Давай повторим!')
        self.restart_btn.clicked.connect(self.restart_game)
        self.restart_btn.setFont(button_font)
        self.restart_btn.setFixedHeight(BUTTON_HEIGHT)
        self.restart_btn.setFixedWidth(BUTTON_WIDTH)
        self.restart_btn.setStyleSheet(BUTTON_STYLE)
        self.restart_btn.hide()  # Скрываем, пока не закончим игру
        btn_layout.addWidget(self.restart_btn)
        
        layout.addLayout(btn_layout)

        # Счетчик прогресса
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)
        self.progress_bar.setFixedHeight(27)
        self.progress_bar.setFixedWidth(500)
        self.progress_bar.setRange(0, len(self.cards))
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat(f'Изучено: 0 из {len(self.cards)}')
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Создаем горизонтальный layout для нижней части
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 30, 10)
        bottom_layout.setSpacing(10)
        # Добавляем растяжение слева
        bottom_layout.addStretch()

        # Случайный термин
        self.random_btn = QPushButton('?')
        self.random_btn.setFixedSize(RANDOM_BUTTON_SIZE, RANDOM_BUTTON_SIZE)
        self.random_btn.setFont(QFont('Calibri', 30, QFont.Bold))
        self.random_btn.setStyleSheet(RANDOM_BUTTON_STYLE)
        self.random_btn.clicked.connect(self.show_random_term)
        self.random_btn.setToolTip('Случайный термин')
        bottom_layout.addWidget(self.random_btn)

        layout.addLayout(bottom_layout)

        # Показываем первую карточку
        self.next_card()

    def load_cards(self):
        '''Загружаем карточки из Json (сейчас это terms.json)'''
        with open('terms.json', 'r', encoding='utf-8') as f:
            cards = json.load(f)
        return cards

    def next_card(self):
        '''Следующая не изученная карточка'''
        # Определяем доступные карточки (не изученные)
        available = [c for c in self.cards if c['id'] not in self.learned]
        # Если все изучили
        if not available:
            self.term_label.setText('Поздравляем!\nВы изучили все термины!')
            self.show_def_btn.hide()
            self.know_btn.hide()
            self.dont_know_btn.hide()
            self.restart_btn.show()
            self.update_progress()
            return

        self.show_def_btn.show()
        self.know_btn.show()
        self.dont_know_btn.show()
        self.restart_btn.hide()

        self.current_card = random.choice(available)
        self.term_label.setText(self.current_card['term'])
        self.def_label.setText(self.current_card['definition'])
        self.def_label.hide()
        self.show_def_btn.setEnabled(True)
        self.know_btn.setEnabled(True)
        self.dont_know_btn.setEnabled(True)

        self.update_progress()

    def show_definition(self):
        '''Определение текущего термина'''
        if self.current_card:
            self.def_label.show()

    def mark_known(self):
        '''Отметка изученного термина'''
        if self.current_card:
            self.learned.add(self.current_card['id'])
            self.next_card()

    def update_progress(self):
        '''Обновляем счетчик прогресса'''
        studied = len(self.learned)
        total = len(self.cards)
        self.progress_bar.setValue(studied)
        self.progress_bar.setFormat(f'Изучено: {studied} из {total}')

    def restart_game(self):
        '''Перезапускает игру - сбрасывает прогресс'''
        self.learned.clear()  # Очищаем множество изученных карточек
        self.next_card()
        self.update_progress()

    def show_random_term(self):
        '''Показывает случайный термин (не влияет на прогресс)'''
        random_card = random.choice(self.cards)
        self.def_label.hide()
        # Или только из не изученных
        # available = [c for c in self.cards if c['id'] not in self.learned]
        # random_card = random.choice(available) if available else random.choice(self.cards)
        self.term_label.setText(random_card['term'])
        self.def_label.setText(random_card['definition'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CodeLearnApp()
    window.show()
    sys.exit(app.exec_()) # гарантируем чистый выход из программы
