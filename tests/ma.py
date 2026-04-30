import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
                             QFrame, QSizePolicy)
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis, QPieSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

# Класс Общей статистики
class GeneralStatsWidget(QWidget):
    def __init__(self, stats_manager):
        super().__init__()
        self.stats = stats_manager
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # Заголовок и общий процент
        readiness = self.stats.get_readiness_percent()
        header = QLabel(f"Общая готовность к ОГЭ: {readiness}%")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(header)

        # Создаем график (Bar Chart)
        self.chart = QChart()
        self.chart.setTitle("Успешность по номерам заданий")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # Данные для графика
        bar_set = QBarSet("Процент успеха")
        categories = []
        
        # Берем данные из нашего StatsManager
        tasks_data = self.stats.data["tasks"]
        # Сортируем задания по порядку 1, 2, 3...
        sorted_keys = sorted(tasks_data.keys(), key=int)

        for tid in sorted_keys:
            task = tasks_data[tid]
            rate = (task["correct"] / task["total"] * 100) if task["total"] > 0 else 0
            bar_set.append(rate)
            categories.append(f"№{tid}")

        series = QBarSeries()
        series.append(bar_set)
        self.chart.addSeries(series)

        # Оси координат
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("%")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Виджет для отображения графика
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chart_view)

# Класс статистики отдельного задания
class TaskStatsWidget(QWidget):
    def __init__(self, stats_manager, task_id):
        super().__init__()
        self.stats = stats_manager
        self.task_id = str(task_id)
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        task_data = self.stats.data["tasks"].get(self.task_id, {"correct": 0, "total": 0, "avg_time": 0})
        
        # Информационная панель
        info_layout = QHBoxLayout()
        title = QLabel(f"Детально по заданию №{self.task_id}")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        time_label = QLabel(f"Ср. время: {task_data['avg_time']} сек.")
        time_label.setAlignment(Qt.AlignRight)
        
        info_layout.addWidget(title)
        info_layout.addStretch()
        info_layout.addWidget(time_label)
        self.layout.addLayout(info_layout)

        # Круговая диаграмма (Pie Chart)
        series = QPieSeries()
        incorrect = task_data["total"] - task_data["correct"]
        
        # Добавляем сегменты
        slice_correct = series.append(f"Верно: {task_data['correct']}", task_data["correct"])
        slice_wrong = series.append(f"Ошибки: {incorrect}", incorrect)

        # Настройка цветов
        slice_correct.setBrush(Qt.green)
        slice_wrong.setBrush(Qt.red)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Соотношение ответов")
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chart_view)

# --- Пример того, как это встроить в окно ---
from PySide6.QtWidgets import QMainWindow, QApplication
from stats import StatsManager # Наш предыдущий модуль

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статистика ОГЭ")
        self.resize(800, 600)
        
        # Загружаем данные
        self.sm = StatsManager()
        
        # Для примера: показываем общую статистику
        # Если хочешь переключаться, используй QStackedWidget
        self.setCentralWidget(TaskStatsWidget(self.sm, 1))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())