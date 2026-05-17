import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def load_stylesheet(path):
    """Функция для безопасного чтения файла стилей"""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    print(f"Предупреждение: Файл стилей {path} не найден!")
    return ""


class ThemeManager:
    """Класс для управления темами оформления"""
    def __init__(self, app_instance, base_path):
        self.app = app_instance
        self.base_path = base_path

    def set_theme(self, theme_name):
        """Переключает тему: 'dark' или 'light'"""
        filename = "dark_style.qss" if theme_name == "dark" else "light_style.qss"
        full_path = os.path.join(self.base_path, filename)
        
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                style_data = f.read()
                self.app.setStyleSheet(style_data)
        else:
            print(f"Ошибка: файл темы {full_path} не найден!")


def main():
    app = QApplication(sys.argv)

    # Вычисляем путь к файлу style.qss относительно main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Создаем менеджер тем
    theme_manager = ThemeManager(app, 'styles')
    
    # Включаем светлую тему по умолчанию (можно поменять на 'dark')
    theme_manager.set_theme("light")
    

    window = MainWindow(theme_manager)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


