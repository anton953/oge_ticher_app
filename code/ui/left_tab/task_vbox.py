import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


# from ui.left_tab.tab_choose import TabChoose

from help.task_manager import TaskManager

import requests

class TaskVBox(QVBoxLayout):
    def __init__(self, parent, task_id):
        super().__init__(parent)

        self.task_id = task_id

        self.task_manager = TaskManager()

        self.get_task_lay()
        self.get_line()
        
    def get_task_lay(self):
        # Все задания
        task = self.task_manager.get_random(self.task_id)


        v_box = QVBoxLayout()

        id = QLabel(task['id'])
        id.setStyleSheet("color: red;")
        v_box.addWidget(id)

        condition = task['condition']
        condition_widget = QLabel(condition)
        condition_widget.setFixedWidth(1000)
        condition_widget.setWordWrap(True) # Текст будет переноситься, увеличивая высоту метки
        v_box.addWidget(condition_widget)


        if '<img src=' in condition:
            b = condition.find('\"')
            e = condition.rfind('\"')

            ur = condition[(b + 1):e]

            url = 'https://kpolyakov.spb.ru/cms/images/' + ur



            # await event_source.answer_photo(
            #     photo=url,
            #     # caption=clean_caption
            # )


            response = requests.get(url)

            if response.status_code == 200:
                with open('buuf.jpg', 'wb') as f:
                    f.write(response.content)
                print("Фото успешно скачано")
            else:
                print("Не удалось скачать фото")


            # Создаем метку
            image_label = QLabel()

            # Загружаем картинку из файла
            pixmap = QPixmap("buuf.jpg")

            # Устанавливаем картинку в метку
            image_label.setPixmap(pixmap)

            v_box.addWidget(image_label)


        self.insertLayout(0, v_box)

        # try:
        #     self.insertLayout(0, v_box)
        #     print('insert')
        # except:
        #     self.addLayout(v_box)
        #     print('add')


    def get_line(self):
        h_box = QHBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введите текст и нажмите Enter...")
        h_box.addWidget(self.line_edit)

        self.line_edit.returnPressed.connect(lambda: self.handle_enter())

        btn = QPushButton("Следущее задание")
        h_box.addWidget(btn)
        btn.clicked.connect(lambda: (self.remove_sub_layout(), self.get_task_lay()))
        



        self.addLayout(h_box)


    def handle_enter(self):
        text = self.line_edit.text()
        print(f"Вы ввели: {text}")
        self.line_edit.clear()  # Очистить поле после ввода





    
    def remove_sub_layout(self, index_to_remove=0):
        # 1. Извлекаем элемент из родителя по индексу
        item = self.takeAt(index_to_remove)
        
        if item is not None:
            sub_layout = item.layout()
            
            if sub_layout is not None:
                # 2. Очищаем все виджеты внутри вложенного лейаута
                while sub_layout.count():
                    child = sub_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                    elif child.layout():
                        # Рекурсивно чистим, если там есть еще вложенности
                        remove_sub_layout(sub_layout, 0)
                
                # 3. Удаляем сам объект лейаута из памяти
                sub_layout.deleteLater()

        

        
