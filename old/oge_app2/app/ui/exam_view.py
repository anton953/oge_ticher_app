from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer
from app.core.logic import load_tasks


class ExamView(QWidget):
    def __init__(self):
        super().__init__()

        self.tasks = load_tasks()
        self.current = 0
        self.correct = 0
        self.time = 1800

        layout = QVBoxLayout()

        self.timer_label = QLabel()
        layout.addWidget(self.timer_label)

        self.question = QLabel()
        layout.addWidget(self.question)

        self.buttons = []
        for _ in range(4):
            btn = QPushButton()
            btn.clicked.connect(self.answer)
            layout.addWidget(btn)
            self.buttons.append(btn)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

        self.show_task()

    def tick(self):
        self.time -= 1
        self.timer_label.setText(f"{self.time // 60}:{self.time % 60}")

        if self.time <= 0:
            self.finish()

    def show_task(self):
        t = self.tasks[self.current]
        self.question.setText(t["question"])

        for i, opt in enumerate(t["options"]):
            self.buttons[i].setText(opt)

    def answer(self):
        if self.sender().text() == self.tasks[self.current]["answer"]:
            self.correct += 1

        self.current += 1

        if self.current >= len(self.tasks):
            self.finish()
        else:
            self.show_task()

    def finish(self):
        self.timer.stop()
        self.question.setText(f"Результат: {self.correct}/{len(self.tasks)}")