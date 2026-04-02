import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from ui.main_tab import MainTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ОГЭ Информатика")
        self.resize(1000, 600)

        tabs = MainTab()
        self.setCentralWidget(tabs)
