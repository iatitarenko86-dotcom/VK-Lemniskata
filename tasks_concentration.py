# tasks_concentration.py
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from user_states import set_user_state, get_user_state, update_user_data
from simulator_concentration1 import SimulatorConcentration1
from simulator_concentration2 import SimulatorConcentration2
from simulator_concentration3 import SimulatorConcentration3
from simulator_concentration4 import SimulatorConcentration4

# Глобальный словарь для хранения тренажеров по пользователям
тренажеры_пользователей = {}


# ==================== ФУНКЦИИ ДЛЯ СОЗДАНИЯ КЛАВИАТУР ====================
def create_keyboard(buttons, one_time=False):
    """Создание клавиатуры VK с ограничением 4 кнопки в строке"""
    keyboard = VkKeyboard(one_time=one_time)

    MAX_BUTTONS_PER_ROW = 4

    for i, button in enumerate(buttons):
        if "Назад" in button or "В меню" in button or "К тренажеру" in button or "К примерам" in button or "К урокам" in button:
            color = VkKeyboardColor.SECONDARY
        elif button.startswith("🟢"):
            color = VkKeyboardColor.POSITIVE
        elif button.startswith("🔴"):
            color = VkKeyboardColor.NEGATIVE
        elif button.startswith("📖") or button.startswith("📝") or button.startswith("🎓"):
            color = VkKeyboardColor.PRIMARY
        else:
            color = VkKeyboardColor.PRIMARY

        keyboard.add_button(button, color=color)

        if (i + 1) % MAX_BUTTONS_PER_ROW == 0 and i < len(buttons) - 1:
            keyboard.add_line()

    return keyboard.get_keyboard()


def send_message(vk, user_id, text, keyboard=None):
    """Отправка сообщения"""
    try:
        if keyboard:
            vk.messages.send(
                user_id=user_id,
                message=text,
                random_id=random.randint(1, 2 ** 31),
                keyboard=keyboard
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message=text,
                random_id=random.randint(1, 2 ** 31)
            )
        return True
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return False


# ==================== ГЛАВНОЕ МЕНЮ КОНЦЕНТРАЦИИ ====================
def show_concentration_main_menu(vk, user_id):
    """Отображает главное меню задач на концентрацию"""
    keyboard = VkKeyboard()

    keyboard.add_button('📚 Справка', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📝 Примеры', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎓 Обучение', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🎯 Тренажер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)

    text = """🧪 Задачи на концентрацию смесей и сплавов

Выберите раздел для изучения:
• 📚 Справка - формулы и теория
• 📝 Примеры - готовые решения
• 🎓 Обучение - пошаговое изучение
• 🎯 Тренажер - практические задания"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'main_menu')


def start_concentration_tasks(vk, user_id, user_data):
    """Начинает работу с задачами на концентрацию"""
    show_concentration_main_menu(vk, user_id)


# ==================== МЕНЮ ТРЕНАЖЕРА ====================
def show_simulator_menu(vk, user_id):
    """Отображает меню тренажера"""
    keyboard = VkKeyboard()

    keyboard.add_button('🟢 Легкий', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('🟡 Средний', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔴 Сложный', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('🎲 Случайно', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к меню концентрации', color=VkKeyboardColor.SECONDARY)

    text = """🎯 Тренажер: Задачи на концентрацию

Выберите уровень сложности:
• 🟢 Легкий - базовые задачи на смешивание
• 🟡 Средний - задачи с системой уравнений
• 🔴 Сложный - задачи на сплавы и высушивание
• 🎲 Случайно - задача любого уровня"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'simulator_menu')


# ==================== МЕНЮ ПРИМЕРОВ ====================
def show_examples_menu(vk, user_id):
    """Меню примеров"""
    keyboard = VkKeyboard()

    keyboard.add_button('📖 Пример 1: Смешивание растворов', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 2: Система уравнений', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 3: Сплав латуни', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 4: Высушивание', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Пример 5: Два сплава', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 6: Правило креста', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к меню концентрации', color=VkKeyboardColor.SECONDARY)

    text = "📝 Выберите пример для изучения:\n\nКаждый пример содержит:\n• Таблицу данных\n• Развернутое решение\n• Пояснения к каждому шагу\n• Рекомендации по решению"

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'examples_menu')


