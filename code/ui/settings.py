import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap


class SettingsVBox(QVBoxLayout):
    def __init__(self, parent, tm):
        super().__init__(parent)
        self.tm = tm
        self.cr_all()
        self.flag = 'dark'


    def cr_all(self):
        self.addWidget(QLabel("Настройки приложения"))
        btn = QPushButton('ct')
        btn.clicked.connect(self.ct)
        self.addWidget(btn)

    def ct(self):
        self.tm.set_theme(self.flag)
        if self.flag == 'dark':
            self.flag = 'light'
        elif self.flag == 'light':
            self.flag = 'dark'
