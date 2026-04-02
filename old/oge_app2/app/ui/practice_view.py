from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from app.core.logic import load_tasks
from app.core.database import Database


class PracticeView(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.tasks = load_tasks()
        self.current = 0
        self.correct = 0

        layout = QVBoxLayout()

        self.question = QLabel()
        layout.addWidget(self.question)

        self.buttons = []
        for _ in range(4):
            btn = QPushButton()
            btn.clicked.connect(self.answer)
            layout.addWidget(btn)
            self.buttons.append(btn)

        self.result = QLabel()
        layout.addWidget(self.result)

        self.setLayout(layout)
        self.show_task()

    def show_task(self):
        task = self.tasks[self.current]
        self.question.setText(task["question"])

        for i, opt in enumerate(task["options"]):
            self.buttons[i].setText(opt)

    def answer(self):
        if self.sender().text() == self.tasks[self.current]["answer"]:
            self.correct += 1
            self.result.setText("✅")
        else:
            self.result.setText("❌")

        self.current += 1

        if self.current >= len(self.tasks):
            self.finish()
        else:
            self.show_task()

    def finish(self):
        self.db.update_progress("Практика", self.correct, len(self.tasks))
        self.question.setText("Завершено")
        self.result.setText(f"{self.correct}/{len(self.tasks)}")