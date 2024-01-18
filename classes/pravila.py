# импорт нужных библиотек и методов
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class Pravila(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/pravila.ui', self)
        self.pravilaok_btn.clicked.connect(self.home_window_opne)

    def home_window_opne(self):
        self.close()
