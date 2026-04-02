# core/question_bank.py
import json
import random
from pathlib import Path
from typing import List, Dict
from .question import Question, QuestionType

class QuestionBank:
    TOPICS = {
        "number_systems": "Системы счисления",
        "logic": "Логика",
        "text_encoding": "Кодирование текста",
        "image_encoding": "Кодирование изображений",
        "sound_encoding": "Кодирование звука",
        "spreadsheets": "Электронные таблицы",
        "databases": "Базы данных",
        "networks": "Сети и адресация",
        "algorithms": "Алгоритмы",
        "programming": "Программирование"
    }
    
    def __init__(self, data_path: str = "data/questions.json"):
        self.data_path = Path(data_path)
        self.questions: List[Question] = []
        self._load()
    
    def _load(self):
        """Загрузка вопросов из JSON"""
        if not self.data_path.exists():
            self._create_sample_data()
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.questions = [Question(**q) for q in data['questions']]
    
    def _create_sample_data(self):
        """Создание примеров вопросов для теста"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        
        sample = {
            "questions": [
                {
                    "id": "ns_001",
                    "type": "single",
                    "topic": "number_systems",
                    "difficulty": 1,
                    "text": "Переведите число 1011₂ в десятичную систему счисления.",
                    "options": ["9", "10", "11", "12"],
                    "correct_answer": "11",
                    "explanation": "1×2³ + 0×2² + 1×2¹ + 1×2⁰ = 8 + 0 + 2 + 1 = 11"
                },
                {
                    "id": "logic_001",
                    "type": "single",
                    "topic": "logic",
                    "difficulty": 2,
                    "text": "Какое логическое выражение эквивалентно ¬(A ∧ B)?",
                    "options": ["¬A ∧ ¬B", "¬A ∨ ¬B", "A ∨ B", "A ∧ ¬B"],
                    "correct_answer": "¬A ∨ ¬B",
                    "explanation": "По закону де Моргана: ¬(A ∧ B) = ¬A ∨ ¬B"
                },
                {
                    "id": "text_001",
                    "type": "single",
                    "topic": "text_encoding",
                    "difficulty": 1,
                    "text": "Сколько байт занимает слово 'КОД' в кодировке ASCII?",
                    "options": ["3", "6", "12", "24"],
                    "correct_answer": "3",
                    "explanation": "В ASCII 1 символ = 1 байт. Слово из 3 букв = 3 байта."
                }
            ]
        }
        
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)
    
    def get_by_topic(self, topic: str, count: int = None) -> List[Question]:
        """Получить вопросы по теме"""
        filtered = [q for q in self.questions if q.topic == topic]
        random.shuffle(filtered)
        return filtered[:count] if count else filtered
    
    def get_exam_set(self) -> List[Question]:
        """Сгенерировать вариант ОГЭ (25 вопросов по спецификации)"""
        exam_spec = {
            "number_systems": 2,
            "logic": 2,
            "text_encoding": 1,
            "image_encoding": 1,
            "sound_encoding": 1,
            "spreadsheets": 3,
            "databases": 2,
            "networks": 2,
            "algorithms": 6,
            "programming": 5
        }
        
        exam_questions = []
        for topic, count in exam_spec.items():
            available = self.get_by_topic(topic, count)
            exam_questions.extend(available)
        
        random.shuffle(exam_questions)
        return exam_questions[:25]
    
    def get_topics_stats(self) -> Dict[str, int]:
        """Статистика по темам"""
        stats = {topic: 0 for topic in self.TOPICS.keys()}
        for q in self.questions:
            if q.topic in stats:
                stats[q.topic] += 1
        return stats