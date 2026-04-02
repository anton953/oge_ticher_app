import requests

def load_tasks_online():
    try:
        r = requests.get("https://example.com/tasks.json")
        return r.json()
    except:
        return []