import os

# Структура проекта
structure = {
    "oge_app": {
        "app": [
            "main_window.py",
            "navigation.py",
            "styles.py"
        ],
        "modules": {
            "theory": ["theory_widget.py"],
            "practice": ["practice_widget.py"],
            "progress": ["progress_widget.py"]
        },
        "data": ["loader.py"],
        "resources": [],
        "": ["main.py"]  # корень проекта
    }
}


def create_structure(base_path, tree):
    for name, content in tree.items():
        if name == "":
            # файлы в корне
            for file in content:
                file_path = os.path.join(base_path, file)
                open(file_path, "w", encoding="utf-8").close()
        elif isinstance(content, dict):
            dir_path = os.path.join(base_path, name)
            os.makedirs(dir_path, exist_ok=True)
            create_structure(dir_path, content)
        elif isinstance(content, list):
            dir_path = os.path.join(base_path, name)
            os.makedirs(dir_path, exist_ok=True)

            for file in content:
                file_path = os.path.join(dir_path, file)
                open(file_path, "w", encoding="utf-8").close()


def main():
    base_path = os.getcwd()
    create_structure(base_path, structure)
    print("✅ Проект успешно создан!")


if __name__ == "__main__":
    main()