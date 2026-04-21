import json
import os
import time

class StatsManager:
    def __init__(self, filename='user_stats.json'):
        self.filename = filename
        # Веса заданий: 1-12 (базовые) = 1, 13-15 (сложные) = 2
        self.weights = {str(i): (2 if i >= 13 else 1) for i in range(1, 16)}
        self.stats = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Расширенная структура: добавляем время и историю
        return {
            str(i): {
                "correct": 0, 
                "total": 0, 
                "history": [], 
                "total_time": 0,  # в секундах
                "avg_time": 0     # в секундах
            } for i in range(1, 16)
        }

    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=4, ensure_ascii=False)

    def add_attempt(self, task_id, is_correct, seconds_spent):
        """
        Регистрирует попытку.
        seconds_spent: сколько секунд ушло на решение
        """
        tid = str(task_id)
        if tid in self.stats:
            s = self.stats[tid]
            s["total"] += 1
            if is_correct:
                s["correct"] += 1
            
            # Обновляем время
            s["total_time"] += seconds_spent
            s["avg_time"] = round(s["total_time"] / s["total"], 1)
            
            # Обновляем историю (последние 10 попыток для точности)
            s["history"].append(1 if is_correct else 0)
            if len(s["history"]) > 10:
                s["history"].pop(0)
            
            self._save_data()

    def get_dashboard_data(self):
        """Возвращает комплексную статистику для интерфейса."""
        report = {
            "tasks": {},
            "total_readiness": 0,
            "average_speed": 0, # среднее время на одну любую задачу
            "weak_points": []   # список номеров задач, которые идут плохо
        }
        
        weighted_sum = 0
        total_weight = 0
        all_times = []

        for tid, data in self.stats.items():
            # Считаем мастерство по последним попыткам (history)
            recent_attempts = data["history"][-5:] # берем последние 5
            mastery = (sum(recent_attempts) / len(recent_attempts) * 100) if recent_attempts else 0
            
            # Взвешенный прогресс
            weight = self.weights[tid]
            weighted_sum += mastery * weight
            total_weight += weight
            
            if data["avg_time"] > 0:
                all_times.append(data["avg_time"])

            # Добавляем в список слабых мест, если мастерство < 50% и были попытки
            if len(recent_attempts) > 2 and mastery < 50:
                report["weak_points"].append(tid)

            report["tasks"][tid] = {
                "mastery": round(mastery, 1),
                "avg_time": data["avg_time"],
                "total_attempts": data["total"]
            }

        report["total_readiness"] = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0
        report["average_speed"] = round(sum(all_times) / len(all_times), 1) if all_times else 0
        
        return report

# --- Тест-драйв ---
if __name__ == "__main__":
    sm = StatsManager()
    
    # Имитируем решение: задача №1 решена за 30 сек, задача №15 за 300 сек
    sm.add_attempt(1, True, 30)
    sm.add_attempt(15, True, 300)
    sm.add_attempt(15, False, 450) # Ошибся в сложном задании
    
    dashboard = sm.get_dashboard_data()
    print(json.dumps(dashboard, indent=4, ensure_ascii=False))