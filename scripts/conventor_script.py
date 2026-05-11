import re
import json
import html

for i in range(16, 17):
    # Читаем HTML-файл
    with open(f'/home/v386/Downloads/{i}.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Паттерн для заданий
    pattern_task = r"document\.write\(\s*'\(№&nbsp;(\d+)\)\s*'\s*\);\s*document\.write\(\s*changeImageFilePath\('([^']+)'\)\s*\);"

    # Паттерн для ответов  
    pattern_answer = r'<div class="hidedata" id="(\d+)"><script>\s*document\.write\(\s*changeImageFilePath\(\'([^\']+)\'\)\s*\);\s*</script></div>'

    # Извлекаем задания и ответы
    tasks_raw = re.findall(pattern_task, html_content)
    answers_raw = re.findall(pattern_answer, html_content)

    # Создаём словарь ответов
    answers_dict = {id_num: answer for id_num, answer in answers_raw}

    # Формируем результат
    result = []
    for task_id, condition in tasks_raw:
        # Очищаем условие от HTML-сущностей и экранированных символов
        condition_clean = html.unescape(condition)
        condition_clean = condition_clean.replace('\\n', '\n').replace('\\/', '/').replace("\\'", "'")
        
        # Получаем и очищаем ответ
        answer = answers_dict.get(task_id, "")
        answer_clean = html.unescape(answer)
        answer_clean = answer_clean.replace('\\n', '\n').replace('\\/', '/').replace("\\'", "'")
        
        result.append({
            "id": task_id,
            "condition": condition_clean,
            "answer": answer_clean
        })

    # Сохраняем в JSON-файл
    with open(f'tasks/task_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Извлечено {len(result)} заданий")
    print(f"Файл task_{i}.json создан успешно!")