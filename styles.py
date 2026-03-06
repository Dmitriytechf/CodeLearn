# стиль для кнопок
BUTTON_STYLE = '''
    QPushButton {
        background-color: rgba(70, 130, 200, 220);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 15px;
    }
    QPushButton:hover {
        background-color: rgba(100, 150, 220, 220);
    }
    QPushButton:pressed {
        background-color: rgba(50, 100, 180, 220);
    }
'''

# стиль для определения
DEFINITION_STYLE = '''
    QLabel {
        background-color: rgba(128, 0, 255, 120);
        color: white;
        border-radius: 10px;
        padding: 20px;
        max-width: 800px;
        min-width: 600px;
        max-height: 300px;
    }
'''

# стиль для конпки случайного термина
RANDOM_BUTTON_STYLE = '''
    QPushButton {
        background-color: rgba(128, 0, 255, 180);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 30px;
        font-size: 24px;
    }
    QPushButton:hover {
        background-color: rgba(128, 0, 255, 220);
        border: 2px solid white;
    }
    QPushButton:pressed {
        background-color: rgba(100, 0, 200, 220);
    }
'''

# стиль для прогресс-бара
PROGRESS_BAR_STYLE = '''
    QProgressBar {
        border-radius: 20px;
        text-align: center;
        color: white;
        background-color: rgba(255, 92, 250, 80);
        height: 30px;
        font-size: 16px;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background-color: rgba(180, 0, 255, 255);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 100);
    }
'''

# стиль для текста
TEXT_STYLE = 'color: white;'

# размеры кнопок
RANDOM_BUTTON_SIZE = 60
BUTTON_HEIGHT = 60
BUTTON_WIDTH = 400

# Экран
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 900
WINDOW_X = 550
WINDOW_Y = 70

# Прогресс-бара
PROGRESS_WIDTH = 500
PROGRESS_HEIGHT = 27
