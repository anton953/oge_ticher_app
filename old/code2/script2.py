import os

structure = {
    "oge_app2": {
        "main.py": "",
        "app": {
            "ui": {
                "main_window.py": "",
                "dashboard.py": "",
                "theory_view.py": "",
                "practice_view.py": "",
                "stats_view.py": "",
            },
            "core": {
                "database.py": "",
                "models.py": "",
                "logic.py": "",
            },
            "resources": {
                "styles.qss": "",
            },
            "utils": {
                "progress.py": "",
            },
        },
        "data": {
            "app.db": "",
        },
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    create_structure(".", structure)
    print("Структура проекта создана!")