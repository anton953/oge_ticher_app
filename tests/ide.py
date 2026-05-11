import sys
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QPlainTextEdit, QTextEdit, QSplitter)
from PySide6.QtCore import Qt

class SimpleIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide Code Editor")
        self.resize(800, 600)

        # Главный виджет и слой
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Разделитель (Splitter) для изменения размера областей
        splitter = QSplitter(Qt.Vertical)

        # 1. Окно редактора
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Напишите ваш Python код здесь...")
        self.editor.setPlainText("print('Hello from PySide!')\nimport math\nprint(f'Core of pi: {math.pi}')")
        
        # Стилизация под темную тему (опционально)
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                background-color: #2b2b2b;
                color: #f8f8f2;
            }
        """)

        # 2. Окно вывода (Console)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #1e1e1e; color: #abb2bf; font-family: monospace;")

        splitter.addWidget(self.editor)
        splitter.addWidget(self.console)
        layout.addWidget(splitter)

        # Кнопка запуска
        self.run_button = QPushButton("Запустить код (Run)")
        self.run_button.setFixedHeight(40)
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

    def run_code(self):
        code = self.editor.toPlainText()
        self.console.clear()
        self.console.append("<b>--- Запуск программы ---</b>")

        try:
            # Запускаем через subprocess, чтобы не вешать GUI
            # Мы передаем код через stdin
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
                self.console.append(f"<span style='color:red;'>{stderr}</span>")
                
        except subprocess.TimeoutExpired:
            self.console.append("<span style='color:orange;'>Ошибка: Время ожидания истекло (10 сек)</span>")
        except Exception as e:
            self.console.append(f"<span style='color:red;'>Критическая ошибка: {str(e)}</span>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleIDE()
    window.show()
    sys.exit(app.exec())