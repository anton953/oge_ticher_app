import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

# from ui.left_tab.learning import TabChoose
# from ui.main_tab.list_menu import ListMenu

from ui.left_tab.tabs.task.task_vbox import TaskVBox


from ui.left_tab.tabs.learning.learning_vbox import LearningVBox
# from ui.left_tab.tabs.learning.learning_coding import PythonEditorWidget 


from ui.left_tab.tabs.variant_vbox import VariantVBox

from ui.left_tab.tabs.task.coding_task import TaskCodingHBox

from ui.left_tab.tabs.learning.learning_coding_16 import LearningCoding16




class TabChoose(QTabWidget):
    def __init__(self, type_task):
        super().__init__()

        self.type_task = type_task

        self.TabPosition(QTabWidget.West)

        # Создаем вкладки

        if self.type_task == 'learning':
            for i in range(1, 11):
                self.addTab(self.create_learning_tab(i), f'{i}')

            self.addTab(self.cr_learnin_codig(), '16')

        
        elif self.type_task == 'trening':
            for i in range(1, 11):
                self.addTab(self.create_task_tab(i), f'{i}')

            self.addTab(self.create_coding_task_tab(), '16')


        elif self.type_task == 'variant':
            self.addTab(self.create_variant_tab(i))


    def create_learning_tab(self, task_id):
        widget = QWidget()
        main_layout = LearningVBox(widget, task_id)
        return widget

    def cr_learnin_codig(self):
        widget = QWidget()
        main_layout = LearningCoding16(widget)
        return widget


    def create_task_tab(self, task_id):
        widget = QWidget()
        main_layout = TaskVBox(widget, task_id)
        return widget

    def create_coding_task_tab(self):
        widget = QWidget()
        main_layout = TaskCodingHBox(widget)
        return widget


    def create_variant_tab(self):
        widget = QWidget()
        main_layout = VariantVBox(widget)
        return widget



        # widget = QWidget()
        # main_layout = QVBoxLayout(widget)

        # scroll = QScrollArea()
        # scroll.setWidgetResizable(True)


        # container = QWidget()
        # container_layout = TaskVBox(container, task_id)


        
         # # main_layout.addWidget(QLabel(f'{self.type_task}: tasks{task_id}'))
        # # for i in range(40):
        # #     container_layout.addWidget(QLabel(f'task {i}'))


        # scroll.setWidget(container)
        # main_layout.addWidget(scroll)

        # return widget
    

        
