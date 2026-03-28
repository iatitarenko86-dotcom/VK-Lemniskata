# tasks_percentage.py
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from user_states import set_user_state, get_user_state, update_user_data
from simulator_percentage1 import SimulatorPercentage1
from simulator_percentage2 import SimulatorPercentage2
from simulator_percentage3 import SimulatorPercentage3
from simulator_percentage4 import SimulatorPercentage4

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


# ==================== ГЛАВНОЕ МЕНЮ ПРОЦЕНТОВ ====================
def show_percentage_main_menu(vk, user_id):
    """Отображает главное меню задач на проценты"""
    keyboard = VkKeyboard()

    keyboard.add_button('📚 Справка', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📝 Примеры', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎓 Обучение', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🎯 Тренажер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)

    text = """📊 Задачи на проценты

Выберите раздел для изучения:
• 📚 Справка - формулы и теория
• 📝 Примеры - готовые решения
• 🎓 Обучение - пошаговое изучение
• 🎯 Тренажер - практические задания"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'main_menu')


def start_percentage_tasks(vk, user_id, user_data):
    """Начинает работу с задачами на проценты"""
    show_percentage_main_menu(vk, user_id)


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
    keyboard.add_button('🔙 Назад к меню процентов', color=VkKeyboardColor.SECONDARY)

    text = """🎯 Тренажер: Задачи на проценты

Выберите уровень сложности:
• 🟢 Легкий - базовые задачи
• 🟡 Средний - задачи средней сложности
• 🔴 Сложный - комплексные задачи
• 🎲 Случайно - задача любого уровня"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'simulator_menu')


# ==================== МЕНЮ ПРИМЕРОВ ====================
def show_examples_menu(vk, user_id):
    """Меню примеров"""
    keyboard = VkKeyboard()

    keyboard.add_button('📖 Пример 1', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 2', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 3', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 4', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Пример 5', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🔙 Назад к меню процентов', color=VkKeyboardColor.SECONDARY)

    text = "📝 Выберите пример:"
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'examples_menu')


# ==================== МЕНЮ ОБУЧЕНИЯ ====================
def show_training_menu(vk, user_id):
    """Меню обучения"""
    keyboard = VkKeyboard()

    keyboard.add_button('📖 Урок 1', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 2', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 3', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к меню процентов', color=VkKeyboardColor.SECONDARY)

    text = "🎓 Выберите урок:"
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'training_menu')


# ==================== ЗАПУСК УРОВНЕЙ ТРЕНАЖЕРА ====================
def start_easy_simulator(vk, user_id):
    """Запускает легкий уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorPercentage1()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorPercentage1):
                тренажеры_пользователей[user_id] = SimulatorPercentage1()

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

        set_user_state(user_id, 'percentage_tasks', 'easy_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


def start_medium_simulator(vk, user_id):
    """Запускает средний уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorPercentage2()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorPercentage2):
                тренажеры_пользователей[user_id] = SimulatorPercentage2()

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

        set_user_state(user_id, 'percentage_tasks', 'medium_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


def start_hard_simulator(vk, user_id):
    """Запускает сложный уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorPercentage3()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorPercentage3):
                тренажеры_пользователей[user_id] = SimulatorPercentage3()

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

        set_user_state(user_id, 'percentage_tasks', 'hard_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


def start_random_simulator(vk, user_id):
    """Запускает режим случайных задач"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorPercentage4()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorPercentage4):
                тренажеры_пользователей[user_id] = SimulatorPercentage4()

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

        set_user_state(user_id, 'percentage_tasks', 'random_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка: {str(e)}")
        show_simulator_menu(vk, user_id)


# ==================== ПРИМЕРЫ ЗАДАЧ (ПОЛНЫЕ ВЕРСИИ) ====================
def send_example_1(vk, user_id):
    text = """📱 Пример 1: Скидка на телефон

Условие: Телефон стоил 5000 руб, стал 3000 руб. На сколько % снизилась цена?

Решение:
Снижение: 5000 - 3000 = 2000 руб
Процент: 2000 / 5000 × 100% = 40%

Ответ: 40%"""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'viewing_example')


def send_example_2(vk, user_id):
    text = """🧈 Пример 2: Скидка пенсионерам

Условие: Масло стоит 60 руб, скидка 5%. Сколько стоит для пенсионера?

Решение:
Скидка: 60 × 5% = 3 руб
Цена: 60 - 3 = 57 руб
Или: 60 × 0,95 = 57 руб

Ответ: 57 руб"""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'viewing_example')


