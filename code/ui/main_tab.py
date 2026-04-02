import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from ui.left_tab.left_tab import LeftTab
# from ui.main_tab.list_menu import ListMenu


class MainTab(QTabWidget):
    def __init__(self):
        super().__init__()

        # Создаем вкладки
        self.addTab(self.create_home_tab(), "Главная")
        self.addTab(self.create_settings_tab(), "Настройки")
        self.addTab(self.create_about_tab(), "О программе")



    def create_home_tab(self):
        tab = LeftTab()

        return tab

        # widget = QWidget()
        # layout = QVBoxLayout(widget)
        # layout.addWidget(QLabel("Добро пожаловать!"))
        # layout.addWidget(QPushButton("Начать работу"))
        # return widget
    
    def create_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Настройки приложения"))
        return widget
    
    def create_about_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Версия 1.0"))
        return widget
        

        
