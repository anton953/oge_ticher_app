# core/exam_engine.py
from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from .question import Question

@dataclass
class ExamResult:
    total_questions: int
    correct_answers: int
    primary_score: int  # Первичные баллы
    secondary_score: float  # Вторичные (перевод в 5-балльную)
    by_topic: Dict[str, tuple] = field(default_factory=dict)  # (correct, total)
    mistakes: List[tuple] = field(default_factory=list)  # (question, user_answer)
    
    @property
    def percentage(self) -> float:
        return (self.correct_answers / self.total_questions * 100) if self.total_questions else 0

class ExamEngine(QObject):
    # Сигналы для UI
    question_changed = pyqtSignal(int, Question)  # номер, вопрос
    progress_updated = pyqtSignal(int, int)  # текущий, всего
    exam_finished = pyqtSignal(ExamResult)
    answer_recorded = pyqtSignal(int, bool)  # номер вопроса, правильно/нет
    
    def __init__(self):
        super().__init__()
        self.questions: List[Question] = []
        self.current_index: int = 0
        self.answers: Dict[int, str] = {}  # индекс -> ответ
        self.results: Dict[int, bool] = {}  # индекс -> правильно/нет
    
    def start_exam(self, questions: List[Question]):
        """Начать новый экзамен"""
        self.questions = questions
        self.current_index = 0
        self.answers.clear()
        self.results.clear()
        
        self.progress_updated.emit(0, len(self.questions))
        self._emit_current_question()
    
    def _emit_current_question(self):
        """Отправить текущий вопрос в UI"""
        if 0 <= self.current_index < len(self.questions):
            self.question_changed.emit(
                self.current_index + 1, 
                self.questions[self.current_index]
            )
            self.progress_updated.emit(
                self.current_index + 1, 
                len(self.questions)
            )
    
    def answer_current(self, answer: str) -> bool:
        """Ответить на текущий вопрос"""
        if not self.questions or self.current_index >= len(self.questions):
            return False
        
        question = self.questions[self.current_index]
        is_correct = question.check_answer(answer)
        
        self.answers[self.current_index] = answer
        self.results[self.current_index] = is_correct
        
        self.answer_recorded.emit(self.current_index, is_correct)
        
        return is_correct
    
    def next_question(self) -> bool:
        """Перейти к следующему вопросу. False если конец."""
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self._finish_exam()
            return False
        
        self._emit_current_question()
        return True
    
    def previous_question(self) -> bool:
        """Вернуться к предыдущему. False если начало."""
        if self.current_index <= 0:
            return False
        
        self.current_index -= 1
        self._emit_current_question()
        return True
    
    def get_current_answer(self) -> Optional[str]:
        """Получить сохранённый ответ на текущий вопрос"""
        return self.answers.get(self.current_index)
    
    def _finish_exam(self):
        """Завершить экзамен и подсчитать результаты"""
        correct = sum(1 for v in self.results.values() if v)
        total = len(self.questions)
        
        # Статистика по темам
        by_topic: Dict[str, tuple] = {}
        mistakes = []
        
        for i, question in enumerate(self.questions):
            topic = question.topic
            if topic not in by_topic:
                by_topic[topic] = [0, 0]  # [correct, total]
            
            by_topic[topic][1] += 1
            is_correct = self.results.get(i, False)
            if is_correct:
                by_topic[topic][0] += 1
            else:
                mistakes.append((question, self.answers.get(i, "—")))
        
        # Перевод первичных во вторичные (упрощённо)
        # Реальная таблица ФИПИ сложнее, но для MVP:
        primary = correct
        if primary >= 22:
            secondary = 5.0
        elif primary >= 17:
            secondary = 4.0
        elif primary >= 12:
            secondary = 3.0
        else:
            secondary = 2.0
        
        result = ExamResult(
            total_questions=total,
            correct_answers=correct,
            primary_score=primary,
            secondary_score=secondary,
            by_topic={k: tuple(v) for k, v in by_topic.items()},
            mistakes=mistakes
        )
        
        self.exam_finished.emit(result)
    
    def get_progress_percent(self) -> int:
        """Процент прохождения текущего экзамена"""
        if not self.questions:
            return 0
        return int((self.current_index / len(self.questions)) * 100)