from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup,
    QLineEdit
)
from PyQt6.QtCore import QTimer

from data.loader import load_questions
from modules.practice.exam_session import ExamSession


class ExamWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.questions = load_questions("data/questions.json")
        self.session = ExamSession(self.questions)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.timer_label = QLabel()
        self.layout.addWidget(self.timer_label)

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.button_group = QButtonGroup(self)
        self.option_buttons = [QRadioButton() for _ in range(4)]
        for btn in self.option_buttons:
            self.layout.addWidget(btn)
            self.button_group.addButton(btn)

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        self.next_button = QPushButton("Ответить")
        self.layout.addWidget(self.next_button)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.next_button.clicked.connect(self.process)

        # ⏱ таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.load_question()
        self.finished = False

    def update_timer(self):
        time_left = self.session.time_left()
        self.timer_label.setText(f"⏳ Осталось: {time_left} сек")

        if time_left <= 0:
            self.finish()

    def load_question(self):
        q = self.session.current()

        if not q:
            self.finish()
            return

        self.question_label.setText(q["question"])
        self.result_label.setText("")

        if q["type"] == "test":
            self.input_field.hide()
            for i, opt in enumerate(q["options"]):
                self.option_buttons[i].setText(opt)
                self.option_buttons[i].show()
                self.option_buttons[i].setChecked(False)
        else:
            for btn in self.option_buttons:
                btn.hide()
            self.input_field.show()
            self.input_field.clear()

        

    def get_answer(self):
        q = self.session.current()

        if q["type"] == "test":
            for btn in self.option_buttons:
                if btn.isChecked():
                    return btn.text()
        else:
            return self.input_field.text().strip()

        return None

    def process(self):
        ans = self.get_answer()

        if not ans:
            self.result_label.setText("Введите ответ!")
            return

        is_correct, correct = self.session.answer(ans)

        if is_correct:
            self.result_label.setText("✅")
        else:
            self.result_label.setText(f"❌ {correct}")

        if self.session.is_finished():
            self.finish()
        else:
            self.load_question()

    def finish(self):
        self.timer.stop()

        self.question_label.setText("Экзамен завершён")

        for btn in self.option_buttons:
            btn.hide()

        self.input_field.hide()
        self.next_button.hide()

        score = self.session.score
        total = len(self.session.questions)
        grade = self.session.get_grade()

        self.result_label.setText(
            f"Баллы: {score}/{total}\nОценка: {grade}"
        )

        def finish(self):
            if self.finished:
                return

            self.finished = True