# ==================== МЕНЮ ОБУЧЕНИЯ ====================
def show_training_menu(vk, user_id):
    """Меню обучения"""
    keyboard = VkKeyboard()

    keyboard.add_button('📖 Урок 1', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 2', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 3', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к меню концентрации', color=VkKeyboardColor.SECONDARY)

    text = "🎓 Выберите урок:"
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'training_menu')


# ==================== ЗАПУСК УРОВНЕЙ ТРЕНАЖЕРА ====================
def start_easy_simulator(vk, user_id):
    """Запускает легкий уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorConcentration1()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorConcentration1):
                тренажеры_пользователей[user_id] = SimulatorConcentration1()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'легкий'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🟢 Легкий уровень\n\n{задача}\n\nВведите ответ:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'concentration_tasks', 'easy_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


def start_medium_simulator(vk, user_id):
    """Запускает средний уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorConcentration2()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorConcentration2):
                тренажеры_пользователей[user_id] = SimulatorConcentration2()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'средний'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🟡 Средний уровень\n\n{задача}\n\nВведите ответ:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'concentration_tasks', 'medium_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


def start_hard_simulator(vk, user_id):
    """Запускает сложный уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorConcentration3()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorConcentration3):
                тренажеры_пользователей[user_id] = SimulatorConcentration3()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'сложный'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🔴 Сложный уровень\n\n{задача}\n\nВведите ответ:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'concentration_tasks', 'hard_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


def start_random_simulator(vk, user_id):
    """Запускает режим случайных задач"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorConcentration4()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorConcentration4):
                тренажеры_пользователей[user_id] = SimulatorConcentration4()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'случайные'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🎲 Случайная задача\n\n{задача}\n\nВведите ответ:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'concentration_tasks', 'random_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


# ==================== ПРИМЕРЫ ЗАДАЧ (ТАБЛИЦЫ БЕЗ РАМОК - ПРОБЕЛЫ И ДЕФИСЫ) ====================
def send_example_1(vk, user_id):
    text = """🧪 Пример 1: Смешивание растворов

📋 УСЛОВИЕ ЗАДАЧИ
Смешали 8 литров 15% раствора соли и 12 литров 25% раствора соли.
Найдите концентрацию полученного раствора.

📊 ТАБЛИЦА ДАННЫХ

Параметр               1-й р-р   2-й р-р   Смесь
────────────────────────────────────────────────
Масса (л)                 8         12       20
Концентрация (%)         15         25        ?
Масса вещества (л)       1,2        3       4,2

🔍 РАЗВЕРНУТОЕ РЕШЕНИЕ

1️⃣ Находим массу соли в первом растворе:
   m₁ = 8 × 0,15 = 1,2 л

2️⃣ Находим массу соли во втором растворе:
   m₂ = 12 × 0,25 = 3 л

3️⃣ Находим общую массу соли:
   m = 1,2 + 3 = 4,2 л

4️⃣ Находим общий объем смеси:
   V = 8 + 12 = 20 л

5️⃣ Находим концентрацию:
   c = (4,2 / 20) × 100% = 21%

✅ ОТВЕТ: 21%

💡 РЕКОМЕНДАЦИИ
• При смешивании концентрация всегда между исходными (15% < 21% < 25%)
• Формула: c = (m₁·c₁ + m₂·c₂) / (m₁ + m₂)
• Не забывайте переводить проценты в десятичные дроби"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_2(vk, user_id):
    text = """⚗️ Пример 2: Система уравнений

📋 УСЛОВИЕ ЗАДАЧИ
Смешали 30% и 10% растворы соляной кислоты и получили 600 г 15% раствора. Сколько граммов каждого раствора взяли?

