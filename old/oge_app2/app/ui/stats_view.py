from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from app.core.database import Database


class StatsView(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database()

        layout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot()

    def plot(self):
        stats = self.db.get_stats()

        topics = []
        values = []

        for t, c, total in stats:
            topics.append(t)
            values.append(int((c / total) * 100) if total else 0)

        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.bar(topics, values)
        self.canvas.draw()