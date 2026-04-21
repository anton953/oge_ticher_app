import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QProgressBar, QScrollArea, QFrame, QGridLayout)
from PySide6.QtCore import Qt

from helps.stats_module import StatsManager

class TabStats(QWidget):
    def __init__(self):
        super().__init__()
        self.sm = StatsManager()
        self.setWindowTitle("ОГЭ Информатика - Аналитика")
        self.init_ui()

    def init_ui(self):
        # Главный контейнер
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        # --- ВЕРХНЯЯ ПАНЕЛЬ (Карточки) ---
        top_panel = QHBoxLayout()
        
        # Общий прогресс (Крутой градиентный блок)
        self.readiness_card = self.create_stat_card("ГОТОВНОСТЬ", "0%", "#6200EE")
        # Среднее время
        self.time_card = self.create_stat_card("СРЕДНЕЕ ВРЕМЯ", "0с", "#03DAC6")
        # Прогноз баллов (Улучшение: пересчет в оценку ОГЭ)
        self.grade_card = self.create_stat_card("ПРОГНОЗ БАЛЛА", "2", "#CF6679")
        
        top_panel.addWidget(self.readiness_card)
        top_panel.addWidget(self.time_card)
        top_panel.addWidget(self.grade_card)
        self.main_layout.addLayout(top_panel)

        # --- СРЕДНЯЯ ПАНЕЛЬ (Графики) ---
        graphs_layout = QHBoxLayout()
        
        # График 1: Динамика мастерства
        self.history_plot = pg.PlotWidget(title="Динамика последних попыток")
        self.history_plot.setBackground('#1E1E1E')
        self.history_plot.setLabel('left', 'Мастерство', units='%')
        self.history_plot.showGrid(x=True, y=True, alpha=0.3)
        
        # График 2: Время по заданиям
        self.time_bar_plot = pg.PlotWidget(title="Время по номерам заданий")
        self.time_bar_plot.setBackground('#1E1E1E')
        
        graphs_layout.addWidget(self.history_plot)
        graphs_layout.addWidget(self.time_bar_plot)
        self.main_layout.addLayout(graphs_layout, stretch=1)

        # --- НИЖНЯЯ ПАНЕЛЬ (Плитка заданий) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        container = QWidget()
        self.grid_tasks = QGridLayout(container)
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll, stretch=2)

        self.apply_styles()
        self.refresh_data()

    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setMinimumHeight(100)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #1E1E1E;
                border-left: 5px solid {color};
                border-radius: 10px;
            }}
            QLabel {{ background: transparent; }}
        """)
        l = QVBoxLayout(card)
        t = QLabel(title)
        t.setStyleSheet("color: #AAAAAA; font-size: 10px; font-weight: bold;")
        v = QLabel(value)
        v.setObjectName("val_label")
        v.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        l.addWidget(t)
        l.addWidget(v)
        return card

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI'; }
            QProgressBar { border: none; background: #333; height: 6px; border-radius: 3px; }
            QProgressBar::chunk { background: #03DAC6; }
        """)

    def refresh_data(self):
        data = self.sm.get_dashboard_data()
        
        # Обновляем цифры в карточках
        self.readiness_card.findChild(QLabel, "val_label").setText(f"{data['total_readiness']}%")
        self.time_card.findChild(QLabel, "val_label").setText(f"{int(data['average_speed'])}с")
        
        # Простая логика оценки
        score = 2
        if data['total_readiness'] > 80: score = 5
        elif data['total_readiness'] > 60: score = 4
        elif data['total_readiness'] > 40: score = 3
        self.grade_card.findChild(QLabel, "val_label").setText(str(score))

        # Обновляем график истории (Линия)
        # Для примера берем историю первого задания, но в идеале тут должен быть лог всей готовности
        y_data = self.sm.stats["1"]["history"]
        if y_data:
            self.history_plot.clear()
            self.history_plot.plot(y_data, pen=pg.mkPen(color='#BB86FC', width=3), symbol='o')

        # Обновляем столбчатый график (Время)
        task_ids = [int(x) for x in data['tasks'].keys()]
        times = [d['avg_time'] for d in data['tasks'].values()]
        bg = pg.BarGraphItem(x=task_ids, height=times, width=0.6, brush='#03DAC6')
        self.time_bar_plot.clear()
        self.time_bar_plot.addItem(bg)

        # Обновляем плитку задач
        for i, (tid, tdata) in enumerate(data['tasks'].items()):
            task_frame = self.create_task_mini_card(tid, tdata)
            self.grid_tasks.addWidget(task_frame, i // 3, i % 3)

    def create_task_mini_card(self, tid, tdata):
        f = QFrame()
        f.setStyleSheet("background: #252525; border-radius: 8px; padding: 5px;")
        l = QVBoxLayout(f)
        txt = QLabel(f"Задание {tid} ({tdata['mastery']}%)")
        txt.setStyleSheet("font-size: 11px;")
        pb = QProgressBar()
        pb.setValue(int(tdata['mastery']))
        l.addWidget(txt)
        l.addWidget(pb)
        return f

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sm = StatsManager()
    
    # Фейковые данные для красоты при первом запуске
    for i in range(1, 16):
        sm.add_attempt(i, np.random.choice([True, False]), np.random.randint(20, 200))
    
    win = ModernDashboard(sm)
    win.resize(1000, 700)
    win.show()
    sys.exit(app.exec())