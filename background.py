from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap


class BackgroundWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QPainter(self)                 # создаем художника для рисования
        pixmap = QPixmap(self.image_path)        # загружаем изображение
        painter.drawPixmap(self.rect(), pixmap)  # растягиваем на весь виджет
