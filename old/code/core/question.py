# core/question.py
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class QuestionType(Enum):
    SINGLE_CHOICE = "single"      # Задания 1-12
    MULTIPLE_CHOICE = "multiple"  # Если понадобится
    TEXT_INPUT = "text"           # Задания 13-15 (позже)
    MATCHING = "matching"         # Задания на соответствие

@dataclass
class Question:
    id: str
    type: QuestionType
    topic: str           # "number_systems", "logic", etc.
    difficulty: int      # 1-3
    text: str
    options: List[str]   # Варианты ответа
    correct_answer: str  # Индекс или текст
    explanation: str     # Пояснение при ошибке
    image_path: Optional[str] = None  # Для заданий с картинками
    
    def check_answer(self, answer: str) -> bool:
        return answer.strip().lower() == self.correct_answer.strip().lower()