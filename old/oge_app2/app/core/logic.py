import json

def load_tasks():
    with open("data/tasks.json", encoding="utf-8") as f:
        return json.load(f)