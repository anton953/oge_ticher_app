import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, QMainWindow)
from PySide6.QtCharts import (QChart, QChartView, QBarSet, QBarSeries, 
                             QBarCategoryAxis, QValueAxis)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QSizePolicy # Не забудь добавить в импорт

class TimeStatsWidget(QWidget):
    def __init__(self, data_dict, typee):
        super().__init__()
        self.data = data_dict # :param data_dict: Словарь вида {1: {'time': 45, 'is_correct': True}, ...}
        self.type = typee
        self.layout = QVBoxLayout(self)
        self.setup_ui()


    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Заголовок
        header = QLabel("Время выполнения заданий" if self.type == 'one' else'Среднее время выполнения заданий')
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(header)

        # Создаем график
        self.chart = QChart()
        # self.chart.setTitle("Зеленый — верно, Красный — ошибка")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # Создаем два набора данных для разных цветов
        set_correct = QBarSet("Верно" if self.type == 'one' else'Преобладание правельных ответов')
        set_correct.setColor(QColor("#2ecc71")) # Зеленый
        
        set_incorrect = QBarSet("Неверно" if self.type == 'one' else'Преобладание неправельных ответов')
        set_incorrect.setColor(QColor("#e74c3c")) # Красный

        categories = []
        
        # Сортируем ключи (номера заданий), чтобы график шел по порядку

        sorted_tasks = sorted([int(i) for i in self.data.keys()])

        for key in sorted_tasks:
            task_id = str(key)

            task_info = self.data[task_id]
            if type(task_info) == dict:
                time_val = task_info['time']
                is_ok = task_info['is_correct']

                categories.append(f"№{task_id}")
                
                if is_ok:
                    set_correct.append(float(time_val))
                    set_incorrect.append(0)
                else:
                    set_correct.append(0)
                    set_incorrect.append(float(time_val))
            else:
                return

        # Группируем наборы в одну серию
        # Используем QBarSeries для обычных столбиков
        series = QBarSeries()
        series.append(set_correct)
        series.append(set_incorrect)
        # Убираем расстояние между столбиками одного задания, чтобы они казались одним
        series.setBarWidth(0.8) 

        self.chart.addSeries(series)

        # Настройка оси X (Номера заданий)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Настройка оси Y (Время в сек)
        axis_y = QValueAxis()
        # Определяем максимум для шкалы (максимальное время + запас)
        max_time = max([v['time'] for v in self.data.values()]) if self.data else 60
        axis_y.setRange(0, max_time + 10)
        axis_y.setTitleText("Время (сек)")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Виджет для отображения
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        # 2. Устанавливаем минимальную высоту, чтобы график всегда был виден
        # Можешь поставить 300 или 400 в зависимости от дизайна
        chart_view.setMinimumHeight(400) 
        
        # 3. Настраиваем политику размера для самого вьювера
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 4. Отключаем встроенную прокрутку QChartView
        chart_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        chart_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.addWidget(chart_view)

    

# --- Пример использования ---
class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Монитор ОГЭ")
        self.resize(900, 500)

        # Тестовые данные согласно твоему формату
        test_data = {
            1: {'time': 30, 'is_correct': True},
            2: {'time': 120, 'is_correct': False},
            3: {'time': 45, 'is_correct': True},
            4: {'time': 200, 'is_correct': False},
            5: {'time': 15, 'is_correct': True},
            6: {'time': 60, 'is_correct': True}
        }

        # Создаем наш новый виджет и передаем данные
        self.stats_widget = TimeStatsWidget(test_data)
        self.setCentralWidget(self.stats_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec())