import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap


# from ui.left_tab.tab_choose import TabChoose

from helps.task_manager import TaskManager

import requests

from pprint import pprint
# from helps.stats_variant import ResultChartWidget
from ui.left_tab.tabs.variant.stats_variant_upp import TimeStatsWidget

from ui.left_tab.tabs.variant.result_widget import ResultsWidget

import json


class VariantVBox(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_manager = TaskManager()
        print('cr')

        self.true_answers = {}
        self.answers = {i: {'answer': '', 'time': 0, 'is_correct': False} for i in range(1, 11)}
        
        self.lines = {}
        self.timer = None

        self.start_screen()


    def cr_all(self):
        self.clear(self)
        self.answers = {i: {'answer': '', 'time': 0, 'is_correct': False} for i in range(1, 11)}
        self.cr_timer()
        self.cr_btn_end()
        self.cr_var()


    def start_screen(self):
        self.clear(self)

        try:
            with open("variant_time_avg.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            # data = {'1': {'time': 1234, 'is_correct': True}, '2': {'time': 0, 'is_correct': False}, '3': {'time': 0, 'is_correct': False}, '4': {'time': 0, 'is_correct': False}, '5': {'time': 0, 'is_correct': False}, '6': {'time': 0, 'is_correct': False}, '7': {'time': 0, 'is_correct': False}, '8': {'time': 0, 'is_correct': False}, '9': {'time': 0, 'is_correct': False}, '10': {'time': 0, 'is_correct': False}}


            chart_widget = TimeStatsWidget(data, 'all')
            self.addWidget(chart_widget)
            print(data)
        except:
            print('не удалось загрузить виджет статистики')

        btn = QPushButton('начать решать вариант')
        btn.setAutoFillBackground(True)
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.clicked.connect(self.cr_all)
        self.addWidget(btn)


    def update_label(self):
        self.cnt += 1
        self.time_label.setText(f"Секунды: {self.cnt % 60}\nМтнуты: {self.cnt // 60}")


    def cr_timer(self):
        self.cnt = 0
        self.time_label = QLabel('Время 0')
        self.addWidget(self.time_label)

        if not self.timer:
            # Создаем таймер
            self.timer = QTimer(self)
            # Подключаем функцию к сигналу timeout
            self.timer.timeout.connect(self.update_label)
            # print('not timer')
            

        # Запускаем с интервалом 1000 мс (1 секунда)
        self.timer.start(1000)
        # print('start#########################', self.timer)


    def cr_btn_end(self):
        btn = QPushButton('завершить вариант')
        btn.setAutoFillBackground(True)
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
    

    def handle_enter(self, task_id):
        text = self.lines[task_id].text()
        print(f"Вы ввели: {text}")
        # self.line_edit.clear()  # Очистить поле после ввода

        if self.true_answers[task_id] == text.strip():
            self.answers[task_id]['answer'] = text
            self.answers[task_id]['is_correct'] = True
            self.answers[task_id]['time'] = self.cnt
            print('good answer')
        else:
            self.answers[task_id]['answer'] = text
            self.answers[task_id]['is_correct'] = False
            self.answers[task_id]['time'] = self.cnt
            print('wrong answer')


    def upstats(self):
        with open("variant_time_avg.json", "r", encoding="utf-8") as file:
            data_time = json.load(file)

        with open("variant_stats_avg.json", "r", encoding="utf-8") as file:
            data_stats = json.load(file)

        for key in self.answers.keys():
            if self.answers[key]['is_correct']:
                data_stats[f'stats_{key}'] = data_stats['cnt'] + 1  
            else:
                data_stats[f'stats_{key}'] = data_stats['cnt']

            ans_time = (self.answers[key]['time'] - self.answers[key - 1]['time'] if key != 1 else self.answers[key]['time'])

            data_time[key] = {
            'time': (int(data_time[str(key)]['time']) + ans_time) // data_stats['cnt'],
            'is_correct': True if data_stats[f'stats_{key}'] > data_stats['cnt'] else False,
            }

        with open("variant_time_avg.json", "w", encoding="utf-8") as file:
            json.dump(data_time, file, ensure_ascii=False, indent=4)

        with open("variant_stats_avg.json", "w", encoding="utf-8") as file:
            json.dump(data_stats, file, ensure_ascii=False, indent=4)


    def cr_stats(self):
        data_time = {
            int(key): {
            'time': self.answers[key]['time'],
            'is_correct': self.answers[key]['is_correct'],
            }
            for key in self.answers.keys()
            }

        data_stats = {
            f'stats_{key}': 0
            for key in self.answers.keys()
            }
        data_stats['cnt'] = 1

        with open("variant_time_avg.json", "w", encoding="utf-8") as file:
            json.dump(data_time, file, ensure_ascii=False, indent=4)

        with open("variant_stats_avg.json", "w", encoding="utf-8") as file:
            json.dump(data_stats, file, ensure_ascii=False, indent=4)


    def end_var(self):
        self.clear(self)
        # pprint(self.answers, indent=4)

        self.upstats()
        # self.cr_stats()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) # Важно: позволяет содержимому адаптироваться

        container = QWidget()
        layout = QVBoxLayout(container)

        s = f'{self.answers}'
        s += f'\n{self.true_answers}'
        s += f'\nСекунды: {self.cnt % 60}'
        s += f'\nМтнуты: {self.cnt // 60}'
        # self.addWidget(QLabel(s))

        ans = {str(i): (self.true_answers[i], self.answers[i]['answer']) for i in range(1, 11)}

        layout.addWidget(ResultsWidget(ans))

        ans = {
            str(key): {
                'is_correct': self.answers[key]['is_correct'],
                'time': (self.answers[key]['time'] - self.answers[key - 1]['time'] if key != 1 else self.answers[key]['time'])
                }
            for key in self.answers.keys()
            }

        chart_widget = TimeStatsWidget(ans, 'one')
        layout.addWidget(chart_widget)

        btn = QPushButton('закончить')
        btn.setAutoFillBackground(True)
        self.timer.stop()
        # self.clear(self)
        btn.clicked.connect(self.start_screen)
        layout.addWidget(btn)


        scroll_area.setWidget(container)

        # 5. Устанавливаем QScrollArea как главный виджет окна
        self.addWidget(scroll_area)


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