def send_example_3(vk, user_id):
    text = """📚 Пример 3: Двойное снижение

Условие: Книга стоила 120 руб. Сначала снизили на 10%, затем на 5%. Новая цена?

Решение:
1-е снижение: 120 × 0,9 = 108 руб
2-е снижение: 108 × 0,95 = 102,6 руб
Или: 120 × 0,9 × 0,95 = 102,6 руб

Ответ: 102,6 руб"""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'viewing_example')


def send_example_4(vk, user_id):
    text = """💰 Пример 4: Налог на доходы

Условие: После вычета 13% налога получено 9570 руб. Найдите зарплату.

Решение:
Получено: 100% - 13% = 87% от зарплаты
Зарплата: 9570 / 0,87 = 11000 руб

Ответ: 11000 руб"""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'viewing_example')


def send_example_5(vk, user_id):
    text = """🌳 Пример 5: Деревья в парке

Условие: 25% - березы, 1/3 - клены, дубов на 24 больше кленов, остальные 46 - липы. Сколько всего деревьев?

Решение:
Пусть X - всего
0,25X + X/3 + (X/3 + 24) + 46 = X
X/4 + 2X/3 + 70 = X
3X + 8X + 840 = 12X
X = 840

Ответ: 840 деревьев"""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'viewing_example')


