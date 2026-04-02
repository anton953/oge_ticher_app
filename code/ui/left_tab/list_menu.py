import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

class ListMenu(QListWidget):
    """Меню-табы на основе QListWidget"""
    
    tab_changed = Signal(int)  # Сигнал при смене вкладки
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка внешнего вида"""
        self.setFixedWidth(150)
        self.setStyleSheet("""
            QListWidget {
                background-color: #2d2d30;
                color: #cccccc;
                border: none;
                outline: none;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px 10px;
                border: none;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #3e3e42;
            }
        """)
        
        # Подключаем сигнал выбора
        self.currentRowChanged.connect(self.on_selection_changed)
    
    def add_tab(self, title, icon=None):
        """Добавить вкладку"""
        if icon:
            self.addItem(f"{icon} {title}")
        else:
            self.addItem(title)
    
    def add_tabs(self, tabs_list):
        """Добавить несколько вкладок сразу"""
        for tab in tabs_list:
            if isinstance(tab, tuple):
                self.add_tab(tab[0], tab[1])
            else:
                self.add_tab(tab)
    
    def remove_tab(self, index):
        """Удалить вкладку по индексу"""
        self.takeItem(index)
    
    def clear_tabs(self):
        """Очистить все вкладки"""
        self.clear()
    
    def get_current_tab(self):
        """Получить индекс текущей вкладки"""
        return self.currentRow()
    
    def set_current_tab(self, index):
        """Установить текущую вкладку"""
        self.setCurrentRow(index)
    
    def on_selection_changed(self, index):
        """Обработчик смены вкладки"""
        if index >= 0:
            self.tab_changed.emit(index)





# Пример использования
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TabMenu на QListWidget")
        self.setGeometry(100, 100, 800, 500)
        
        # Создаем центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем меню-табы
        self.tab_menu = ListMenu()
        self.tab_menu.add_tabs([
            ("🏠 Главная"),
            ("📊 Статистика"),
            ("⚙️ Настройки"),
            ("ℹ️ О программе")
        ])
        
        # Создаем область для содержимого
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border-left: 1px solid #ddd;
            }
        """)
        
        # Добавляем содержимое для каждой вкладки
        self.content_stack.addWidget(self.create_home_content())
        self.content_stack.addWidget(self.create_stats_content())
        self.content_stack.addWidget(self.create_settings_content())
        self.content_stack.addWidget(self.create_about_content())
        
        # Подключаем сигнал смены вкладки
        self.tab_menu.tab_changed.connect(self.content_stack.setCurrentIndex)
        
        # Добавляем виджеты в layout
        layout.addWidget(self.tab_menu)
        layout.addWidget(self.content_stack, 1)  # 1 = растягивается
    
    def create_home_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("<h1>Главная страница</h1>"))
        layout.addWidget(QLabel("Добро пожаловать в приложение!"))
        layout.addStretch()
        return widget
    
    def create_stats_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("<h1>Статистика</h1>"))
        layout.addWidget(QLabel("Здесь будет отображаться статистика"))
        return widget
    
    def create_settings_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("<h1>Настройки</h1>"))
        
        # Добавляем элементы настроек
        check = QCheckBox("Включить уведомления")
        combo = QComboBox()
        combo.addItems(["Тема 1", "Тема 2"])
        
        layout.addWidget(check)
        layout.addWidget(combo)
        layout.addStretch()
        return widget
    
    def create_about_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("<h1>О программе</h1>"))
        layout.addWidget(QLabel("Версия 1.0"))
        return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())