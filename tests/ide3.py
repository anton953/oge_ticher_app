import sys
import subprocess
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                             QPlainTextEdit, QTextEdit, QSplitter)
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import Qt, QRegularExpression

# --- Класс подсветки (оставляем без изменений) ---
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        fmt = lambda color, bold=False: (
            f := QTextCharFormat(), 
            f.setForeground(QColor(color)), 
            f.setFontWeight(QFont.Bold if bold else QFont.Normal), 
            f
        )[3]

        keywords = ["def", "class", "if", "else", "elif", "return", "import", "from", "for", "while", "print", "self"]
        for w in keywords:
            self.rules.append((QRegularExpression(fr"\b{w}\b"), fmt("#ff79c6", True)))
        
        self.rules.append((QRegularExpression(r"'.*?'|\".*?\""), fmt("#f1fa8c"))) # Строки
        self.rules.append((QRegularExpression(r"#.*"), fmt("#6272a4")))           # Комментарии

    def highlightBlock(self, text):
        for pattern, char_format in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), char_format)

# --- Наш кастомный виджет редактора ---
class PythonEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Убираем отступы, чтобы встроить плотно

        # Разделитель
        self.splitter = QSplitter(Qt.Vertical)

        # Поле ввода кода
        self.editor = QPlainTextEdit()
        self.setup_editor()
        
        # Поле вывода
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background: #1e1e1e; color: #50fa7b; font-family: monospace;")

        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.console)
        
        # Кнопка
        self.run_btn = QPushButton("▶ Запустить код")
        self.run_btn.clicked.connect(self.run_python_code)
        self.run_btn.setStyleSheet("padding: 8px; background: #44475a; color: white; border: none;")

        layout.addWidget(self.splitter)
        layout.addWidget(self.run_btn)

    def setup_editor(self):
        # 4 пробела вместо Tab
        font = QFont("Consolas", 12)
        self.editor.setFont(font)
        metrics = self.editor.fontMetrics()
        self.editor.setTabStopDistance(4 * metrics.horizontalAdvance(" "))
        
        # Подсветка
        self.highlighter = PythonHighlighter(self.editor.document())
        
        # Темная тема
        self.editor.setStyleSheet("""
            QPlainTextEdit { 
                background-color: #282a36; color: #f8f8f2; 
                border: 1px solid #44475a; padding: 5px;
            }
        """)

    def run_python_code(self):
        code = self.editor.toPlainText()
        try:
            res = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True, text=True, encoding='utf-8', timeout=5
            )
            output = res.stdout if res.stdout else res.stderr
            self.console.setPlainText(output)
        except Exception as e:
            self.console.setPlainText(f"Ошибка запуска: {e}")



# --- Пример использования в основном окне ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(PythonEditorWidget()) # Просто вставляем как любой другой виджет
        self.setWindowTitle("Main App")