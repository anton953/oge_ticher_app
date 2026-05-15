import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt

class ResultsWidget(QWidget):
    def __init__(self, results_data):
        super().__init__()
        self.setWindowTitle("Проверка результатов ОГЭ")
        self.resize(500, 400)

        # 1. Создаем макет (layout)
        self.layout = QVBoxLayout(self)

        # 2. Создаем таблицу
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["№", "Ваш ответ", "Верно", "Статус"])
        
        # Растягиваем колонки, чтобы они занимали всё место
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 3. Заполняем таблицу данными
        self.display_results(results_data)

        # Добавляем таблицу в макет
        self.layout.addWidget(self.table)

    def display_results(self, data):
        """
        Метод для обработки словаря и покраски ячеек.
        data: dict вида {"1": ("12", "12"), "2": ("АБВ", "АБГ")}
        Где кортеж это (Правильный, Пользовательский)
        """
        self.table.setRowCount(len(data))
        
        for row, (task_num, answers) in enumerate(data.items()):
            correct_ans, user_ans = answers
            
            # Создаем элементы таблицы
            item_num = QTableWidgetItem(str(task_num))
            item_user = QTableWidgetItem(str(user_ans))
            item_correct = QTableWidgetItem(str(correct_ans))
            item_status = QTableWidgetItem()

            # Сравниваем ответы (убираем лишние пробелы и приводим к регистру)
            is_correct = str(correct_ans).strip().lower() == str(user_ans).strip().lower()

            if is_correct:
                # Если правильно — зеленый
                bg_color = QColor("#d4edda") # Светло-зеленый
                item_status.setText("✅")
            else:
                # Если ошибка — красный
                bg_color = QColor("#f8d7da") # Светло-красный
                item_status.setText("❌")

            text_color = QBrush(QColor("black"))

            # Применяем цвет фона к ячейкам в строке
            for item in [item_num, item_user, item_correct, item_status]:
                item.setBackground(bg_color)   # Цвет фона (тот, что мы делали раньше)
                item.setForeground(text_color) # Устанавливаем черный цвет текста
                
                # Можно также сделать текст жирным или отцентровать его
                item.setTextAlignment(Qt.AlignCenter)
            
            # Вставляем данные в таблицу
            self.table.setItem(row, 0, item_num)
            self.table.setItem(row, 1, item_user)
            self.table.setItem(row, 2, item_correct)
            self.table.setItem(row, 3, item_status)

# Пример использования:
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Имитация данных: Номер задания: (Правильный, Мой ответ)
    test_results = {
        "1": ("12", "12"),
        "2": ("АБВ", "АБГ"),
        "3": ("64", "64"),
        "4": ("15", "10"),
        "5": ("2121", "2121")
    }

    window = ResultsWidget(test_results)
    window.show()

    sys.exit(app.exec())