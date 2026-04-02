from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class NavigationPanel(QWidget):
    def __init__(self, switch_callback):
        super().__init__()

        self.setFixedWidth(220)

        layout = QVBoxLayout()
        self.setLayout(layout)

        buttons = [
            ("📚 Теория", "theory"),
            ("🧩 Практика", "practice"),
            ("❌ Ошибки", "mistakes"),
            ("🎓 Экзамен", "exam"),
            ("📊 Прогресс", "progress"),
        ]

        for text, name in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, n=name: switch_callback(n))
            layout.addWidget(btn)

        layout.addStretch()