📊 ТАБЛИЦА ДАННЫХ

Параметр                30% р-р   10% р-р   Смесь
────────────────────────────────────────────────
Масса (г)                 x         y       600
Концентрация (%)         30        10       15
Масса вещества (г)       0,3x      0,1y      90

🔍 РАЗВЕРНУТОЕ РЕШЕНИЕ

1️⃣ Составляем систему:
   x + y = 600
   0,3x + 0,1y = 90

2️⃣ Из первого: y = 600 - x

3️⃣ Подставляем:
   0,3x + 0,1(600 - x) = 90
   0,3x + 60 - 0,1x = 90
   0,2x + 60 = 90
   0,2x = 30
   x = 150

4️⃣ Находим y:
   y = 600 - 150 = 450

✅ ОТВЕТ
30% раствора: 150 г
10% раствора: 450 г

💡 РЕКОМЕНДАЦИИ
• Всегда обозначайте неизвестные переменные
• Проверка: 150×0,3 + 450×0,1 = 45 + 45 = 90 г вещества"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_3(vk, user_id):
    text = """🏺 Пример 3: Сплав латуни

📋 УСЛОВИЕ ЗАДАЧИ
В сплаве латуни меди на 11 кг больше, чем цинка. После добавления 12 кг меди концентрация меди стала 75%. Сколько кг меди было первоначально?

📊 ТАБЛИЦА ДАННЫХ

Параметр               Было    Добавили    Стало
────────────────────────────────────────────────
Масса меди (кг)         x         12       x+12
Масса цинка (кг)        y          0         y
Общая масса (кг)       x+y        12       x+y+12

Дано: x = y + 11

🔍 РАЗВЕРНУТОЕ РЕШЕНИЕ

1️⃣ Выражаем y: y = x - 11

2️⃣ Уравнение концентрации:
   (x + 12) / (2x + 1) = 0,75

3️⃣ Умножаем:
   x + 12 = 0,75(2x + 1)
   x + 12 = 1,5x + 0,75

4️⃣ Решаем:
   -0,5x + 11,25 = 0
   x = 22,5

✅ ОТВЕТ: 22,5 кг меди

💡 РЕКОМЕНДАЦИИ
• В задачах на сплавы те же формулы, что и для растворов
• После добавления вещества общая масса увеличивается
• Проверка: было 22,5 кг меди, 11,5 кг цинка, всего 34 кг
  После: меди 34,5 кг, всего 46 кг, 34,5/46 = 75% ✓"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_4(vk, user_id):
    text = """🍎 Пример 4: Высушивание фруктов

📋 УСЛОВИЕ ЗАДАЧИ
Свежие фрукты содержат 80% воды, сушеные - 28% воды. Сколько кг сушеных фруктов получится из 288 кг свежих?

📊 ТАБЛИЦА ДАННЫХ

Параметр                 Свежие    Сушеные
──────────────────────────────────────────
Масса (кг)                288         x
Содержание воды (%)        80         28
Сухое вещество (%)         20         72

Важно! Масса сухого вещества НЕ ИЗМЕНЯЕТСЯ!

🔍 РАЗВЕРНУТОЕ РЕШЕНИЕ

1️⃣ Масса сухого вещества в свежих:
   Сухое = 100% - 80% = 20%
   m_сух = 288 × 0,2 = 57,6 кг

2️⃣ В сушеных сухое вещество:
   100% - 28% = 72%

3️⃣ Находим массу сушеных:
   0,72 × x = 57,6
   x = 57,6 / 0,72 = 80 кг

✅ ОТВЕТ: 80 кг

