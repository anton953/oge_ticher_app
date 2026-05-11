import sys
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QPlainTextEdit, QTextEdit, QSplitter)
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import Qt, QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Форматы для разных элементов кода
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ff79c6"))  # Розовый
        keyword_format.setFontWeight(QFont.Bold)

        builtins_format = QTextCharFormat()
        builtins_format.setForeground(QColor("#8be9fd"))  # Голубой

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#f1fa8c"))  # Желтый

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6272a4"))  # Серо-синий

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#bd93f9"))  # Фиолетовый

        # 1. Ключевые слова Python
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda", "None",
            "nonlocal", "not", "or", "pass", "raise", "return", "True",
            "try", "while", "with", "yield", "self"
        ]
        for word in keywords:
            pattern = QRegularExpression(fr"\b{word}\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # 2. Встроенные функции
        builtins = ["print", "len", "range", "input", "int", "str", "list", "dict"]
        for word in builtins:
            pattern = QRegularExpression(fr"\b{word}\b")
            self.highlighting_rules.append((pattern, builtins_format))

        # 3. Числа
        self.highlighting_rules.append((QRegularExpression(r"\b[0-9]+\b"), number_format))

        # 4. Строки (одинарные и двойные кавычки)
        self.highlighting_rules.append((QRegularExpression(r"'.*?'"), string_format))
        self.highlighting_rules.append((QRegularExpression(r'".*?"'), string_format))

        # 5. Комментарии
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))

    def highlightBlock(self, text):
        """Метод вызывается автоматически при изменении текста"""
        for pattern, char_format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


from PySide6.QtGui import QTextCursor

class CodeEditor(QPlainTextEdit):
    def keyPressEvent(self, event):
        # Если нажат Tab
        if event.key() == Qt.Key_Tab:
            # Вставляем 4 пробела вместо символа табуляции
            self.insertPlainText("    ")
            return # Прерываем стандартную обработку, чтобы фокус не ушел
        
        # Для всех остальных клавиш вызываем стандартное поведение
        super().keyPressEvent(event)

# В основном классе SimpleIDE замените:
# self.editor = QPlainTextEdit() 
# на:
# self.editor = CodeEditor()


class SimpleIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Python IDE")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        splitter = QSplitter(Qt.Vertical)

        # Редактор
        self.editor = CodeEditor()


        # Устанавливаем ширину табуляции равную 4 пробелам
        font_metrics = self.editor.fontMetrics()
        space_width = font_metrics.horizontalAdvance(" ") # Ширина одного пробела в пикселях
        self.editor.setTabStopDistance(4 * space_width)

        self.editor.setPlaceholderText("# Напишите ваш код...")
        # Применяем наш класс подсветки к документу редактора
        self.highlighter = PythonHighlighter(self.editor.document())
        
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 15px;
                background-color: #282a36;
                color: #f8f8f2;
                border: none;
                padding: 10px;
            }
        """)

        # Консоль
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            background-color: #21222c; 
            color: #50fa7b; 
            font-family: monospace;
            border-top: 2px solid #44475a;
            padding: 5px;
        """)

        splitter.addWidget(self.editor)
        splitter.addWidget(self.console)
        layout.addWidget(splitter)

        self.run_button = QPushButton("RUN CODE")
        self.run_button.setCursor(Qt.PointingHandCursor)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #44475a;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #6272a4;
            }
        """)
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

    def run_code(self):
        code = self.editor.toPlainText()
        self.console.clear()
        
        try:
            process = subprocess.Popen(
                [sys.executable, "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            stdout, stderr = process.communicate(timeout=10)

            if stdout:
                self.console.append(stdout)
            if stderr:
                self.console.append(f"<span style='color:#ff5555;'>{stderr}</span>")
                
        except Exception as e:
            self.console.append(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleIDE()
    window.show()
    sys.exit(app.exec())