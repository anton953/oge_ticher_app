import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


# from ui.left_tab.tab_choose import TabChoose

from helps.task_manager import TaskManager

import requests

# TODO make learning coding

class LearningCodingHBox(QHBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)


        self.cr_window()


    def cr_window(self): 

        # 1. Создаем область прокрутки
        scroll = QScrollArea()

        image_label = QLabel()
        pixmap = QPixmap(f"photo/{self.task_id}.png")
        image_label.setPixmap(pixmap)

        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        image_label.setAlignment(Qt.AlignCenter)

        # 3. Помещаем QLabel внутрь ScrollArea
        scroll.setWidget(image_label)

        self.addWidget(scroll)


