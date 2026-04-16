import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


# from ui.left_tab.tab_choose import TabChoose

from help.task_manager import TaskManager

import requests

class LearningVBox(QVBoxLayout):
    def __init__(self, parent, task_id):
        super().__init__(parent)

        self.task_id = task_id

        label = QLabel()

        # Загружаем картинку
        pixmap = QPixmap(f"photo/{task_id}.png") # Укажите путь к вашему файлу

        # Устанавливаем картинку в лейбл
        label.setPixmap(pixmap)

        self.addWidget(label)


    def cr_window(self): 

        widget = QWidget()
        main_layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)


        container = QWidget()
        container_layout = TaskVBox(container, task_id)


        
         # main_layout.addWidget(QLabel(f'{self.type_task}: tasks{task_id}'))
        # for i in range(40):
        #     container_layout.addWidget(QLabel(f'task {i}'))


        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        return widget