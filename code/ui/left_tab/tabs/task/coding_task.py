import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

import requests
from helps.task_manager import TaskManager
from helps.ide import PythonEditorWidget
from helps.stats_module_upp import StatsManagerr
from ui.left_tab.tabs.stats_widget import TaskStatsWidget


class TaskCodingHBox(QVBoxLayout):
    def __init__(self, parent, task_id=16):
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
        h_box = QHBoxLayout()

        self.ide = PythonEditorWidget()
        h_box.addWidget(self.ide)

        v_box = QVBoxLayout()
        v_box.addLayout(self.get_task_lay())
        v_box.addLayout(self.get_buttons())
        h_box.addLayout(v_box)

        self.addLayout(h_box)
        self.add_end_btn()


    def add_end_btn(self):
        btn = QPushButton('закончить сессию')
        btn.clicked.connect(self.start_screen)
        self.addWidget(btn)


    def update_label(self):
        self.cnt += 1
        self.time_label.setText(f"Секунды: {self.cnt % 60}\nМинуты: {self.cnt // 60}")


    def cr_timer(self, per):
        self.cnt = 0
        self.time_label = QLabel('Время 0')
        per.addWidget(self.time_label)

        if not self.timer:
            # Создаем таймер
            self.timer = QTimer(self)
            # Подключаем функцию к сигналу timeout
            self.timer.timeout.connect(self.update_label)
        
        # Запускаем с интервалом 1000 мс (1 секунда)
        self.timer.start(1000)

        
    def get_task_lay(self):
        self.flag = True
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
        condition_widget.setFixedWidth(500)
        condition_widget.setFixedHeight(400)
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
                    print("��е удалось скачать фото")

                # Создаем метку
                image_label = QLabel()

                # Загружаем картинку из файла
                pixmap = QPixmap("buuf.jpg")

                # Устанавливаем картинку в метку
                image_label.setPixmap(pixmap)

                v_box.addWidget(image_label)
            except:
                label = QLabel('Не удалось скачать фото')
                v_box.addWidget(label)

        return v_box


    def get_buttons(self):
        h_box = QHBoxLayout()

        # self.btn_check = QPushButton('Проверить')
        # h_box.addWidget(self.btn_check)
        # self.btn_check.clicked.connect(self.con_btn_check)

        self.btn_next = QPushButton('Следующее задание')
        h_box.addWidget(self.btn_next)
        self.btn_next.clicked.connect(self.con_btn_next)

        # self.square = QWidget()
        # self.square.setFixedSize(25, 25) # Задаем размер, чтобы получился квадрат
        # self.square.setStyleSheet("background-color: grey;")
        # h_box.addWidget(self.square)

        self.cr_timer(h_box)

        return h_box


    def con_btn_next(self):
        self.cnt = 0

        self.remove_sub_layout()
        self.cr_all()
        # self.square.setStyleSheet("background-color: grey;")


    def con_btn_check(self):
        text = self.ide.output()

        if self.flag:
            if self.answer == text.strip():
                print('good answer')

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
                        self.clear(child.layout())
                
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
