import json
import os

class StatsManager:
    def __init__(self, filename='stats.json'):
        self.filename = filename
        # Загружаем данные или создаем пустую структуру
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"tasks": {}, "history": []}

    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_attempt(self, task_id, is_correct, time_spent):
        """
        Добавляет результат решения одного задания.
        :param task_id: Номер задания (строка или число)
        :param is_correct: True если правильно, иначе False
        :param time_spent: Время в секундах
        """
        task_id = str(task_id)
        
        if task_id not in self.data["tasks"]:
            self.data["tasks"][task_id] = {"correct": 0, "total": 0, "avg_time": 0}

        task = self.data["tasks"][task_id]
        
        # Пересчитываем среднее время (упрощенно)
        total_time = task["avg_time"] * task["total"] + time_spent
        task["total"] += 1
        if is_correct:
            task["correct"] += 1
        task["avg_time"] = round(total_time / task["total"], 2)

        self._save_data()

    def get_chart_data(self):
        """
        Возвращает данные, удобные для построения графиков (например, в Chart.js)
        """
        labels = sorted(self.data["tasks"].keys(), key=int)
        success_rates = []
        
        for tid in labels:
            task = self.data["tasks"][tid]
            rate = (task["correct"] / task["total"]) * 100 if task["total"] > 0 else 0
            success_rates.append(round(rate, 1))
            
        return json.dumps({
            "labels": [f"Задание {l}" for l in labels],
            "datasets": [
                {
                    "label": "Процент успеха",
                    "data": success_rates
                }
            ]
        }, ensure_ascii=False)

    def get_readiness_percent(self):
        """Считает общий процент готовности по всем заданиям"""
        total_correct = sum(t["correct"] for t in self.data["tasks"].values())
        total_attempts = sum(t["total"] for t in self.data["tasks"].values())
        
        if total_attempts == 0:
            return 0
        return round((total_correct / total_attempts) * 100, 1)

# Пример использования:
if __name__ == "__main__":
    stats = StatsManager()
    
    # Допустим, пользователь решил 1-е задание за 30 секунд правильно
    stats.add_attempt(task_id=1, is_correct=True, time_spent=30)
    # И 2-е задание за 120 секунд неправильно
    stats.add_attempt(task_id=2, is_correct=False, time_spent=120)

    print(f"Общая готовность: {stats.get_readiness_percent()}%")
    print("Данные для графиков:", stats.get_chart_data())