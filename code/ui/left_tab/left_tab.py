import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from ui.left_tab.tab_choose import TabChoose
from ui.left_tab.tabs.variant_vbox import VariantVBox
# from ui.left_tab.tabs.stats_vbox import TabStats
# from ui.left_tab.tabs.stats_vbox3 import UltraDashboard as TabStats
from ui.left_tab.tabs.stats_widget import GeneralStatsWidget as TabStats



class LeftTab(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setTabPosition(QTabWidget.West)  # West - слева, East - справа

        #  # Дополнительные настройки
        # self.setTabShape(QTabWidget.Rounded)  # Форма вкладок
        # self.setMovable(True)  # Можно перетаскивать
        # self.setDocumentMode(True)  # Компактный режим


        # Создаем вкладки
        self.tab_learning = self.create_learning_tab()
        self.addTab(self.tab_learning, "Обучение")

        self.tab_trening = self.create_trening_tab()
        self.addTab(self.tab_trening, "Тренеровка")
        
        self.tab_var = self.create_variant_tab()
        self.addTab(self.tab_var, "Вариант")
        
        self.tab_stats = self.create_stats_tab()
        self.addTab(self.tab_stats, "Статистика")
        # self.addTab(self.create_about_tab(), "")

        self.currentChanged.connect(self.on_tab_changed)


    def on_tab_changed(self, index):
        # Допустим, индекс нашей обновляемой вкладки — 1
        if index == 3:
            self.refresh_second_tab(index)

        

    
    def refresh_second_tab(self, index):
        # 1. Stop the widget from sending signals (preventing the loop)
        self.blockSignals(True)
        
        try:
            old_widget = self.widget(index)
            
            # Create the new widget
            new_widget = self.create_stats_tab()
            
            # Replace the tab
            self.removeTab(index)
            # Note: Restoring the original title "Статистика"
            self.insertTab(index, new_widget, "Статистика")
            
            # Set focus back
            self.setCurrentIndex(index)
            
            if old_widget:
                old_widget.deleteLater()
        finally:
            # 2. Re-enable signals so the UI stays interactive
            self.blockSignals(False)





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

    
    
        

        
