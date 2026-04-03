import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

# from ui.left_tab.learning import TabChoose
# from ui.main_tab.list_menu import ListMenu


class TabChoose(QTabWidget):
    def __init__(self, type_task):
        super().__init__()

        self.type_task = type_task

        self.TabPosition(QTabWidget.West)

        # Создаем вкладки
        for i in range(1, 11):
            self.addTab(self.create_home_tab(i), f'{i}')
            



    def create_home_tab(self, n):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # TODO добавить обработчик заданий (пока эмитация)
        layout.addWidget(QLabel(f'{self.type_task}: tasks{n}'))
        for i in range(10): #TODO проблема с прокруткой
            layout.addWidget(QLabel(f'task {i}'))

        return widget
    

        
