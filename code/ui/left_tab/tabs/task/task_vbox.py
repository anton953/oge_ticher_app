import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap


# from ui.left_tab.tab_choose import TabChoose

from helps.task_manager import TaskManager

from helps.stats_module_upp import StatsManagerr

import requests
from ui.left_tab.tabs.stats_widget import TaskStatsWidget

class TaskVBox(QVBoxLayout):
    def __init__(self, parent, task_id):
        super().__init__(parent)

        self.task_id = task_id
        self.flag = True

        self.task_manager = TaskManager()

        self.sm = StatsManagerr()

        self.timer = None
        self.start_screen()


    def start_screen(self):
        if self.timer:
            self.timer.stop()
        self.clear(self)

        stats_widget = TaskStatsWidget(self.task_id)
        self.addWidget(stats_widget)


        btn = QPushButton('начать решать вариант')
        btn.clicked.connect(self.cr_all)
        self.addWidget(btn)



    def cr_all(self):
        self.clear(self)
        self.get_task_lay()
        self.get_line()
        self.add_end_btn()

    def add_end_btn(self):
        btn = QPushButton('закончить сессию')
        btn.clicked.connect(self.start_screen)
        self.addWidget(btn)


    def update_label(self):
            self.cnt += 1
            self.time_label.setText(f"Секунды: {self.cnt % 60}\nМтнуты: {self.cnt // 60}")


    def cr_timer(self, per):
        
            self.cnt = 0
            self.time_label = QLabel('Время 0')
            per.addWidget(self.time_label)

            if not self.timer:
                # Создаем таймер
                self.timer = QTimer(self)
                # Подключаем функцию к сигналу timeout
                self.timer.timeout.connect(self.update_label)
                # print('-------------')
                

            # Запускаем с интервалом 1000 мс (1 секунда)
            self.timer.start(1000)
            # print('start#########################', self.timer)
        
        
    def get_task_lay(self):
        self.flag = True
        # self.cr_timer()
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


        
        self.cr_timer(h_box)


        self.addLayout(h_box)

    def btn_conn(self):
        self.line_edit.clear()  # Очистить поле после ввода
        self.cnt = 0

        self.remove_sub_layout()
        self.get_task_lay()
        self.square.setStyleSheet("background-color: grey;")
        # self.btn.setEnabled(True)  # Включить обратно[]



    def handle_enter(self):
        text = self.line_edit.text()
        # print(f"Вы ввели: {text}")
        # self.line_edit.clear()  # Очистить поле после ввода

        if self.flag:
            if self.answer == text.strip():
                print('good answer')

                # self.btn.setEnabled(False) # Отключить[]
                self.square.setStyleSheet("background-color: green;")

                self.sm.add_attempt(self.task_id, True, self.cnt)
                self.flag = False

            else:
                print('wrong answer')
                self.square.setStyleSheet("background-color: red;")

                self.sm.add_attempt(self.task_id, False, self.cnt)







    
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
        
