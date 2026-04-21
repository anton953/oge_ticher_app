import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QProgressBar, QScrollArea, QFrame, QGridLayout)
from PySide6.QtCore import Qt
# from helps.stats_module import StatsManager # Наш предыдущий модуль
from helps.stats_module import StatsManager


class TabStats(QWidget):
    def __init__(self):
        super().__init__()
        self.sm = StatsManager()
        self.init_ui()

    def init_ui(self):
        # Основной вертикальный лейаут
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. ШАПКА: Общая готовность
        self.header_card = QFrame()
        self.header_card.setObjectName("HeaderCard")
        header_layout = QVBoxLayout(self.header_card)
        
        self.lbl_total_readiness = QLabel("0%")
        self.lbl_total_readiness.setObjectName("TotalReadiness")
        self.lbl_total_readiness.setAlignment(Qt.AlignCenter)
        
        lbl_title = QLabel("ОБЩАЯ ГОТОВНОСТЬ К ОГЭ")
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setObjectName("CardTitle")

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(self.lbl_total_readiness)
        self.main_layout.addWidget(self.header_card)

        # 2. СРЕДНИЙ РЯД: Время и Слабые места
        mid_layout = QHBoxLayout()
        
        # Карточка времени
        self.time_card = QFrame()
        time_layout = QVBoxLayout(self.time_card)
        self.lbl_avg_time = QLabel("0 сек")
        self.lbl_avg_time.setObjectName("StatValue")
        time_layout.addWidget(QLabel("Среднее время"), alignment=Qt.AlignCenter)
        time_layout.addWidget(self.lbl_avg_time, alignment=Qt.AlignCenter)
        
        # Карточка слабых мест
        self.weak_card = QFrame()
        weak_layout = QVBoxLayout(self.weak_card)
        self.lbl_weak_points = QLabel("Нет")
        self.lbl_weak_points.setObjectName("StatValue")
        weak_layout.addWidget(QLabel("Нужно подтянуть"), alignment=Qt.AlignCenter)
        weak_layout.addWidget(self.lbl_weak_points, alignment=Qt.AlignCenter)

        mid_layout.addWidget(self.time_card)
        mid_layout.addWidget(self.weak_card)
        self.main_layout.addLayout(mid_layout)

        # 3. СПИСОК ЗАДАНИЙ (Scroll Area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("NoBorderScroll")
        
        container = QWidget()
        self.grid_tasks = QGridLayout(container)
        self.grid_tasks.setSpacing(15)
        
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # Применяем стили "по красоте"
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
            QFrame { background-color: #1E1E1E; border-radius: 15px; padding: 10px; }
            #HeaderCard { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3700B3, stop:1 #03DAC6); }
            #TotalReadiness { font-size: 48px; font-weight: bold; color: white; }
            #CardTitle { font-size: 14px; color: rgba(255,255,255,0.8); letter-spacing: 2px; }
            #StatValue { font-size: 20px; font-weight: bold; color: #03DAC6; }
            QProgressBar { border: none; background-color: #333; height: 8px; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background-color: #03DAC6; border-radius: 4px; }
            QLabel#TaskNum { font-weight: bold; font-size: 16px; }
            #NoBorderScroll { border: none; background-color: transparent; }
        """)

        self.refresh_stats()

    def refresh_stats(self):
        data = self.sm.get_dashboard_data()
        
        # Обновляем шапку
        self.lbl_total_readiness.setText(f"{data['total_readiness']}%")
        self.lbl_avg_time.setText(f"{data['average_speed']} сек")
        
        weak = ", ".join(data['weak_points']) if data['weak_points'] else "Все ок!"
        self.lbl_weak_points.setText(weak)

        # Очистка и заполнение сетки задач
        for i in reversed(range(self.grid_tasks.count())): 
            self.grid_tasks.itemAt(i).widget().setParent(None)

        for i, (tid, tdata) in enumerate(data['tasks'].items()):
            task_widget = self.create_task_item(tid, tdata)
            self.grid_tasks.addWidget(task_widget, i // 2, i % 2) # Сетка в 2 колонки

    def create_task_item(self, tid, tdata):
        item = QFrame()
        item.setMinimumHeight(80)
        layout = QVBoxLayout(item)
        
        top_row = QHBoxLayout()
        lbl_num = QLabel(f"Задание {tid}")
        lbl_num.setObjectName("TaskNum")
        lbl_perc = QLabel(f"{tdata['mastery']}%")
        top_row.addWidget(lbl_num)
        top_row.addStretch()
        top_row.addWidget(lbl_perc)
        
        pb = QProgressBar()
        pb.setValue(int(tdata['mastery']))
        
        lbl_time = QLabel(f"⏱ {tdata['avg_time']}с")
        lbl_time.setStyleSheet("color: #888; font-size: 11px;")

        layout.addLayout(top_row)
        layout.addWidget(pb)
        layout.addWidget(lbl_time)
        return item

# Для запуска теста
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    manager = StatsManager()
    # Тестовые данные
    manager.add_attempt(1, True, 15)
    manager.add_attempt(5, False, 120)
    
    window = DashboardWidget(manager)
    window.resize(600, 800)
    window.show()
    sys.exit(app.exec())