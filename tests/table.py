from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class TableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример таблицы QTableWidget")
        self.resize(400, 300)
        
        # Создание таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(2)
        
        # Установка заголовков
        self.table.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])
        
        # Заполнение ячеек
        self.table.setItem(0, 0, QTableWidgetItem("Иван"))
        self.table.setItem(0, 1, QTableWidgetItem("25"))
        self.table.setItem(0, 2, QTableWidgetItem("Москва"))
        self.table.setItem(1, 0, QTableWidgetItem("Мария"))
        self.table.setItem(1, 1, QTableWidgetItem("30"))
        self.table.setItem(1, 2, QTableWidgetItem("СПб"))
        
        # Лейаут
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = TableApp()
window.show()
sys.exit(app.exec())
