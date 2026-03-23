# ui/results_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.exam_engine import ExamResult


class ResultsDialog(QDialog):
    def __init__(self, result: ExamResult, parent=None):
        super().__init__(parent)
        self.result = result
        self.setWindowTitle("Результаты экзамена")
        self.setMinimumSize(600, 500)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # === ЗАГОЛОВОК ===
        title = QLabel("🎉 Экзамен завершён!")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # === ОСНОВНЫЕ БАЛЛЫ ===
        scores_layout = QHBoxLayout()
        
        # Первичные
        primary_widget = self._create_score_card(
            "Первичный балл", 
            f"{self.result.correct_answers}/{self.result.total_questions}",
            self._get_score_color(self.result.primary_score, self.result.total_questions)
        )
        scores_layout.addWidget(primary_widget)
        
        # Вторичные
        secondary_widget = self._create_score_card(
            "Отметка", 
            f"{self.result.secondary_score:.0f}",
            self._get_grade_color(self.result.secondary_score)
        )
        scores_layout.addWidget(secondary_widget)
        
        # Процент
        percent_widget = self._create_score_card(
            "Правильно", 
            f"{self.result.percentage:.1f}%",
            self._get_percent_color(self.result.percentage)
        )
        scores_layout.addWidget(percent_widget)
        
        layout.addLayout(scores_layout)
        
        # === ТАБЫ С ДЕТАЛЯМИ ===
        tabs = QTabWidget()
        
        # Вкладка 1: По темам
        topics_tab = self._create_topics_tab()
        tabs.addTab(topics_tab, "📚 По темам")
        
        # Вкладка 2: Ошибки
        if self.result.mistakes:
            mistakes_tab = self._create_mistakes_tab()
            tabs.addTab(mistakes_tab, f"❌ Ошибки ({len(self.result.mistakes)})")
        
        layout.addWidget(tabs)
        
        # === КНОПКИ ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_close = QPushButton("Закрыть")
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px 40px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        self.btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_close)
        
        layout.addLayout(btn_layout)
    
    def _create_score_card(self, title: str, value: str, color: str) -> QWidget:
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Segoe UI", 11))
        title_lbl.setStyleSheet("color: rgba(255,255,255,0.9);")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)
        
        value_lbl = QLabel(value)
        value_lbl.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        value_lbl.setStyleSheet("color: white;")
        value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_lbl)
        
        return widget
    
    def _create_topics_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Тема", "Правильно", "Всего", "Прогресс"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.setRowCount(len(self.result.by_topic))
        
        for i, (topic, (correct, total)) in enumerate(self.result.by_topic.items()):
            # Название темы
            topic_name = topic  # Можно маппинг добавить
            table.setItem(i, 0, QTableWidgetItem(topic_name))
            
            # Статистика
            table.setItem(i, 1, QTableWidgetItem(str(correct)))
            table.setItem(i, 2, QTableWidgetItem(str(total)))
            
            # Прогресс-бар в ячейке
            progress = int((correct / total * 100)) if total else 0
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(progress)
            bar.setTextVisible(True)
            bar.setFormat(f"{progress}%")
            table.setCellWidget(i, 3, bar)
        
        layout.addWidget(table)
        return widget
    
    def _create_mistakes_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        for question, user_answer in self.result.mistakes[:10]:  # Первые 10
            mistake_widget = QWidget()
            mistake_widget.setStyleSheet("""
                QWidget {
                    background-color: #ffebee;
                    border-left: 4px solid #f44336;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
            
            m_layout = QVBoxLayout(mistake_widget)
            
            # Вопрос
            q_text = QLabel(f"<b>Вопрос:</b> {question.text[:100]}...")
            q_text.setWordWrap(True)
            m_layout.addWidget(q_text)
            
            # Ответы
            answers = QLabel(
                f"<span style='color: #f44336;'>Ваш ответ: {user_answer}</span><br>"
                f"<span style='color: #4caf50;'>Правильно: {question.correct_answer}</span>"
            )
            m_layout.addWidget(answers)
            
            # Пояснение
            if question.explanation:
                expl = QLabel(f"<i>💡 {question.explanation}</i>")
                expl.setStyleSheet("color: #666; margin-top: 5px;")
                expl.setWordWrap(True)
                m_layout.addWidget(expl)
            
            scroll_layout.addWidget(mistake_widget)
        
        scroll_layout.addStretch()
        
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll)
        return widget
    
    def _get_score_color(self, score: int, total: int) -> str:
        ratio = score / total
        if ratio >= 0.8: return "#4CAF50"
        if ratio >= 0.6: return "#FF9800"
        return "#f44336"
    
    def _get_grade_color(self, grade: float) -> str:
        if grade >= 4.5: return "#4CAF50"
        if grade >= 3.5: return "#8BC34A"
        if grade >= 3: return "#FF9800"
        return "#f44336"
    
    def _get_percent_color(self, percent: float) -> str:
        if percent >= 80: return "#4CAF50"
        if percent >= 60: return "#FF9800"
        return "#f44336"