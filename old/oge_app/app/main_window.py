from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget

from app.navigation import NavigationPanel
from modules.theory.theory_widget import TheoryWidget
from modules.practice.practice_widget import PracticeWidget
from modules.practice.exam_widget import ExamWidget
from modules.progress.progress_widget import ProgressWidget
from PyQt6.QtCore import QPropertyAnimation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ОГЭ Информатика")
        self.setMinimumSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)

        self.nav = NavigationPanel(self.switch)

        self.stack = QStackedWidget()

        # страницы
        self.theory = TheoryWidget()
        self.practice = PracticeWidget(mode="all")
        self.mistakes = PracticeWidget(mode="mistakes")
        self.exam = ExamWidget()
        self.progress = ProgressWidget()

        self.stack.addWidget(self.theory)
        self.stack.addWidget(self.practice)
        self.stack.addWidget(self.mistakes)
        self.stack.addWidget(self.exam)
        self.stack.addWidget(self.progress)

        layout.addWidget(self.nav)
        layout.addWidget(self.stack)

    def switch(self, name):
        pages = {
            "theory": 0,
            "practice": 1,
            "mistakes": 2,
            "exam": 3,
            "progress": 4
        }

        if name == "exam":
            self.exam = ExamWidget()  # новая сессия
            self.stack.removeWidget(self.stack.widget(3))
            self.stack.insertWidget(3, self.exam)

        if name == "progress":
            self.progress.update_progress()

        self.stack.setCurrentIndex(pages[name])

        self.animation = QPropertyAnimation(self.stack, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.5)
        self.animation.setEndValue(1)
        self.animation.start()