import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from ui.left_tab.tab_choose import TabChoose
from ui.left_tab.tabs.variant_vbox import VariantVBox
# from ui.left_tab.tabs.stats_vbox import TabStats
from ui.left_tab.tabs.stats_vbox_upp import TabStats



class LeftTab(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setTabPosition(QTabWidget.West)  # West - слева, East - справа

        #  # Дополнительные настройки
        # self.setTabShape(QTabWidget.Rounded)  # Форма вкладок
        # self.setMovable(True)  # Можно перетаскивать
        # self.setDocumentMode(True)  # Компактный режим


        # Создаем вкладки
        self.addTab(self.create_learning_tab(), "Обучение")
        self.addTab(self.create_trening_tab(), "Тренеровка")
        self.addTab(self.create_variant_tab(), "Вариант")
        self.addTab(self.create_stats_tab(), "Статистика")
        # self.addTab(self.create_about_tab(), "")



    def create_learning_tab(self):
        widget = TabChoose('learning')
        return widget
    
        


    def create_trening_tab(self):
        widget = TabChoose('trening')
        return widget


    def create_variant_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = VariantVBox(container)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        return widget


    def create_stats_tab(self):
        widget = TabStats()
        return widget

    
    
        

        
