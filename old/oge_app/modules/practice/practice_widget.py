from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QProgressBar
)

from data.loader import load_questions
from data.progress_manager import ProgressManager


class PracticeWidget(QWidget):
    def __init__(self, mode="all"):
        super().__init__()

        self.mode = mode
        self.manager = ProgressManager("data/progress.json")

        self.all_questions = load_questions("data/questions.json")
        self.questions = self.filter_questions()

        self.current_index = 0
        self.score = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.question_label = QLabel()
        self.question_label.setObjectName("card")
        self.layout.addWidget(self.question_label)

        self.button_group = QButtonGroup(self)

        self.option_buttons = []
        for _ in range(4):
            btn = QRadioButton()
            self.layout.addWidget(btn)
            self.button_group.addButton(btn)
            self.option_buttons.append(btn)

        self.next_button = QPushButton("Ответить")
        self.layout.addWidget(self.next_button)

        self.restart_button = QPushButton("🔄 Начать заново")
        self.layout.addWidget(self.restart_button)
        self.restart_button.hide()

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.next_button.clicked.connect(self.handle_answer)
        self.restart_button.clicked.connect(self.restart_test)

        self.load_question()

    def filter_questions(self):
        if self.mode == "mistakes":
            wrong_ids = set(self.manager.data["wrong_questions"])
            return [q for q in self.all_questions if q["id"] in wrong_ids]
        return self.all_questions

    def load_question(self):
        if not self.questions:
            self.question_label.setText("Нет заданий 🎉")
            self.next_button.hide()
            return

        if self.current_index >= len(self.questions):
            self.show_result()
            return

        q = self.questions[self.current_index]

        self.question_label.setText(q["question"])

        for i, option in enumerate(q["options"]):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setChecked(False)
            self.option_buttons[i].show()

        self.result_label.setText("")
        self.next_button.setText("Ответить")

        self.update_progress()

    def update_progress(self):
        total = len(self.questions)
        current = self.current_index
        percent = int((current / total) * 100) if total else 0
        self.progress_bar.setValue(percent)

    def handle_answer(self):
        if self.next_button.text() == "Ответить":
            self.check_answer()
        else:
            self.next_question()

    def check_answer(self):
        selected = None
        for btn in self.option_buttons:
            if btn.text() == correct:
                btn.setStyleSheet("background-color: green;")
            elif btn.isChecked():
                btn.setStyleSheet("background-color: red;")
            if btn.isChecked():
                selected = btn.text()

        if not selected:
            self.result_label.setText("Выберите ответ!")
            return

        q = self.questions[self.current_index]
        correct = q["answer"]

        is_correct = selected == correct

        if is_correct:
            self.score += 1
            self.result_label.setText("✅ Правильно")
        else:
            self.result_label.setText(f"❌ Ответ: {correct}")

        # 🔥 теперь через менеджер
        self.manager.add_result(q["id"], is_correct, q.get("topic"))

        self.next_button.setText("Далее")

    def next_question(self):
        self.current_index += 1
        self.load_question()

    def show_result(self):
        self.question_label.setText("Тест завершён 🎉")

        for btn in self.option_buttons:
            btn.hide()

        self.next_button.hide()
        self.restart_button.show()

        total = len(self.questions)
        percent = int((self.score / total) * 100) if total else 0

        self.result_label.setText(
            f"Результат: {self.score}/{total} ({percent}%)"
        )

    def restart_test(self):
        self.current_index = 0
        self.score = 0
        self.questions = self.filter_questions()

        self.restart_button.hide()
        self.next_button.show()

        for btn in self.option_buttons:
            btn.show()

        self.load_question()




    from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QProgressBar
)

from data.loader import load_questions
from data.progress_manager import ProgressManager


class PracticeWidget(QWidget):
    def __init__(self, mode="all"):
        super().__init__()

        self.mode = mode
        self.manager = ProgressManager("data/progress.json")

        self.all_questions = load_questions("data/questions.json")
        self.questions = self.filter_questions()

        self.current_index = 0
        self.score = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.button_group = QButtonGroup(self)

        self.option_buttons = []
        for _ in range(4):
            btn = QRadioButton()
            self.layout.addWidget(btn)
            self.button_group.addButton(btn)
            self.option_buttons.append(btn)

        self.next_button = QPushButton("Ответить")
        self.layout.addWidget(self.next_button)

        self.restart_button = QPushButton("🔄 Начать заново")
        self.layout.addWidget(self.restart_button)
        self.restart_button.hide()

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.next_button.clicked.connect(self.handle_answer)
        self.restart_button.clicked.connect(self.restart_test)

        self.load_question()

    def filter_questions(self):
        if self.mode == "mistakes":
            wrong_ids = set(self.manager.data["wrong_questions"])
            return [q for q in self.all_questions if q["id"] in wrong_ids]
        return self.all_questions

    def load_question(self):
        if not self.questions:
            self.question_label.setText("Нет заданий 🎉")
            self.next_button.hide()
            return

        if self.current_index >= len(self.questions):
            self.show_result()
            return

        q = self.questions[self.current_index]

        self.question_label.setText(q["question"])

        for i, option in enumerate(q["options"]):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setChecked(False)
            self.option_buttons[i].show()

        self.result_label.setText("")
        self.next_button.setText("Ответить")

        self.update_progress()

    def update_progress(self):
        total = len(self.questions)
        current = self.current_index
        percent = int((current / total) * 100) if total else 0
        self.progress_bar.setValue(percent)

    def handle_answer(self):
        if self.next_button.text() == "Ответить":
            self.check_answer()
        else:
            self.next_question()

    def check_answer(self):
        selected = None
        for btn in self.option_buttons:
            if btn.isChecked():
                selected = btn.text()

        if not selected:
            self.result_label.setText("Выберите ответ!")
            return

        q = self.questions[self.current_index]
        correct = q["answer"]

        is_correct = selected == correct

        if is_correct:
            self.score += 1
            self.result_label.setText("✅ Правильно")
        else:
            self.result_label.setText(f"❌ Ответ: {correct}")

        # 🔥 теперь через менеджер
        self.manager.add_result(q["id"], is_correct)

        self.next_button.setText("Далее")

    def next_question(self):
        self.current_index += 1
        self.load_question()

    def show_result(self):
        self.question_label.setText("Тест завершён 🎉")

        for btn in self.option_buttons:
            btn.hide()

        self.next_button.hide()
        self.restart_button.show()

        total = len(self.questions)
        percent = int((self.score / total) * 100) if total else 0

        self.result_label.setText(
            f"Результат: {self.score}/{total} ({percent}%)"
        )

    def restart_test(self):
        self.current_index = 0
        self.score = 0
        self.questions = self.filter_questions()

        self.restart_button.hide()
        self.next_button.show()

        for btn in self.option_buttons:
            btn.show()

        self.load_question()