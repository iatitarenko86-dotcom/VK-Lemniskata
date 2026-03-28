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

    keyboard.add_button('📖 Пример 1', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 2', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 3', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Пример 4', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Пример 5', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🔙 Назад к меню концентрации', color=VkKeyboardColor.SECONDARY)

    text = "📝 Выберите пример:"
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


# ==================== ПРИМЕРЫ ЗАДАЧ ====================
def send_example_1(vk, user_id):
    text = """🧪 Пример 1: Смешивание растворов

Условие: Смешали 8 л 15% раствора и 12 л 25% раствора. Найдите концентрацию.

Решение:
1) 8 × 0,15 = 1,2 л (вещества в 1-м)
2) 12 × 0,25 = 3 л (вещества во 2-м)
3) 1,2 + 3 = 4,2 л (всего вещества)
4) 8 + 12 = 20 л (общий объем)
5) 4,2 / 20 × 100% = 21%

Ответ: 21%"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_2(vk, user_id):
    text = """⚗️ Пример 2: Система уравнений

Условие: Смешали 30% и 10% растворы, получили 600 г 15% раствора. Сколько граммов каждого взяли?

Решение:
Пусть x - масса 30% раствора, y - масса 10%
x + y = 600
0,3x + 0,1y = 0,15×600 = 90
Решаем: y = 600 - x
0,3x + 0,1(600-x) = 90
0,3x + 60 - 0,1x = 90
0,2x = 30 → x = 150, y = 450

Ответ: 150 г 30% и 450 г 10%"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_3(vk, user_id):
    text = """🏺 Пример 3: Сплав латуни

Условие: Меди на 11 кг больше цинка. После добавления 12 кг меди, концентрация стала 75%. Сколько меди было?

Решение:
Пусть x - медь, y - цинк
x = y + 11
(x + 12)/(x + y + 12) = 0,75
Подставляем: (y+23)/(2y+23) = 0,75
y + 23 = 1,5y + 17,25
0,5y = 5,75 → y = 11,5 → x = 22,5

Ответ: 22,5 кг"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_4(vk, user_id):
    text = """🍎 Пример 4: Высушивание фруктов

Условие: Свежие фрукты содержат 80% воды, сушеные - 28%. Сколько сухих получится из 288 кг свежих?

Решение:
Сухого вещества в свежих: 288 × 0,2 = 57,6 кг
В сушеных сухого: 100% - 28% = 72%
Масса сушеных: 57,6 / 0,72 = 80 кг

Ответ: 80 кг"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


def send_example_5(vk, user_id):
    text = """📊 Пример 5: Два сплава

Условие: Сплав 1 (10% меди), сплав 2 (40% меди). Масса 2-го на 3 кг больше 1-го. После сплавления получили 30% меди. Найдите массу 3-го сплава.

Решение:
Пусть x - масса 1-го сплава, тогда 2-го: x+3
Масса 3-го: 2x+3
Меди: 0,1x + 0,4(x+3) = 0,3(2x+3)
0,1x + 0,4x + 1,2 = 0,6x + 0,9
0,5x + 1,2 = 0,6x + 0,9
0,3 = 0,1x → x = 3
Масса 3-го: 2×3 + 3 = 9 кг

Ответ: 9 кг"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'viewing_example')


# ==================== УРОКИ ====================
def send_lesson(vk, user_id, lesson_num):
    """Отправляет урок"""
    lessons = {
        1: """📖 Урок 1: Основные понятия

Концентрация = (масса вещества / масса раствора) × 100%

Масса вещества = масса раствора × концентрация / 100%

Закон сохранения: m₁·c₁ + m₂·c₂ = (m₁ + m₂)·c""",

        2: """📖 Урок 2: Смешивание растворов

Алгоритм:
1. Найти массу вещества в каждом растворе
2. Сложить массы веществ
3. Сложить массы растворов
4. Разделить массу вещества на массу смеси и умножить на 100%""",

        3: """📖 Урок 3: Сплавы и высушивание

Сплавы - аналогично растворам.

Высушивание:
При высушивании масса сухого вещества не меняется!
m₁ × (100% - w₁) = m₂ × (100% - w₂)"""
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

Основные понятия:
• Концентрация = масса вещества / масса раствора × 100%

Основные формулы:
• m(вещества) = m(раствора) × c / 100%
• При смешивании: m₁·c₁ + m₂·c₂ = (m₁ + m₂)·c
• При высушивании: m₁·(100%-w₁) = m₂·(100%-w₂)

Правило креста:
      a        |c - b|
        \\     /
          c
        /     \\
      b        |a - c|
Соотношение a : b = |c - b| : |a - c|"""

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
    elif text == '📝 Примеры':
        show_examples_menu(vk, user_id)
    elif text == '🎓 Обучение':
        show_training_menu(vk, user_id)
    elif text == '🎯 Тренажер':
        show_simulator_menu(vk, user_id)

    # ========== ВЫБОР ПРИМЕРОВ ==========
    elif text == '📖 Пример 1':
        send_example_1(vk, user_id)
    elif text == '📖 Пример 2':
        send_example_2(vk, user_id)
    elif text == '📖 Пример 3':
        send_example_3(vk, user_id)
    elif text == '📖 Пример 4':
        send_example_4(vk, user_id)
    elif text == '📖 Пример 5':
        send_example_5(vk, user_id)

    # ========== ВЫБОР УРОКОВ ==========
    elif text == '📖 Урок 1':
        send_lesson(vk, user_id, 1)
    elif text == '📖 Урок 2':
        send_lesson(vk, user_id, 2)
    elif text == '📖 Урок 3':
        send_lesson(vk, user_id, 3)

    # ========== ВЫБОР УРОВНЯ ТРЕНАЖЕРА ==========
    elif text == '🟢 Легкий':
        start_easy_simulator(vk, user_id)
    elif text == '🟡 Средний':
        start_medium_simulator(vk, user_id)
    elif text == '🔴 Сложный':
        start_hard_simulator(vk, user_id)
    elif text == '🎲 Случайно':
        start_random_simulator(vk, user_id)

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

    elif text == '➡️ Далее' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator']:
        if user_id in тренажеры_пользователей:
            next_task = тренажеры_пользователей[user_id].получить_текущую_задачу()
            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
            send_message(vk, user_id, f"Следующая задача:\n\n{next_task}\n\nВведите ответ:", keyboard.get_keyboard())

    # ========== НАВИГАЦИЯ В УРОКАХ ==========
    elif text == '⬅️ Назад' and current_submodule == 'viewing_lesson':
        current_lesson = user_state.get('current_lesson', 1)
        prev_lesson = current_lesson - 1 if current_lesson > 1 else 3
        send_lesson(vk, user_id, prev_lesson)

    elif text == '➡️ Далее' and current_submodule == 'viewing_lesson':
        current_lesson = user_state.get('current_lesson', 1)
        next_lesson = current_lesson + 1 if current_lesson < 3 else 1
        send_lesson(vk, user_id, next_lesson)

    else:
        show_concentration_main_menu(vk, user_id)
