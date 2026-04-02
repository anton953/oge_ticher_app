import random
import time


class ExamSession:
    def __init__(self, questions, duration_minutes=30):
        self.questions = random.sample(questions, min(15, len(questions)))
        self.index = 0
        self.score = 0

        self.start_time = time.time()
        self.duration = duration_minutes * 60

    def current(self):
        if self.index < len(self.questions):
            return self.questions[self.index]
        return None

    def answer(self, user_answer):
        q = self.current()
        if not q:
            return False, None

        correct = str(q["answer"]).strip()
        user = str(user_answer).strip()

        is_correct = correct == user

        if is_correct:
            self.score += 1

        self.index += 1
        return is_correct, correct

    def is_finished(self):
        return self.index >= len(self.questions) or self.time_left() <= 0

    def time_left(self):
        elapsed = time.time() - self.start_time
        return max(0, int(self.duration - elapsed))

    def get_grade(self):
        # простая шкала (пример)
        if self.score >= 13:
            return 5
        elif self.score >= 10:
            return 4
        elif self.score >= 6:
            return 3
        return 2