import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List")
        self.setGeometry(100, 100, 400, 500)
        
        # Виджеты
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Верхняя панель
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Новая задача...")
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)
        
        # Список задач
        self.task_list = QListWidget()
        
        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.del_button = QPushButton("Удалить")
        self.del_button.clicked.connect(self.delete_task)
        self.clear_button = QPushButton("Очистить всё")
        self.clear_button.clicked.connect(self.task_list.clear)
        btn_layout.addWidget(self.del_button)
        btn_layout.addWidget(self.clear_button)
        
        # Сборка
        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addLayout(btn_layout)
        
        # Обработка Enter
        self.task_input.returnPressed.connect(self.add_task)
        
    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            self.task_list.addItem(task)
            self.task_input.clear()
            
    def delete_task(self):
        current = self.task_list.currentRow()
        if current >= 0:
            self.task_list.takeItem(current)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())