# ==================== УРОКИ (ПОЛНЫЕ ВЕРСИИ) ====================
def send_lesson(vk, user_id, lesson_num):
    """Отправляет урок"""
    lessons = {
        1: """📖 Урок 1: Основные формулы

Основные формулы процентов:
1. p% от A = A × p / 100
2. Если p% числа равны B, то A = B × 100 / p
3. Сколько процентов B составляет от A: (B / A) × 100%

Примеры:
1) Найти 8% от 50: 50 × 8 / 100 = 4
2) Найти число, если 12% от него равны 36: 36 × 100 / 12 = 300
3) Найти, сколько процентов 15 составляет от 60: (15 / 60) × 100% = 25%""",

        2: """📖 Урок 2: Изменение величины

Формулы изменения величины:
• Увеличение на p%: A × (1 + p/100)
• Уменьшение на p%: A × (1 - p/100)

Примеры:
1) Увеличить 200 на 15%: 200 × 1,15 = 230
2) Уменьшить 200 на 15%: 200 × 0,85 = 170

Последовательные изменения:
A × (1 ± p/100) × (1 ± q/100)

Пример: Цену 1000 руб сначала повысили на 10%, затем понизили на 10%.
Конечная цена: 1000 × 1,1 × 0,9 = 990 руб""",

        3: """📖 Урок 3: Сложные проценты

Формула сложных процентов:
A = P × (1 + r/n)^(n×t)

где:
P - начальная сумма
r - годовая процентная ставка (в десятичных)
n - количество начислений в год
t - количество лет
A - конечная сумма

Пример: Банковский вклад 10000 руб под 10% годовых на 2 года с ежегодной капитализацией.
A = 10000 × (1 + 0,1)^2 = 10000 × 1,21 = 12100 руб

Задачи на концентрацию:
Концентрация = (масса вещества / масса раствора) × 100%

Пример: Смешали 200 г 10% и 300 г 20% растворов.
Концентрация = (200×0,1 + 300×0,2) / 500 × 100% = (20 + 60) / 500 × 100% = 16%"""
    }

    text = lessons.get(lesson_num, lessons[1])

    keyboard = VkKeyboard()
    keyboard.add_button('⬅️ Назад', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('➡️ Далее', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к урокам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'viewing_lesson')
    update_user_data(user_id, {'current_lesson': lesson_num})


# ==================== СПРАВОЧНЫЙ МАТЕРИАЛ ====================
def send_reference_material(vk, user_id):
    """Отправляет справочный материал"""
    text = """📚 Справочный материал по задачам на проценты

Основные формулы:
• p% от A = A × p / 100
• Число по проценту: A = B × 100 / p
• Процентное отношение: (B / A) × 100%

Изменение величины:
• Увеличение на p%: A × (1 + p/100)
• Уменьшение на p%: A × (1 - p/100)
• Последовательные изменения: A × (1 ± p/100) × (1 ± q/100)

Сложные проценты:
A = P × (1 + r/n)^(n×t)

Типы задач:
1. Нахождение процента от числа
2. Нахождение числа по его проценту
3. Нахождение процентного отношения
4. Изменение величины на проценты
5. Сложные проценты
6. Задачи на концентрацию и смеси

Алгоритм решения:
1. Определить, что дано и что нужно найти
2. Записать данные в виде пропорции
3. Составить уравнение
4. Решить уравнение
5. Проверить ответ на реалистичность"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к меню процентов', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'reference')


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

        данные_уровня = уровень_данные.get(уровень, {'эмодзи': '📊', 'текст': 'Тренажер'})

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
            данные_уровня = уровень_данные.get(submodule, {'эмодзи': '📊', 'текст': 'Тренажер'})
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
            данные_уровня = уровень_данные.get(submodule, {'эмодзи': '📊', 'текст': 'Тренажер'})
            send_message(vk, user_id,
                         f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n{задача}\n\nВведите ответ:",
                         keyboard.get_keyboard())
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при переходе к следующей задаче: {str(e)}")


# ==================== ОСНОВНОЙ ОБРАБОТЧИК ====================
def handle_percentage_tasks(vk, user_id, text, user_data):
    """Обрабатывает сообщения в модуле задач на проценты"""
    user_state = get_user_state(user_id)
    current_submodule = user_state.get('sub_module', '')

    # ========== ОБРАБОТКА КНОПОК НАЗАД ==========
    if text == '🔙 Назад к типам задач':
        from main import show_text_tasks_menu
        show_text_tasks_menu(user_id)
        return

    if text == '🔙 Назад к меню процентов':
        show_percentage_main_menu(vk, user_id)
        return

    if text == '🔙 Назад':
        if current_submodule == 'examples_menu' or current_submodule == 'viewing_example':
            show_examples_menu(vk, user_id)
        elif current_submodule == 'training_menu' or current_submodule == 'viewing_lesson':
            show_training_menu(vk, user_id)
        elif current_submodule == 'simulator_menu':
            show_simulator_menu(vk, user_id)
        else:
            show_percentage_main_menu(vk, user_id)
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
            '🔙 Назад к тренажеру', '🔙 Назад к меню процентов', '🔙 Назад к типам задач',
            '📖 Пример 1', '📖 Пример 2', '📖 Пример 3', '📖 Пример 4', '📖 Пример 5',
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
    elif text == '📖 Пример 1':
        send_example_1(vk, user_id)
        return
    elif text == '📖 Пример 2':
        send_example_2(vk, user_id)
        return
    elif text == '📖 Пример 3':
        send_example_3(vk, user_id)
        return
    elif text == '📖 Пример 4':
        send_example_4(vk, user_id)
        return
    elif text == '📖 Пример 5':
        send_example_5(vk, user_id)
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
        show_percentage_main_menu(vk, user_id)
        return
