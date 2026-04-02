from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from data.progress_manager import ProgressManager
import json


class ProgressWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = ProgressManager("data/progress.json")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.weak_label = QLabel()
        layout.addWidget(self.weak_label)

        self.export_btn = QPushButton("📄 Экспорт результатов")
        layout.addWidget(self.export_btn)

        self.export_btn.clicked.connect(self.export)

        self.update_progress()

    def update_progress(self):
        data = self.manager.data

        self.label.setText(
            f"📊 Решено: {data['total_answered']}\n"
            f"📈 Успех: {self.manager.get_percent()}%"
        )

        weak = self.manager.get_weak_topics()

        if weak:
            text = "⚠ Слабые темы:\n"
            for topic, percent in weak:
                text += f"- {topic}: {percent}%\n"
        else:
            text = "🔥 Нет слабых тем!"

        self.weak_label.setText(text)

    def export(self):
        with open("results.txt", "w", encoding="utf-8") as f:
            json.dump(self.manager.data, f, indent=4, ensure_ascii=False)