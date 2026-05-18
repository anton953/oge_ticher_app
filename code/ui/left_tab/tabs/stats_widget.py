import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
                             QFrame, QSizePolicy, QMainWindow, QApplication)
from PySide6.QtCharts import (QChart, QChartView, QBarSet, QBarSeries, 
                             QBarCategoryAxis, QValueAxis, QPieSeries)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor

# 1. НЕ ЗАБУДЬ ДОБАВИТЬ В ИМПОРТЫ НАВЕРХУ ФАЙЛА QStackedBarSeries:
from PySide6.QtCharts import QChart, QChartView, QBarSet, QStackedBarSeries, QBarCategoryAxis, QValueAxis

# Предполагаем, что модуль StatsManager находится в доступной папке.
# Замени на свой актуальный импорт, если имя файла отличается.
try:
    from helps.stats_module_upp import StatsManagerr
except ImportError:
    # Заглушка для теста, если модуля нет под рукой
    class StatsManagerr:
        def __init__(self):
            self.data = {
                "tasks": {
                    "1": {"correct": 9, "total": 10, "avg_time": 45},
                    "2": {"correct": 6, "total": 10, "avg_time": 60},
                    "3": {"correct": 4, "total": 10, "avg_time": 80},
                    "4": {"correct": 1, "total": 10, "avg_time": 120},
                }
            }
        def get_readiness_percent(self):
            return 50


# --- КЛАСС ОБЩЕЙ СТАТИСТИКИ (С ЦВЕТНЫМИ СТОЛБИКАМИ) ---
class GeneralStatsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stats = StatsManagerr()
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # Заголовок и общий процент готовности
        readiness = self.stats.get_readiness_percent()
        header = QLabel(f"Общая готовность к ОГЭ: {readiness}%")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(header)

        # Создаем график
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # Создаем 4 набора данных под каждый цвет
        bar_set_green = QBarSet("Отлично (75-100%)")
        bar_set_blue = QBarSet("Хорошо (50-75%)")
        bar_set_yellow = QBarSet("Удовлетворительно (25-50%)")
        bar_set_red = QBarSet("Требует внимания (0-25%)")

        # Задаем цвета для каждого набора
        bar_set_green.setBrush(QColor(Qt.green))
        bar_set_blue.setBrush(QColor(Qt.cyan))
        bar_set_yellow.setBrush(QColor(QColor(255, 165, 0)))
        bar_set_red.setBrush(QColor(Qt.red))

        categories = []
        
        # Получаем и сортируем номера заданий
        tasks_data = self.stats.data["tasks"]
        sorted_keys = sorted(tasks_data.keys(), key=int)

        for tid in sorted_keys:
            task = tasks_data[tid]
            rate = (task["correct"] / task["total"] * 100) if task["total"] > 0 else 0
            categories.append(f"№{tid}")

            # Распределяем значения по категориям высоты.
            # Если условие выполняется, кладем туда 'rate', иначе '0'
            if 75 <= rate <= 100:
                bar_set_green.append(rate)
                bar_set_blue.append(0)
                bar_set_yellow.append(0)
                bar_set_red.append(0)
            elif 50 <= rate < 75:
                bar_set_green.append(0)
                bar_set_blue.append(rate)
                bar_set_yellow.append(0)
                bar_set_red.append(0)
            elif 25 <= rate < 50:
                bar_set_green.append(0)
                bar_set_blue.append(0)
                bar_set_yellow.append(rate)
                bar_set_red.append(0)
            else: # 0 <= rate < 25
                bar_set_green.append(0)
                bar_set_blue.append(0)
                bar_set_yellow.append(0)
                bar_set_red.append(rate)

        # Создаем серию и добавляем в нее все наборы
        # Поскольку в каждой точке активен только один набор (остальные 0),
        # они будут отображаться как один цветной столбик.
        series = QStackedBarSeries()
        series.append(bar_set_green)
        series.append(bar_set_blue)
        series.append(bar_set_yellow)
        series.append(bar_set_red)
        self.chart.addSeries(series)
        # series.setBarWidth(0.7)

        # Настройка оси X
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Настройка оси Y
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("%")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Скроем легенду, чтобы график выглядел чище (или оставь, если нужны подсказки цветов)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # Виджет для отображения графика
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chart_view)


# --- КЛАСС СТАТИСТИКИ ОТДЕЛЬНОГО ЗАДАНИЯ ---
class TaskStatsWidget(QWidget):
    def __init__(self, task_id):
        super().__init__()
        self.stats = StatsManagerr()
        self.task_id = str(task_id)
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        task_data = self.stats.data["tasks"].get(self.task_id, {"correct": 0, "total": 0, "avg_time": 0})
        
        info_layout = QHBoxLayout()
        title = QLabel(f"Детально по заданию №{self.task_id}")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        time_label = QLabel(f"Ср. время: {task_data['avg_time']} сек.")
        time_label.setAlignment(Qt.AlignRight)
        
        info_layout.addWidget(title)
        info_layout.addStretch()
        info_layout.addWidget(time_label)
        self.layout.addLayout(info_layout)

        series = QPieSeries()
        incorrect = task_data["total"] - task_data["correct"]
        
        slice_correct = series.append(f"Верно: {task_data['correct']}", task_data["correct"])
        slice_wrong = series.append(f"Ошибки: {incorrect}", incorrect)

        slice_correct.setBrush(QColor(Qt.green))
        slice_wrong.setBrush(QColor(Qt.red))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Соотношение ответов")
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chart_view)


# --- ОСНОВНОЕ ОКНО ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статистика ОГЭ")
        self.resize(800, 600)
        
        # Отображаем общую статистику с разноцветными графиками
        self.setCentralWidget(GeneralStatsWidget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())