import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from helps.ide import PythonEditorWidget


class LearningCoding16(QVBoxLayout):
    """
    Обучающий tab для задания 16 (программирование на Python).
    Содержит уроки по основным темам.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setContentsMargins(10, 10, 10, 10)
        self.setSpacing(10)
        
        # Вкладки с уроками
        self.tabs = QTabWidget()
        # self.tabs.setTabPosition(QTabWidget.West)
        
        # Создаем уроки
        self.tabs.addTab(self.create_lesson_if_else(), "Условия (if/else)")
        self.tabs.addTab(self.create_lesson_for(), "Циклы (for)")
        self.tabs.addTab(self.create_lesson_while(), "Циклы (while)")
        self.tabs.addTab(self.create_lesson_functions(), "Функции")
        self.tabs.addTab(self.create_lesson_lists(), "Списки")
        self.tabs.addTab(self.create_lesson_strings(), "Строки")
        
        self.addWidget(self.tabs)
    
    
    def create_lesson_if_else(self):
        """Урок про условные операторы"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Описание
        description = QLabel(
            "<h3>Условные операторы (if/else)</h3>"
            "<p>Используются для выполнения кода в зависимости от условия.</p>"
            "<p><b>Синтаксис:</b></p>"
            "<pre>if условие:\n    код если True\nelse:\n    код если False</pre>"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # IDE с примером
        ide = PythonEditorWidget()
        example_code = """# Пример: проверка четности числа
x = 10

if x % 2 == 0:
    print(f"{x} - четное число")
else:
    print(f"{x} - нечетное число")

# Пример: сравнение чисел
age = 25

if age < 18:
    print("Вы несовершеннолетний")
elif age >= 18 and age < 65:
    print("Вы совершеннолетний")
else:
    print("Вы пенсионер")"""
        
        ide.load_template(example_code)
        layout.addWidget(ide)
        
        return widget
    
    
    def create_lesson_for(self):
        """Урок про цикл for"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        description = QLabel(
            "<h3>Цикл for</h3>"
            "<p>Используется для повторения кода определенное количество раз.</p>"
            "<p><b>Синтаксис:</b></p>"
            "<pre>for i in range(начало, конец):\n    код который повторяется</pre>"
            "<p><b>range(n)</b> - от 0 до n-1</p>"
            "<p><b>range(start, end)</b> - от start до end-1</p>"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        ide = PythonEditorWidget()
        example_code = """# Пример 1: вывод чисел от 1 до 5
for i in range(1, 6):
    print(i)

# Пример 2: таблица умножения на 3
print("\\nТаблица умножения на 3:")
for i in range(1, 11):
    print(f"3 * {i} = {3 * i}")

# Пример 3: сумма чисел от 1 до 10
summa = 0
for i in range(1, 11):
    summa += i
print(f"\\nСумма чисел от 1 до 10: {summa}")

# Пример 4: перебор списка
fruits = ["яблоко", "груша", "апельсин"]
for fruit in fruits:
    print(f"Я люблю {fruit}")"""
        
        ide.load_template(example_code)
        layout.addWidget(ide)
        
        return widget
    
    
    def create_lesson_while(self):
        """Урок про цикл while"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        description = QLabel(
            "<h3>Цикл while</h3>"
            "<p>Повторяет код пока условие True.</p>"
            "<p><b>Синтаксис:</b></p>"
            "<pre>while условие:\n    код\n    изменение условия</pre>"
            "<p><b>Внимание:</b> не забудьте изменить условие, иначе бесконечный цикл!</p>"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        ide = PythonEditorWidget()
        example_code = """# Пример 1: отсчет
count = 5
while count > 0:
    print(count)
    count -= 1
print("Поехали!")

# Пример 2: угадай число
secret = 42
guess = None
attempts = 0

while guess != secret:
    guess = int(input("Угадайте число от 1 до 100: "))
    attempts += 1
    
    if guess < secret:
        print("Число больше")
    elif guess > secret:
        print("Число меньше")
    else:
        print(f"Верно! Вы угадали за {attempts} попыток")

# Пример 3: сумма до заданного числа
n = 0
while n < 100:
    n += 10
    print(n)"""
        
        ide.load_template(example_code)
        layout.addWidget(ide)
        
        return widget
    
    
    def create_lesson_functions(self):
        """Урок про функции"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        description = QLabel(
            "<h3>Функции</h3>"
            "<p>Функция - это блок кода, который можно использовать много раз.</p>"
            "<p><b>Синтаксис:</b></p>"
            "<pre>def имя_функции(параметры):\n    код\n    return результат</pre>"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        ide = PythonEditorWidget()
        example_code = """# Пример 1: функция без параметров
def greet():
    print("Привет, мир!")

greet()

# Пример 2: функция с параметрами
def greet_person(name):
    print(f"Привет, {name}!")

greet_person("Иван")
greet_person("Мария")

# Пример 3: функция с return
def add(a, b):
    return a + b

result = add(10, 20)
print(f"10 + 20 = {result}")

# Пример 4: функция с несколькими параметрами
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

print(f"Факториал 5 = {factorial(5)}")

# Пример 5: функция для проверки простого числа
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(f"17 - простое число: {is_prime(17)}")
print(f"15 - простое число: {is_prime(15)}")"""
        
        ide.load_template(example_code)
        layout.addWidget(ide)
        
        return widget
    
    
    def create_lesson_lists(self):
        """Урок про списки"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        description = QLabel(
            "<h3>Списки (Lists)</h3>"
            "<p>Список - упорядоченная коллекция элементов.</p>"
            "<p><b>Синтаксис:</b> list = [элемент1, элемент2, ...]</p>"
            "<p><b>Индексация:</b> начинается с 0</p>"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        ide = PythonEditorWidget()
        example_code = """# Пример 1: создание списка
numbers = [1, 2, 3, 4, 5]
print(numbers)

# Пример 2: доступ к элементам
print(f"Первый элемент: {numbers[0]}")
print(f"Последний элемент: {numbers[-1]}")

# Пример 3: срезы списков
print(f"Элементы с 1 до 3: {numbers[1:4]}")

# Пример 4: добавление элементов
numbers.append(6)
print(f"После append: {numbers}")

# Пример 5: удаление элементов
numbers.remove(3)
print(f"После remove(3): {numbers}")

# Пример 6: длина списка
print(f"Длина списка: {len(numbers)}")

# Пример 7: сумма и максимум
print(f"Сумма: {sum(numbers)}")
print(f"Максимум: {max(numbers)}")
print(f"Минимум: {min(numbers)}")

# Пример 8: сортировка
unsorted = [3, 1, 4, 1, 5, 9]
sorted_list = sorted(unsorted)
print(f"Отсортировано: {sorted_list}")

# Пример 9: перебор списка
fruits = ["яблоко", "груша", "банан"]
for fruit in fruits:
    print(f"Фрукт: {fruit}")"""
        
        ide.load_template(example_code)
        layout.addWidget(ide)
        
        return widget
    
    
    def create_lesson_strings(self):
        """Урок про строки"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        description = QLabel(
            "<h3>Строки (Strings)</h3>"
            "<p>Строка - последовательность символов.</p>"
            "<p><b>Создание:</b> 'строка' или \"строка\"</p>"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        ide = PythonEditorWidget()
        example_code = """# Пример 1: создание строк
text = "Привет, Python!"
print(text)

# Пример 2: длина строки
print(f"Длина: {len(text)}")

# Пример 3: доступ к символам
print(f"Первый символ: {text[0]}")
print(f"Последний символ: {text[-1]}")

# Пример 4: слайсы строк
print(f"Первые 7 символов: {text[:7]}")

# Пример 5: методы строк
print(f"Верхний регистр: {text.upper()}")
print(f"Нижний регистр: {text.lower()}")

# Пример 6: замена
new_text = text.replace("Python", "JavaScript")
print(f"После замены: {new_text}")

# Пример 7: разделение
words = text.split(", ")
print(f"Слова: {words}")

# Пример 8: объединение
joined = " - ".join(["Один", "Два", "Три"])
print(f"Объединено: {joined}")

# Пример 9: проверка подстроки
if "Python" in text:
    print("'Python' найден в тексте")

# Пример 10: форматирование строк
name = "Иван"
age = 25
print(f"Мне зовут {name}, мне {age} лет")
print("Мне зовут {}, мне {} лет".format(name, age))"""
        
        ide.load_template(example_code)
        layout.addWidget(ide)
        
        return widget
