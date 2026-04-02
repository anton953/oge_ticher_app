from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class TheoryWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Раздел теории")
        layout.addWidget(label)