💡 РЕКОМЕНДАЦИИ
• При высушивании меняется только содержание воды
• Масса сухого вещества постоянна
• Формула: m₁×(100%-w₁) = m₂×(100%-w₂)
• Проверка: 288×0,2 = 80×0,72 = 57,6 кг сухого вещества ✓"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_5(vk, user_id):
    text = """📊 Пример 5: Два сплава

📋 УСЛОВИЕ ЗАДАЧИ
Имеется два сплава меди с цинком. Первый содержит 10% меди, второй - 40% меди. Масса второго на 3 кг больше первого. После сплавления получили сплав с 30% меди. Найдите массу третьего сплава.

📊 ТАБЛИЦА ДАННЫХ

Параметр               Сплав 1    Сплав 2    Сплав 3
────────────────────────────────────────────────────
Масса (кг)               x         x+3        2x+3
Концентрация (%)         10         40         30
Масса меди (кг)         0,1x      0,4(x+3)   0,3(2x+3)

🔍 РАЗВЕРНУТОЕ РЕШЕНИЕ

1️⃣ Уравнение по массе меди:
   0,1x + 0,4(x + 3) = 0,3(2x + 3)

2️⃣ Раскрываем скобки:
   0,1x + 0,4x + 1,2 = 0,6x + 0,9
   0,5x + 1,2 = 0,6x + 0,9

3️⃣ Переносим:
   0,5x - 0,6x = 0,9 - 1,2
   -0,1x = -0,3
   x = 3

4️⃣ Масса третьего сплава:
   m₃ = 2×3 + 3 = 9 кг

✅ ОТВЕТ: 9 кг

💡 РЕКОМЕНДАЦИИ
• Выражайте все неизвестные через одну переменную
• Составляйте уравнение по массе чистого вещества
• Проверка: 3×0,1 + 6×0,4 = 0,3 + 2,4 = 2,7 кг меди
  9×0,3 = 2,7 кг меди ✓"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_6(vk, user_id):
    text = """📐 Пример 6: Правило креста

📋 УСЛОВИЕ ЗАДАЧИ
Смешали 30% и 10% растворы соли и получили 600 г 15% раствора. Сколько граммов каждого взяли? (Решение по правилу креста)

📊 ПРАВИЛО КРЕСТА

Диагональная схема:

      30%                   5 частей (15-10=5)
         \                 /
          15%
         /                 \
      10%                   15 частей (30-15=15)

Соотношение: 30% : 10% = 5 : 15 = 1 : 3

🔍 РАЗВЕРНУТОЕ РЕШЕНИЕ

1️⃣ Вычисляем разности:
   |15 - 10| = 5 (частей 30% раствора)
   |30 - 15| = 15 (частей 10% раствора)

2️⃣ Соотношение: 1 : 3

3️⃣ Всего частей: 1 + 3 = 4

4️⃣ Масса одной части: 600 ÷ 4 = 150 г

5️⃣ Массы растворов:
   30%: 1 × 150 = 150 г
   10%: 3 × 150 = 450 г

✅ ОТВЕТ
30% раствора: 150 г
10% раствора: 450 г

💡 РЕКОМЕНДАЦИИ
• Правило креста работает только для двух компонентов
• Формула: a : b = |c - b| : |a - c|
• Проверка: 150×0,3 + 450×0,1 = 45 + 45 = 90 г
  600×0,15 = 90 г ✓"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


