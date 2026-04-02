from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget
)

import qtawesome as qta

from app.ui.dashboard import Dashboard
from app.ui.theory_view import TheoryView
from app.ui.practice_view import PracticeView
from app.ui.stats_view import StatsView
from app.ui.exam_view import ExamView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ОГЭ Информатика")
        self.resize(1000, 600)

        layout = QHBoxLayout()

        sidebar = QVBoxLayout()

        btn1 = QPushButton(qta.icon('fa5s.home'), " Главная")
        btn2 = QPushButton(qta.icon('fa5s.book'), " Теория")
        btn3 = QPushButton(qta.icon('fa5s.pen'), " Практика")
        btn4 = QPushButton(qta.icon('fa5s.chart-bar'), " Статистика")
        btn5 = QPushButton(qta.icon('fa5s.clock'), " Экзамен")

        sidebar.addWidget(btn1)
        sidebar.addWidget(btn2)
        sidebar.addWidget(btn3)
        sidebar.addWidget(btn4)
        sidebar.addWidget(btn5)
        sidebar.addStretch()

        self.stack = QStackedWidget()

        self.stack.addWidget(Dashboard())
        self.stack.addWidget(TheoryView())
        self.stack.addWidget(PracticeView())
        self.stack.addWidget(StatsView())
        self.stack.addWidget(ExamView())

        btn1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn3.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn4.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn5.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        container = QWidget()
        layout.addLayout(sidebar, 1)
        layout.addWidget(self.stack, 4)

        container.setLayout(layout)
        self.setCentralWidget(container)