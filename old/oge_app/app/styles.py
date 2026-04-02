def get_styles():
    return """
    QWidget {
        background-color: #1e1e2f;
        color: #ffffff;
        font-family: Segoe UI;
    }

    QPushButton {
        background-color: #3a86ff;
        border: none;
        padding: 10px;
        border-radius: 10px;
    }

    QPushButton:hover {
        background-color: #5aa0ff;
    }

    QPushButton:pressed {
        background-color: #2f6edc;
    }

    QRadioButton {
        background-color: #2a2a40;
        padding: 8px;
        border-radius: 8px;
    }

    QLineEdit {
        background-color: #2a2a40;
        border-radius: 8px;
        padding: 8px;
    }

    QProgressBar {
        background-color: #2a2a40;
        border-radius: 8px;
        height: 10px;
    }

    QProgressBar::chunk {
        background-color: #3a86ff;
        border-radius: 8px;
    }

    QLabel#card {
    background-color: #2a2a40;
    padding: 15px;
    border-radius: 12px;
    }
    """