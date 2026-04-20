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

        self.answer = task['answer']
        print(task['id'], 'true answer:', self.answer)


        v_box = QVBoxLayout()

        id = QLabel(task['id'])
        id.setStyleSheet("color: red;")
        v_box.addWidget(id)

        condition = task['condition']
        condition_widget = QLabel(condition)
        condition_widget.setFixedWidth(1000)
        condition_widget.setFixedHeight(200)
        condition_widget.setWordWrap(True) # Текст будет переноситься, увеличивая высоту метки

        v_box.addWidget(condition_widget)


        if '<img src=' in condition:
            b = condition.find('\"')
            e = condition.rfind('\"')

            ur = condition[(b + 1):e]

            url = 'https://kpolyakov.spb.ru/cms/images/' + ur

            try:
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
            except:
                lablel = QLabel('Не удалось скачать фото')
                v_box.addWidget(lablel)


        self.insertLayout(0, v_box)


    def get_line(self):
        h_box = QHBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введите текст и нажмите Enter...")
        h_box.addWidget(self.line_edit)

        self.line_edit.returnPressed.connect(lambda: self.handle_enter())

        self.btn_next = QPushButton('Следущее задание')
        h_box.addWidget(self.btn_next)
        self.btn_next.clicked.connect(self.btn_conn)

        self.square = QWidget()
        self.square.setFixedSize(25, 25) # Задаем размер, чтобы получился квадрат
        self.square.setStyleSheet("background-color: grey;")
        h_box.addWidget(self.square)
        



        self.addLayout(h_box)

    def btn_conn(self):
        self.line_edit.clear()  # Очистить поле после ввода

        self.remove_sub_layout()
        self.get_task_lay()
        self.square.setStyleSheet("background-color: grey;")
        # self.btn.setEnabled(True)  # Включить обратно[]



    def handle_enter(self):
        text = self.line_edit.text()
        print(f"Вы ввели: {text}")
        # self.line_edit.clear()  # Очистить поле после ввода

        if self.answer == text.strip():
            print('good answer')

            # self.btn.setEnabled(False) # Отключить[]
            self.square.setStyleSheet("background-color: green;")

        else:
            print('wrong answer')
            self.square.setStyleSheet("background-color: red;")







    
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

        

        
