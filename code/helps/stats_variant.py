import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter

class ResultChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.chart = QChart()
        self.chart.setTitle("Время выполнения задач")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        self.layout.addWidget(self.chart_view)

    def update_chart(self, results_dict):
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        series = QBarSeries()
        series.setBarWidth(1)
        categories = list(results_dict.keys())
        max_time = 0
        
        # Количество задач
        count = len(categories)

        # Для того чтобы каждый столбец имел свой цвет и стоял в своей категории:
        for i, (task_name, data) in enumerate(results_dict.items()):
            bar_set = QBarSet(task_name)
            time_val = data.get('time', 0)
            is_correct = data.get('is_correct', False)

            # Создаем список значений, где время стоит только на нужной позиции i
            # Пример для 3 задач и второй задачи: [0, 15, 0]
            values = [0] * count
            values[i] = time_val
            bar_set.append(values)
            
            # Настройка цвета
            color = QColor("#4CAF50") if is_correct else QColor("#F44336")
            bar_set.setColor(color)
            bar_set.setBorderColor(color.darker(150))
            
            series.append(bar_set)
            
            if time_val > max_time:
                max_time = time_val

        self.chart.addSeries(series)

        # Настройка оси X
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Настройка оси Y
        axis_y = QValueAxis()
        upper_bound = max_time * 1.2 if max_time > 0 else 10
        axis_y.setRange(0, upper_bound)
        axis_y.setTitleText("Секунды")
        axis_y.setLabelFormat("%d")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Легенда (теперь она будет показывать названия задач с их цветами)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    user_results = {
        "Задача 1": {"is_correct": True, "time": 12},
        "Задача 2": {"is_correct": False, "time": 30},
        "Задача 3": {"is_correct": True, "time": 18},
        "Задача 6": {"is_correct": True, "time": 8},
        "Задача 7": {"is_correct": True, "time": 8},
        "Задача 44": {"is_correct": True, "time": 8},
        "Задача 4568": {"is_correct": True, "time": 8},
        "Задача 4": {"is_correct": True, "time": 8},
        "Задача 49": {"is_correct": True, "time": 8},
        "Задача 45": {"is_correct": True, "time": 8},
        "Задача 43": {"is_correct": True, "time": 8},
        "Задача 41": {"is_correct": True, "time": 8},
        "Задача 5": {"is_correct": False, "time": 45},
    }

    window = QMainWindow()
    chart_widget = ResultChartWidget()
    chart_widget.update_chart(user_results)
    
    window.setCentralWidget(chart_widget)
    window.resize(900, 600)
    window.show()
    
    sys.exit(app.exec())