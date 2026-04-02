import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                               QWidget, QLabel, QVBoxLayout, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Меню через вкладки")
        self.setGeometry(100, 100, 600, 400)
        
        # Создаем виджет с вкладками
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        # Создаем вкладки
        tabs.addTab(self.create_home_tab(), "Главная")
        tabs.addTab(self.create_settings_tab(), "Настройки")
        tabs.addTab(self.create_about_tab(), "О программе")
        
    def create_home_tab(self):
        """Создание содержимого для вкладки 'Главная'"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Добро пожаловать!"))
        layout.addWidget(QPushButton("Начать работу"))
        return widget
    
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

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())