# ui/exam_widget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QButtonGroup, QRadioButton,
    QProgressBar, QScrollArea, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.exam_engine import ExamEngine
from core.question import Question


class ExamWidget(QWidget):
    # Сигнал для возврата в меню
    finished = pyqtSignal()
    
    def __init__(self, engine: ExamEngine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.current_question: Question = None
        self.answer_buttons: list[QRadioButton] = []
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # === ВЕРХНЯЯ ПАНЕЛЬ ===
        top_panel = QHBoxLayout()
        
        # Номер вопроса
        self.number_label = QLabel("Вопрос 1/25")
        self.number_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        top_panel.addWidget(self.number_label)
        
        top_panel.addStretch()
        
        # Прогресс-бар экзамена
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(300)
        top_panel.addWidget(self.progress_bar)
        
        layout.addLayout(top_panel)
        
        # === РАЗДЕЛИТЕЛЬ ===
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #ddd;")
        layout.addWidget(line)
        
        # === ОБЛАСТЬ ВОПРОСА ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        self.question_container = QWidget()
        question_layout = QVBoxLayout(self.question_container)
        question_layout.setSpacing(20)
        
        # Текст вопроса
        self.question_text = QLabel("Текст вопроса загружается...")
        self.question_text.setWordWrap(True)
        self.question_text.setFont(QFont("Segoe UI", 13))
        self.question_text.setStyleSheet("""
            QLabel {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
        """)
        question_layout.addWidget(self.question_text)
        
        # Тема и сложность
        self.meta_label = QLabel("")
        self.meta_label.setFont(QFont("Segoe UI", 10))
        self.meta_label.setStyleSheet("color: #666;")
        question_layout.addWidget(self.meta_label)
        
        # Варианты ответов
        self.answers_group = QButtonGroup(self)
        self.answers_widget = QWidget()
        self.answers_layout = QVBoxLayout(self.answers_widget)
        self.answers_layout.setSpacing(10)
        
        question_layout.addWidget(self.answers_widget)
        question_layout.addStretch()
        
        scroll.setWidget(self.question_container)
        layout.addWidget(scroll)
        
        # === НИЖНЯЯ ПАНЕЛЬ ===
        bottom_panel = QHBoxLayout()
        
        self.btn_prev = QPushButton("← Предыдущий")
        self.btn_prev.setEnabled(False)
        self.btn_prev.clicked.connect(self._on_prev)
        bottom_panel.addWidget(self.btn_prev)
        
        bottom_panel.addStretch()
        
        self.btn_answer = QPushButton("Ответить")
        self.btn_answer.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 30px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.btn_answer.clicked.connect(self._on_answer)
        bottom_panel.addWidget(self.btn_answer)
        
        self.btn_next = QPushButton("Следующий →")
        self.btn_next.setEnabled(False)
        self.btn_next.clicked.connect(self._on_next)
        bottom_panel.addWidget(self.btn_next)
        
        layout.addLayout(bottom_panel)
    
    def _connect_signals(self):
        self.engine.question_changed.connect(self._on_question_changed)
        self.engine.progress_updated.connect(self._on_progress_updated)
    
    def reset(self):
        """Сброс состояния"""
        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(False)
        self.btn_answer.setEnabled(True)
        self.btn_answer.setText("Ответить")
        self.btn_answer.setStyleSheet(self.btn_answer.styleSheet().replace("#f44336", "#4CAF50"))
    
    def _on_question_changed(self, number: int, question: Question):
        """Обновить отображение вопроса"""
        self.current_question = question
        
        # Номер
        total = 25  # или динамически
        self.number_label.setText(f"Вопрос {number}/{self.engine.questions}")
        
        # Текст
        self.question_text.setText(f"<b>Задание {number}.</b><br><br>{question.text}")
        
        # Метаданные
        topic_name = self.engine.bank.TOPICS.get(question.topic, question.topic)
        self.meta_label.setText(f"Тема: {topic_name} | Сложность: {'★' * question.difficulty}")
        
        # Очистить старые варианты
        for btn in self.answer_buttons:
            self.answers_group.removeButton(btn)
            btn.deleteLater()
        self.answer_buttons.clear()
        
        # Создать новые варианты
        for i, option in enumerate(question.options):
            rb = QRadioButton(option)
            rb.setFont(QFont("Segoe UI", 12))
            rb.setStyleSheet("""
                QRadioButton {
                    padding: 10px;
                    background-color: #f9f9f9;
                    border-radius: 6px;
                }
                QRadioButton:hover {
                    background-color: #e3f2fd;
                }
                QRadioButton:checked {
                    background-color: #bbdefb;
                }
            """)
            self.answers_group.addButton(rb, i)
            self.answers_layout.addWidget(rb)
            self.answer_buttons.append(rb)
        
        # Восстановить сохранённый ответ если есть
        saved = self.engine.get_current_answer()
        if saved:
            for btn in self.answer_buttons:
                if btn.text() == saved:
                    btn.setChecked(True)
                    break
        
        # Обновить кнопки навигации
        self.btn_prev.setEnabled(number > 1)
        self.btn_next.setEnabled(False)  # Сначала нужно ответить
    
    def _on_progress_updated(self, current: int, total: int):
        """Обновить прогресс-бар"""
        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)
        self.number_label.setText(f"Вопрос {current}/{total}")
    
    def _on_answer(self):
        """Обработать ответ"""
        # Получить выбранный вариант
        checked = self.answers_group.checkedButton()
        if not checked:
            QMessageBox.warning(self, "Внимание", "Выберите вариант ответа!")
            return
        
        answer = checked.text()
        is_correct = self.engine.answer_current(answer)
        
        # Визуальная обратная связь
        if is_correct:
            checked.setStyleSheet(checked.styleSheet() + "background-color: #c8e6c9;")
        else:
            checked.setStyleSheet(checked.styleSheet() + "background-color: #ffcdd2;")
            # Показать правильный
            correct = self.current_question.correct_answer
            for btn in self.answer_buttons:
                if btn.text() == correct:
                    btn.setStyleSheet(btn.styleSheet() + "background-color: #c8e6c9;")
                    break
        
        # Заблокировать изменение
        for btn in self.answer_buttons:
            btn.setEnabled(False)
        
        # Изменить кнопку
        self.btn_answer.setEnabled(False)
        self.btn_answer.setText("✓ Отвечено" if is_correct else "✗ Неверно")
        self.btn_answer.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 12px 30px;
                font-size: 14px;
                border-radius: 6px;
            }
        """)
        
        # Разрешить переход дальше
        self.btn_next.setEnabled(True)
        if is_correct:
            self.btn_next.setFocus()
    
    def _on_next(self):
        """Следующий вопрос"""
        if not self.engine.next_question():
            # Экзамен закончился
            pass  # Результат обработается через сигнал exam_finished
    
    def _on_prev(self):
        """Предыдущий вопрос"""
        self.engine.previous_question()