# ==================== УРОКИ ====================
def send_lesson(vk, user_id, lesson_num):
    """Отправляет урок"""
    lessons = {
        1: """📖 Урок 1: Основные понятия

🔤 ОСНОВНЫЕ ОПРЕДЕЛЕНИЯ

Концентрация - это отношение массы растворенного вещества к массе раствора, выраженное в процентах.

Формула: c = (m_вещества / m_раствора) × 100%

📐 ОСНОВНЫЕ ФОРМУЛЫ

1) Нахождение массы вещества:
   m_вещества = m_раствора × c / 100%

2) Нахождение массы раствора:
   m_раствора = m_вещества × 100% / c

3) Закон сохранения массы:
   m₁·c₁ + m₂·c₂ = (m₁ + m₂)·c

💡 ПРИМЕР
Найти массу соли в 200 г 15% раствора.

Решение:
m = 200 × 15% / 100% = 200 × 0,15 = 30 г

Ответ: 30 г соли""",

        2: """📖 Урок 2: Смешивание растворов

📐 АЛГОРИТМ РЕШЕНИЯ

1. Найти массу вещества в каждом растворе
2. Сложить массы веществ
3. Сложить массы растворов
4. Разделить массу вещества на массу смеси и умножить на 100%

📊 ПРИМЕР
Смешали 300 г 20% и 200 г 30% растворов. Найти концентрацию смеси.

Решение:
m₁ = 300 × 0,2 = 60 г
m₂ = 200 × 0,3 = 60 г
m = 60 + 60 = 120 г
M = 300 + 200 = 500 г
c = (120 / 500) × 100% = 24%

Ответ: 24%""",

        3: """📖 Урок 3: Сплавы и высушивание

🏺 СПЛАВЫ
Задачи на сплавы решаются так же, как и на растворы.
Вместо вещества - металл, вместо раствора - сплав.

🍎 ВЫСУШИВАНИЕ
При высушивании:
• Масса сухого вещества НЕ ИЗМЕНЯЕТСЯ!
• Изменяется только содержание воды

Формула: m₁ × (100% - w₁) = m₂ × (100% - w₂)

💡 ПРИМЕР
Свежие грибы содержат 90% воды, сушеные - 12% воды.
Сколько сушеных грибов получится из 22 кг свежих?

Решение:
Сухого вещества в свежих: 22 × 0,1 = 2,2 кг
В сушеных сухого: 100% - 12% = 88%
Масса сушеных: 2,2 / 0,88 = 2,5 кг

Ответ: 2,5 кг"""
    }

    text = lessons.get(lesson_num, lessons[1])

    keyboard = VkKeyboard()
    keyboard.add_button('⬅️ Назад', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('➡️ Далее', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к урокам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_lesson')
    update_user_data(user_id, {'current_lesson': lesson_num})


# ==================== СПРАВОЧНЫЙ МАТЕРИАЛ ====================
def send_reference_material(vk, user_id):
    """Отправляет справочный материал"""
    text = """📚 Справочный материал по задачам на концентрацию

📐 ОСНОВНЫЕ ФОРМУЛЫ

1) Концентрация = (m_вещества / m_раствора) × 100%

2) m_вещества = m_раствора × c / 100%

3) При смешивании: m₁·c₁ + m₂·c₂ = (m₁ + m₂)·c

4) При высушивании: m₁·(100%-w₁) = m₂·(100%-w₂)

📊 ПРАВИЛО КРЕСТА

      a                    |c - b|
        \                 /
          c
        /                 \
      b                    |a - c|

Соотношение a : b = |c - b| : |a - c|

🔍 АЛГОРИТМ РЕШЕНИЯ

1. Определить, что дано и что нужно найти
2. Записать данные в виде таблицы
3. Составить уравнение на основе закона сохранения
4. Решить уравнение
5. Проверить ответ на реалистичность

📋 ТИПЫ ЗАДАЧ

1. Смешивание двух растворов
2. Смешивание трех и более растворов
3. Задачи на сплавы
4. Задачи на высушивание
5. Задачи с добавлением чистого вещества или воды
6. Задачи с переливанием
7. Задачи с процентным содержанием"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к меню концентрации', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'reference')


# ==================== ОБЩИЕ ФУНКЦИИ ДЛЯ ТРЕНАЖЕРА ====================
def handle_simulator_input(vk, user_id, user_input, уровень):
    """Обрабатывает ввод ответа в тренажере"""
    try:
        if user_id not in тренажеры_пользователей:
            send_message(vk, user_id, "❌ Тренажер не инициализирован. Начните заново.")
            show_simulator_menu(vk, user_id)
            return

        тренажер = тренажеры_пользователей[user_id]
        успех, сообщение = тренажер.проверить_ответ(user_input)

        уровень_данные = {
            'легкий': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
            'средний': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
            'сложный': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'},
            'случайные': {'эмодзи': '🎲', 'текст': 'Случайная задача'}
        }

        данные_уровня = уровень_данные.get(уровень, {'эмодзи': '🧪', 'текст': 'Тренажер'})

        keyboard = VkKeyboard()

        if уровень == 'случайные':
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
        else:
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        if успех:
            if "Следующая задача" in сообщение or "следующая" in сообщение.lower():
                new_task = тренажер.получить_текущую_задачу()
                send_message(vk, user_id, f"✅ Верно!\n\n{new_task}\n\nВведите ответ:", keyboard.get_keyboard())
            else:
                final_keyboard = VkKeyboard()
                final_keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
                send_message(vk, user_id, сообщение, final_keyboard.get_keyboard())
        else:
            task = тренажер.получить_текущую_задачу()
            send_message(vk, user_id, f"{сообщение}\n\n{task}\n\nВведите ответ:", keyboard.get_keyboard())
    except Exception as e:
        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
        send_message(vk, user_id, f"❌ Ошибка при проверке ответа: {str(e)}\n\nПопробуйте еще раз:",
                     keyboard.get_keyboard())


def send_simulator_hint(vk, user_id):
    """Отправляет подсказку для тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            send_message(vk, user_id, "❌ Тренажер не инициализирован.")
            return

        тренажер = тренажеры_пользователей[user_id]
        подсказка = тренажер.получить_подсказку()

        user_state = get_user_state(user_id)
        submodule = user_state.get('sub_module', '')

        keyboard = VkKeyboard()

        if submodule == 'random_simulator':
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
        else:
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id, подсказка, keyboard.get_keyboard())
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при получении подсказки: {str(e)}")


def show_simulator_answer(vk, user_id):
    """Показывает ответ для тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            send_message(vk, user_id, "❌ Тренажер не инициализирован.")
            return

        тренажер = тренажеры_пользователей[user_id]
        ответ = тренажер.показать_ответ()

        user_state = get_user_state(user_id)
        submodule = user_state.get('sub_module', '')

        if submodule == 'random_simulator':
            keyboard = VkKeyboard()
            keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, f"🎲 Случайная задача\n\n{ответ}\n\nНажмите 'Новая задача' для продолжения:",
                         keyboard.get_keyboard())
        else:
            уровень_данные = {
                'easy_simulator': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
                'medium_simulator': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
                'hard_simulator': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'}
            }
            данные_уровня = уровень_данные.get(submodule, {'эмодзи': '🧪', 'текст': 'Тренажер'})
            keyboard = VkKeyboard()
            keyboard.add_button('➡️ Следующая задача', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id,
                         f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n{ответ}\n\nНажмите 'Следующая задача' для продолжения:",
                         keyboard.get_keyboard())
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при показе ответа: {str(e)}")


def next_simulator_task(vk, user_id):
    """Переходит к следующей задаче в тренажере"""
    try:
        if user_id not in тренажеры_пользователей:
            send_message(vk, user_id, "❌ Тренажер не инициализирован.")
            return

        тренажер = тренажеры_пользователей[user_id]
        user_state = get_user_state(user_id)
        submodule = user_state.get('sub_module', '')

        if submodule == 'random_simulator':
            задача = тренажер.получить_следующую_задачу()
            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, f"🎲 Случайная задача\n\n{задача}\n\nВведите ответ:", keyboard.get_keyboard())
        else:
            if hasattr(тренажер, 'текущая_задача'):
                тренажер.текущая_задача += 1
            задача = тренажер.получить_текущую_задачу()
            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            уровень_данные = {
                'easy_simulator': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
                'medium_simulator': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
                'hard_simulator': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'}
            }
            данные_уровня = уровень_данные.get(submodule, {'эмодзи': '🧪', 'текст': 'Тренажер'})
            send_message(vk, user_id,
                         f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n{задача}\n\nВведите ответ:",
                         keyboard.get_keyboard())
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при переходе к следующей задаче: {str(e)}")


# ==================== ОСНОВНОЙ ОБРАБОТЧИК ====================
def handle_concentration_tasks(vk, user_id, text, user_data):
    """Обрабатывает сообщения в модуле задач на концентрацию"""
    user_state = get_user_state(user_id)
    current_submodule = user_state.get('sub_module', '')

    # ========== ОБРАБОТКА КНОПОК НАЗАД ==========
    if text == '🔙 Назад к типам задач':
        from main import show_text_tasks_menu
        show_text_tasks_menu(user_id)
        return

    if text == '🔙 Назад к меню концентрации':
        show_concentration_main_menu(vk, user_id)
        return

    if text == '🔙 Назад к тренажеру':
        show_simulator_menu(vk, user_id)
        return

    if text == '🔙 Назад':
        if current_submodule == 'viewing_example':
            show_examples_menu(vk, user_id)
        elif current_submodule == 'viewing_lesson':
            show_training_menu(vk, user_id)
        elif current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
            show_simulator_menu(vk, user_id)
        else:
            from main import show_text_tasks_menu
            show_text_tasks_menu(user_id)
        return

    # ========== ОБРАБОТКА ВОЗВРАТА ИЗ ПРИМЕРОВ И УРОКОВ ==========
    if text == '🔙 Назад к примерам':
        show_examples_menu(vk, user_id)
        return

    if text == '🔙 К примерам':
        show_examples_menu(vk, user_id)
        return

    if text == '🔙 Назад к урокам':
        show_training_menu(vk, user_id)
        return

    if text == '🔙 К урокам':
        show_training_menu(vk, user_id)
        return

    if text == '🔙 К тренажеру':
        show_simulator_menu(vk, user_id)
        return

    # ========== ОБРАБОТКА ВВОДА ОТВЕТА В ТРЕНАЖЕРЕ ==========
    if current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
        system_buttons = [
            '💡 Подсказка', '📝 Ответ', '🔙 Назад', '➡️ Далее',
            '🔄 Новая', '📚 Справка', '📝 Примеры', '🎓 Обучение',
            '🎯 Тренажер', '🟢 Легкий', '🟡 Средний', '🔴 Сложный',
            '🎲 Случайно', '🔙 В меню', '🔙 К примерам', '🔙 К урокам',
            '🔙 Назад к тренажеру', '🔙 Назад к меню концентрации', '🔙 Назад к типам задач',
            '📖 Пример 1: Смешивание растворов', '📖 Пример 2: Система уравнений', 
            '📖 Пример 3: Сплав латуни', '📖 Пример 4: Высушивание', 
            '📖 Пример 5: Два сплава', '📖 Пример 6: Правило креста',
            '📖 Урок 1', '📖 Урок 2', '📖 Урок 3', '⬅️ Назад', '➡️ Далее'
        ]

        if text not in system_buttons:
            level_map = {
                'easy_simulator': 'легкий',
                'medium_simulator': 'средний',
                'hard_simulator': 'сложный',
                'random_simulator': 'случайные'
            }
            level = level_map.get(current_submodule, 'легкий')

            if user_id in тренажеры_пользователей:
                тренажер = тренажеры_пользователей[user_id]
                success, message = тренажер.проверить_ответ(text)

                keyboard = VkKeyboard()
                if current_submodule == 'random_simulator':
                    keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
                else:
                    keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_line()
                    keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

                if success:
                    if "Следующая задача" in message or "следующая" in message.lower():
                        new_task = тренажер.получить_текущую_задачу()
                        send_message(vk, user_id, f"✅ Верно!\n\n{new_task}\n\nВведите ответ:", keyboard.get_keyboard())
                    else:
                        final_keyboard = VkKeyboard()
                        final_keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
                        send_message(vk, user_id, message, final_keyboard.get_keyboard())
                else:
                    task = тренажер.получить_текущую_задачу()
                    send_message(vk, user_id, f"{message}\n\n{task}\n\nВведите ответ:", keyboard.get_keyboard())
            return

    # ========== ОСНОВНОЕ МЕНЮ ==========
    if text == '📚 Справка':
        send_reference_material(vk, user_id)
        return
    elif text == '📝 Примеры':
        show_examples_menu(vk, user_id)
        return
    elif text == '🎓 Обучение':
        show_training_menu(vk, user_id)
        return
    elif text == '🎯 Тренажер':
        show_simulator_menu(vk, user_id)
        return

    # ========== ВЫБОР ПРИМЕРОВ ==========
    elif text == '📖 Пример 1: Смешивание растворов':
        send_example_1(vk, user_id)
        return
    elif text == '📖 Пример 2: Система уравнений':
        send_example_2(vk, user_id)
        return
    elif text == '📖 Пример 3: Сплав латуни':
        send_example_3(vk, user_id)
        return
    elif text == '📖 Пример 4: Высушивание':
        send_example_4(vk, user_id)
        return
    elif text == '📖 Пример 5: Два сплава':
        send_example_5(vk, user_id)
        return
    elif text == '📖 Пример 6: Правило креста':
        send_example_6(vk, user_id)
        return

    # ========== ВЫБОР УРОКОВ ==========
    elif text == '📖 Урок 1':
        send_lesson(vk, user_id, 1)
        return
    elif text == '📖 Урок 2':
        send_lesson(vk, user_id, 2)
        return
    elif text == '📖 Урок 3':
        send_lesson(vk, user_id, 3)
        return

    # ========== ВЫБОР УРОВНЯ ТРЕНАЖЕРА ==========
    elif text == '🟢 Легкий':
        start_easy_simulator(vk, user_id)
        return
    elif text == '🟡 Средний':
        start_medium_simulator(vk, user_id)
        return
    elif text == '🔴 Сложный':
        start_hard_simulator(vk, user_id)
        return
    elif text == '🎲 Случайно':
        start_random_simulator(vk, user_id)
        return

    # ========== КНОПКИ УПРАВЛЕНИЯ ТРЕНАЖЕРОМ ==========
    elif text == '💡 Подсказка' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
        if user_id in тренажеры_пользователей:
            hint = тренажеры_пользователей[user_id].получить_подсказку()
            keyboard = VkKeyboard()
            if current_submodule == 'random_simulator':
                keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            else:
                keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, hint, keyboard.get_keyboard())
        return

    elif text == '📝 Ответ' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
        if user_id in тренажеры_пользователей:
            answer = тренажеры_пользователей[user_id].показать_ответ()
            keyboard = VkKeyboard()
            if current_submodule == 'random_simulator':
                keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            else:
                keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, answer, keyboard.get_keyboard())
        return

    elif text == '🔄 Новая' and current_submodule == 'random_simulator':
        if user_id in тренажеры_пользователей:
            new_task = тренажеры_пользователей[user_id].получить_следующую_задачу()
            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, f"🎲 Новая задача\n\n{new_task}\n\nВведите ответ:", keyboard.get_keyboard())
        return

    elif text == '➡️ Далее' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator']:
        if user_id in тренажеры_пользователей:
            next_task = тренажеры_пользователей[user_id].получить_текущую_задачу()
            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, f"Следующая задача:\n\n{next_task}\n\nВведите ответ:", keyboard.get_keyboard())
        return

    # ========== НАВИГАЦИЯ В УРОКАХ ==========
    elif text == '⬅️ Назад' and current_submodule == 'viewing_lesson':
        current_lesson = user_state.get('current_lesson', 1)
        prev_lesson = current_lesson - 1 if current_lesson > 1 else 3
        send_lesson(vk, user_id, prev_lesson)
        return

    elif text == '➡️ Далее' and current_submodule == 'viewing_lesson':
        current_lesson = user_state.get('current_lesson', 1)
        next_lesson = current_lesson + 1 if current_lesson < 3 else 1
        send_lesson(vk, user_id, next_lesson)
        return

    else:
        show_concentration_main_menu(vk, user_id)
        return
