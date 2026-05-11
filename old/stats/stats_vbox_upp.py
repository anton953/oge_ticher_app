import sys
from datetime import datetime, timedelta
import pyqtgraph as pg
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QProgressBar, QScrollArea, QFrame, QGridLayout)
from PySide6.QtCore import Qt


from helps.stats_module import StatsManager

class TabStats(QWidget):
    def __init__(self):
        super().__init__()
        self.sm = StatsManager()
        # Нормативы времени в секундах (примерные по ФИПИ)
        self.time_standards = {
            "1": 120, "2": 180, "3": 120, "4": 120, "5": 120,
            "6": 240, "7": 120, "8": 300, "9": 300, "10": 180,
            "11": 60, "12": 60, "13": 1200, "14": 1800, "15": 2700
        }
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI';")

        # --- 1. ВЕРХНИЕ КАРТОЧКИ ---
        top_panel = QHBoxLayout()
        self.readiness_card = self.create_stat_card("ГОТОВНОСТЬ", "0%", "#6200EE")
        self.time_card = self.create_stat_card("СРЕДНЕЕ ВРЕМЯ", "0с", "#03DAC6")
        top_panel.addWidget(self.readiness_card)
        top_panel.addWidget(self.time_card)
        self.main_layout.addLayout(top_panel)

        # --- 2. КАЛЕНДАРЬ АКТИВНОСТИ (НОВОЕ) ---
        self.main_layout.addWidget(QLabel("АКТИВНОСТЬ ЗА ПОСЛЕДНИЙ МЕСЯЦ"))
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(4)
        self.draw_calendar()
        self.main_layout.addLayout(self.calendar_grid)

        # --- 3. ГРАФИКИ ---
        graphs_layout = QHBoxLayout()
        self.time_plot = pg.PlotWidget(title="Твое время vs Норматив")
        self.time_plot.setBackground('#1E1E1E')
        graphs_layout.addWidget(self.time_plot)
        self.main_layout.addLayout(graphs_layout)

        # --- 4. СПИСОК ЗАДАНИЙ ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.container = QWidget()
        self.grid_tasks = QGridLayout(self.container)
        scroll.setWidget(self.container)
        self.main_layout.addWidget(scroll)

        self.refresh_data()

    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"background: #1E1E1E; border-left: 5px solid {color}; border-radius: 10px; padding: 10px;")
        l = QVBoxLayout(card)
        l.addWidget(QLabel(title), alignment=Qt.AlignTop)
        v = QLabel(value); v.setObjectName("val"); v.setStyleSheet("font-size: 24px; font-weight: bold;")
        l.addWidget(v)
        return card

    def draw_calendar(self):
        # Рисуем сетку 4 недели x 7 дней
        activity_data = self.sm.stats.get("activity", {})
        today = datetime.now()
        
        for i in range(28): # последние 28 дней
            date = today - timedelta(days=27-i)
            date_str = date.strftime("%Y-%m-%d")
            count = activity_data.get(date_str, 0)
            
            day_box = QFrame()
            # Цвет зависит от интенсивности (0, 1-2, 3-5, 6+)
            color = "#1E1E1E" # пустой
            if count > 0: color = "#0E4429" # слабый зеленый
            if count > 3: color = "#26a641" # средний
            if count > 6: color = "#39d353" # яркий
            
            day_box.setFixedSize(15, 15)
            day_box.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
            day_box.setToolTip(f"{date_str}: {count} задач")
            
            self.calendar_grid.addWidget(day_box, 0, i) # в один ряд для простоты

    def refresh_data(self):
        data = self.sm.get_dashboard_data()
        self.readiness_card.findChild(QLabel, "val").setText(f"{data['total_readiness']}%")
        
        # Обновляем график времени с нормативом
        ids = [int(k) for k in data['tasks'].keys()]
        times = [d['avg_time'] for d in data['tasks'].values()]
        standards = [self.time_standards.get(str(k), 0) for k in ids]

        self.time_plot.clear()
        # Столбики игрока
        bg = pg.BarGraphItem(x=ids, height=times, width=0.6, brush='#03DAC6', name="Твое время")
        self.time_plot.addItem(bg)
        # Линия норматива (Красная пунктирная)
        self.time_plot.plot(ids, standards, pen=pg.mkPen('r', width=2, style=Qt.DashLine), symbol='x', name="Норматив")

        # Плитка задач
        for i, (tid, tdata) in enumerate(data['tasks'].items()):
            f = QFrame()
            f.setStyleSheet("background: #252525; border-radius: 5px; padding: 5px;")
            l = QVBoxLayout(f)
            l.addWidget(QLabel(f"Задание {tid}"))
            pb = QProgressBar(); pb.setValue(int(tdata['mastery']))
            l.addWidget(pb)
            self.grid_tasks.addWidget(f, i // 5, i % 5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sm = StatsManager()
    
    # Эмуляция активности для теста календаря
    sm.stats["activity"] = {"2026-04-20": 2, "2026-04-21": 8, "2026-04-18": 1}
    
    win = UltraDashboard(sm)
    win.resize(900, 700)
    win.show()
    sys.exit(app.exec())