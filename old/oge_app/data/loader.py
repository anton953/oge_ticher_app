import json
import os


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

    btn.setStyleSheet("")


def load_progress(path):
    if not os.path.exists(path):
        return {
            "total_answered": 0,
            "correct": 0,
            "wrong_questions": []
        }

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)