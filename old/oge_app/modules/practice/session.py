import random


class TestSession:
    def __init__(self, questions, wrong_ids=None, mode="all"):
        self.mode = mode
        self.all_questions = questions
        self.wrong_ids = set(wrong_ids or [])

        self.questions = self.generate_session()
        self.index = 0
        self.score = 0

    def generate_session(self):
        if self.mode == "mistakes":
            return [q for q in self.all_questions if q["id"] in self.wrong_ids]

        # 🔥 адаптивная логика
        weighted = []

        for q in self.all_questions:
            weight = 3 if q["id"] in self.wrong_ids else 1
            weighted.extend([q] * weight)

        random.shuffle(weighted)

        # убираем дубли
        unique = []
        seen = set()

        for q in weighted:
            if q["id"] not in seen:
                unique.append(q)
                seen.add(q["id"])

        return unique[:10]  # ограничение на тест

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
        return is_correct, correct  # всегда 2 значения

    def is_finished(self):
        return self.index >= len(self.questions)