import json
import os


class ProgressManager:
    def __init__(self, path):
        self.path = path
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.path):
            return {
                "total_answered": 0,
                "correct": 0,
                "wrong_questions": []
            }

        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def add_result(self, question_id, is_correct):
        self.data["total_answered"] += 1

        if is_correct:
            self.data["correct"] += 1

            # ✅ УДАЛЯЕМ из ошибок если исправил
            if question_id in self.data["wrong_questions"]:
                self.data["wrong_questions"].remove(question_id)
        else:
            # ✅ добавляем без дублей
            if question_id not in self.data["wrong_questions"]:
                self.data["wrong_questions"].append(question_id)

        self.save()

    def get_percent(self):
        total = self.data["total_answered"]
        if total == 0:
            return 0
        return int((self.data["correct"] / total) * 100)

    def reset(self):
        self.data = {
            "total_answered": 0,
            "correct": 0,
            "wrong_questions": []
        }
        self.save()



    def add_result(self, question_id, is_correct, topic=None):
        self.data["total_answered"] += 1

        if "topics" not in self.data:
            self.data["topics"] = {}

        if topic:
            if topic not in self.data["topics"]:
                self.data["topics"][topic] = {"correct": 0, "total": 0}

            self.data["topics"][topic]["total"] += 1

        if is_correct:
            self.data["correct"] += 1
            if topic:
                self.data["topics"][topic]["correct"] += 1

            if question_id in self.data["wrong_questions"]:
                self.data["wrong_questions"].remove(question_id)
        else:
            if question_id not in self.data["wrong_questions"]:
                self.data["wrong_questions"].append(question_id)

        self.save()


    def get_weak_topics(self):
        weak = []

        for topic, stats in self.data.get("topics", {}).items():
            total = stats["total"]
            if total == 0:
                continue

            percent = stats["correct"] / total

            if percent < 0.6:
                weak.append((topic, int(percent * 100)))

        return weak