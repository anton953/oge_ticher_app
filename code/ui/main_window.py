# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QStackedWidget,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from core.question_bank import QuestionBank
from core.exam_engine import ExamEngine
from ui.exam_wiget import ExamWidget
from ui.results_dialog import ResultsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ОГЭ Тренажёр по Информатике")
        self.setMinimumSize(900, 700)
        
        # Инициализация ядра
        self.bank = QuestionBank()
        self.engine = ExamEngine()
        
        # Подключение сигналов
        self.engine.exam_finished.connect(self.show_results)
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # === ШАПКА ===
        header = QHBoxLayout()
        
        self.title_label = QLabel("🎓 ОГЭ Тренажёр")
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.addWidget(self.title_label)
        
        header.addStretch()
        
        # Глобальный прогресс готовности (пока заглушка)
        self.readiness_widget = QWidget()
        readiness_layout = QVBoxLayout(self.readiness_widget)
        readiness_layout.setSpacing(5)
        readiness_layout.setContentsMargins(0, 0, 0, 0)
        
        self.readiness_label = QLabel("Готовность: 0%")
        self.readiness_label.setFont(QFont("Segoe UI", 12))
        self.readiness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.readiness_bar = QProgressBar()
        self.readiness_bar.setRange(0, 100)
        self.readiness_bar.setValue(0)
        self.readiness_bar.setTextVisible(False)
        self.readiness_bar.setFixedSize(200, 10)
        
        readiness_layout.addWidget(self.readiness_label)
        readiness_layout.addWidget(self.readiness_bar)
        
        header.addWidget(self.readiness_widget)
        layout.addLayout(header)
        
        # === СТЕК ВИДЖЕТОВ ===
        self.stack = QStackedWidget()
        
        # 1. Главное меню
        self.menu_widget = self._create_menu_widget()
        self.stack.addWidget(self.menu_widget)
        
        # 2. Виджет экзамена
        self.exam_widget = ExamWidget(self.engine)
        self.stack.addWidget(self.exam_widget)
        
        layout.addWidget(self.stack)
        
        # === СТАТУС ===
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
    
    def _create_menu_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Приветствие
        welcome = QLabel("Выберите режим подготовки")
        welcome.setFont(QFont("Segoe UI", 16))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        layout.addSpacing(30)
        
        # Кнопки режимов
        btn_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 20px 40px;
                font-size: 16px;
                border-radius: 10px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        
        # Экзамен
        self.btn_exam = QPushButton("📝 Экзаменационный вариант")
        self.btn_exam.setStyleSheet(btn_style)
        self.btn_exam.setFont(QFont("Segoe UI", 14))
        self.btn_exam.clicked.connect(self.start_exam)
        layout.addWidget(self.btn_exam, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Тематика
        self.btn_topic = QPushButton("📚 Тренировка по темам")
        self.btn_topic.setStyleSheet(btn_style.replace("#4CAF50", "#2196F3").replace("#45a049", "#1976D2").replace("#3d8b40", "#1565C0"))
        self.btn_topic.setFont(QFont("Segoe UI", 14))
        self.btn_topic.clicked.connect(self.start_topic_training)
        layout.addWidget(self.btn_topic, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Марафон
        self.btn_marathon = QPushButton("⚡ Быстрая тренировка (10 вопросов)")
        self.btn_marathon.setStyleSheet(btn_style.replace("#4CAF50", "#FF9800").replace("#45a049", "#F57C00").replace("#3d8b40", "#E65100"))
        self.btn_marathon.setFont(QFont("Segoe UI", 14))
        self.btn_marathon.clicked.connect(self.start_marathon)
        layout.addWidget(self.btn_marathon, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        
        # Статистика
        stats = self._create_stats_panel()
        layout.addWidget(stats)
        
        return widget
    
    def _create_stats_panel(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        topics = self.bank.get_topics_stats()
        total = sum(topics.values())
        
        info = QLabel(f"📊 В базе: {total} вопросов по {len([t for t in topics.values() if t > 0])} темам")
        info.setFont(QFont("Segoe UI", 11))
        layout.addWidget(info)
        
        return widget
    
    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
    
    # === СЛОТЫ ===
    
    def start_exam(self):
        """Начать полный экзамен"""
        questions = self.bank.get_exam_set()
        if len(questions) < 25:
            QMessageBox.warning(self, "Внимание", 
                f"Недостаточно вопросов в базе ({len(questions)}/25).\nДобавьте больше вопросов.")
            return
        
        self.engine.start_exam(questions)
        self.exam_widget.reset()
        self.stack.setCurrentIndex(1)
        self.status_label.setText("Режим: Экзамен")
    
    def start_topic_training(self):
        """Тренировка по теме (пока заглушка — берём случайные)"""
        # TODO: Диалог выбора темы
        questions = self.bank.get_by_topic("number_systems", 10)
        if not questions:
            QMessageBox.warning(self, "Внимание", "Вопросы по этой теме не найдены.")
            return
        
        self.engine.start_exam(questions)
        self.exam_widget.reset()
        self.stack.setCurrentIndex(1)
        self.status_label.setText("Режим: Тренировка по теме")
    
    def start_marathon(self):
        """Быстрая тренировка"""
        all_q = self.bank.questions.copy()
        import random
        random.shuffle(all_q)
        questions = all_q[:10]
        
        self.engine.start_exam(questions)
        self.exam_widget.reset()
        self.stack.setCurrentIndex(1)
        self.status_label.setText("Режим: Быстрая тренировка")
    
    def show_results(self, result):
        """Показать результаты экзамена"""
        dialog = ResultsDialog(result, self)
        dialog.exec()
        
        # Вернуться в меню
        self.stack.setCurrentIndex(0)
        self.status_label.setText("Готов к работе")
        
        # Обновить прогресс (заглушка — потом реальная логика)
        self._update_readiness(result.percentage)
    
    def _update_readiness(self, last_score: float):
        """Обновить индикатор готовности (упрощённо)"""
        # В реальности здесь будет сложная логика из БД
        current = self.readiness_bar.value()
        new_val = min(100, int((current + last_score) / 2))
        self.readiness_bar.setValue(new_val)
        self.readiness_label.setText(f"Готовность: {new_val}%")