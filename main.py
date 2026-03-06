import sys
import random
import json

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel,
                             QPushButton, QHBoxLayout, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from background import BackgroundWidget
from styles import (BUTTON_STYLE, TEXT_STYLE, BUTTON_HEIGHT,
                    BUTTON_WIDTH, DEFINITION_STYLE, RANDOM_BUTTON_SIZE,
                    RANDOM_BUTTON_STYLE, PROGRESS_BAR_STYLE,
                    WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT,
                    PROGRESS_WIDTH, PROGRESS_HEIGHT)


class CodeLearnApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CodeLearn')
        # Положение окна: setGeometry(x, y, ширина, высота)
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.cards = self.load_cards()
        self.learned = set()           # id изученных карточек
        self.hard_cards = set()        # id карточек, отмеченных "Не знаю"
                                       # (по ТЗ, но пока не юзаем)
        self.current_card = None       # текущая карточка

        # Центральный виджет
        central_widget = BackgroundWidget('img/fon3.jpg', self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # Метка для термина
        self.term_label = self.create_label(
            'Начнем обучение?', 
            font_size=24, 
            bold=True,
            style=TEXT_STYLE
        )
        layout.addWidget(self.term_label)

        # Метка для определения
        self.def_label = self.create_label(
            '', 
            font_size=18, 
            style=DEFINITION_STYLE, 
            word_wrap=True, 
            hidden=True
        )
        layout.addWidget(self.def_label, alignment=Qt.AlignCenter)

        #Основные кнопки
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_font = QFont('Arial', 14, QFont.Bold)
        btn_w, btn_h = BUTTON_WIDTH, BUTTON_HEIGHT
        
        def mk_btn(text, func, hidden=False):
            btn = QPushButton(text)
            btn.clicked.connect(func)
            btn.setFont(btn_font)
            btn.setFixedSize(btn_w, btn_h)
            btn.setStyleSheet(BUTTON_STYLE)
            if hidden:
                btn.hide()
            return btn

        self.show_def_btn = mk_btn('Показать определение', self.show_definition)
        self.know_btn = mk_btn('Знаю', self.mark_known)
        self.dont_know_btn = mk_btn('Не знаю', self.mark_dont_know)
        self.restart_btn = mk_btn('Давай повторим!', self.restart_game, hidden=True)
        for btn in [self.show_def_btn, self.know_btn, self.dont_know_btn, self.restart_btn]:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)
        self.progress_bar.setFixedHeight(PROGRESS_HEIGHT)
        self.progress_bar.setFixedWidth(PROGRESS_WIDTH)
        self.progress_bar.setRange(0, len(self.cards))
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat(f'Изучено: 0 из {len(self.cards)}')
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Нижняя часть
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 30, 10)
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

        self.next_card()

    def create_label(self, text, font_size, bold=False,
                     style=None, word_wrap=False, hidden=False):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Calibri', font_size, QFont.Bold if bold else QFont.Normal))
        if style:
            label.setStyleSheet(style)
        if word_wrap:
            label.setWordWrap(True)
        if hidden:
            label.hide()
        return label

    def load_cards(self):
        '''Загружаем карточки из Json (сейчас это terms.json)'''
        try:
            with open('terms.json', 'r', encoding='utf-8') as f:
                cards = json.load(f)
            return cards
        except FileNotFoundError:
            raise Exception('Ошибка. Файл не найден')

    def next_card(self):
        '''Следующая не изученная карточка'''
        self.def_label.hide()
        # Определяем доступные карточки (не изученные)
        avail = [c for c in self.cards if c['id'] not in self.learned]

        if not avail:
            self.term_label.setText('Поздравляем!\nВы изучили все термины!')
            self.show_def_btn.hide()
            self.know_btn.hide()
            self.dont_know_btn.hide()
            self.restart_btn.show()
            self.update_progress()
            return

        for btn in [self.show_def_btn, self.know_btn, self.dont_know_btn]:
            btn.show()
        self.restart_btn.hide()
        self.current_card = random.choice(avail)
        self.term_label.setText(self.current_card['term'])
        self.def_label.setText(self.current_card['definition'])
        for btn in [self.show_def_btn, self.know_btn, self.dont_know_btn]:
            btn.setEnabled(True)
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

    def mark_dont_know(self):
        '''Отметка "Не знаю" - добавляет термин в список для повторения'''
        if self.current_card:
            # Добавляем в список сложных. Пока просто для соответствия ТЗ
            self.hard_cards.add(self.current_card['id'])
            self.next_card()

    def update_progress(self):
        '''Обновляем счетчик прогресса'''
        studied = len(self.learned)
        total = len(self.cards)
        self.progress_bar.setValue(studied)
        self.progress_bar.setFormat(f'Изучено: {studied} из {total}')

    def restart_game(self):
        '''Перезапускает игру - сбрасывает прогресс'''
        self.learned.clear()
        self.hard_cards.clear()
        self.def_label.hide()
        self.next_card()
        self.update_progress()

    def show_random_term(self):
        '''Показывает случайный термин'''
        self.def_label.hide()
        available = [c for c in self.cards if c['id'] not in self.learned]

        if available:
            random_card = random.choice(available)
            self.term_label.setText(random_card['term'])
            self.def_label.setText(random_card['definition'])
        else:
            reply = QMessageBox.question(
                self, 
                'Повторение',
                'Все термины изучены! Хотите начать заново?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.restart_game()
            else:
                self.term_label.setText('Повторение — мать учения')
                self.def_label.setText('')
                self.def_label.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CodeLearnApp()
    window.show()
    sys.exit(app.exec_()) # гарантируем чистый выход из программы
