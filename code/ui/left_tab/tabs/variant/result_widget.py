import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy)
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt

class ResultsWidget(QWidget):
    def __init__(self, results_data):
        super().__init__()
        self.setWindowTitle("Результаты ОГЭ")
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["№", "Ваш ответ", "Верно", "Статус"])
        
        # Растягиваем колонки по ширине
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Убираем вертикальный заголовок (индексы 1, 2, 3 слева)
        self.table.verticalHeader().setVisible(False)
        
        # Отключаем скроллбары
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.display_results(results_data)
        self.layout.addWidget(self.table)
        
        # Добавляем "пружину" снизу, чтобы таблица прижималась к верху
        self.layout.addStretch()

    def display_results(self, data):
        self.table.setRowCount(len(data))
        black_brush = QBrush(QColor("black"))
        
        for row, (task_num, answers) in enumerate(data.items()):
            correct_ans, user_ans = answers
            is_correct = str(correct_ans).strip().lower() == str(user_ans).strip().lower()
            
            bg_color = QColor("#d4edda") if is_correct else QColor("#f8d7da")
            
            items = [
                QTableWidgetItem(str(task_num)),
                QTableWidgetItem(str(user_ans)),
                QTableWidgetItem(str(correct_ans)),
                QTableWidgetItem("✅" if is_correct else "❌")
            ]

            for item in items:
                item.setBackground(bg_color)
                item.setForeground(black_brush)
                item.setTextAlignment(Qt.AlignCenter)
                # Запрещаем редактирование ячеек
                item.setFlags(Qt.ItemIsEnabled) 

            for col, item in enumerate(items):
                self.table.setItem(row, col, item)

        # ПОСЛЕ заполнения подгоняем размер
        self.table.resizeRowsToContents() # Сначала подгоняем высоту строк под текст
        
        header_height = self.table.horizontalHeader().height()
        rows_height = sum([self.table.rowHeight(i) for i in range(self.table.rowCount())])
        final_height = header_height + rows_height + 2
        
        self.table.setFixedHeight(final_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Пример данных
    test_results = {str(i): ("Ответ", "Ответ") for i in range(1, 16)} # 15 заданий ОГЭ
    
    window = ResultsWidget(test_results)
    window.show()
    sys.exit(app.exec())