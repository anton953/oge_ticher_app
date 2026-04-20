import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap


# from ui.left_tab.tab_choose import TabChoose

from help.task_manager import TaskManager

import requests

from pprint import pprint

class VariantVBox(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_manager = TaskManager()
        print('cr')

        self.true_answers = {}
        self.answers = {i: False for i in range(1, 11)}
        

        self.lines = {}


        self.start_screen()

    def cr_all(self):
        self.clear(self)
        self.cr_timer()
        self.cr_btn_end()
        self.cr_var()


    def start_screen(self):
        btn = QPushButton('начать решать вариант')
        btn.clicked.connect(self.cr_all)
        self.addWidget(btn)

    def update_label(self):
        self.cnt += 1
        self.time_label.setText(f"Секунды: {self.cnt % 60}\nМтнуты: {self.cnt // 60}")


    def cr_timer(self):
        self.cnt = 0
        self.time_label = QLabel('Время 0')
        # self.time_label.show()
        self.addWidget(self.time_label)
        # Создаем таймер
        timer = QTimer(self)
        # Подключаем функцию к сигналу timeout
        timer.timeout.connect(self.update_label)
        # Запускаем с интервалом 1000 мс (1 секунда)
        timer.start(1000)



    def cr_btn_end(self):
        btn = QPushButton('завершить вариант')
        btn.clicked.connect(self.end_var)
        self.addWidget(btn)


    def cr_var(self):
        for i in range(1, 11):
            self.get_task_lay(i)

        
    def get_task_lay(self, task_id):
        task = self.task_manager.get_random(task_id)

        self.true_answers[task_id] = task['answer']
        print(task['id'], 'true answer:', self.true_answers[task_id])


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



        h_box = QHBoxLayout()

        self.lines[task_id] = QLineEdit()
        self.lines[task_id].setPlaceholderText("Введите текст и нажмите Enter...")
        h_box.addWidget(self.lines[task_id])

        self.lines[task_id].returnPressed.connect(lambda: self.handle_enter(task_id))

        


        v_box.addLayout(h_box)
        self.addLayout(v_box)
        print('add')



    

    def handle_enter(self, task_id):
        text = self.lines[task_id].text()
        print(f"Вы ввели: {text}")
        # self.line_edit.clear()  # Очистить поле после ввода

        if self.true_answers[task_id] == text.strip():
            self.answers[task_id] = True
            print('good answer')


        else:
            self.answers[task_id] = False
            print('wrong answer')



    def end_var(self):
        self.clear(self)
        pprint(self.answers, indent=4)
        self.addWidget(QLabel(f'{self.answers}'))
        btn = QPushButton('закончить')
        btn.clicked.connect(self.start_screen())
        self.addWidget(btn)




    def clear(self, layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            
            if widget:
                # Если это виджет — удаляем его
                widget.deleteLater()
            elif item.layout():
                # Если это вложенный макет — вызываем эту же функцию для него
                self.clear(item.layout())






    
  