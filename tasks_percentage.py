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


# ==================== ПРИМЕРЫ ЗАДАЧ ====================
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


# ==================== УРОКИ ====================
def send_lesson(vk, user_id, lesson_num):
    """Отправляет урок"""
    lessons = {
        1: """📖 Урок 1: Основные формулы

p% от A = A × p / 100
Если p% числа равны B, то A = B × 100 / p
Сколько процентов B составляет от A: (B / A) × 100%""",

        2: """📖 Урок 2: Нахождение процента

Примеры:
1) 8% от 50 = 50 × 8 / 100 = 4
2) Число, если 12% = 36: 36 × 100 / 12 = 300
3) 15 от 60 = (15/60) × 100% = 25%""",

        3: """📖 Урок 3: Изменение величины

Увеличение на p%: A × (1 + p/100)
Уменьшение на p%: A × (1 - p/100)

Пример: Увеличить 200 на 15% = 200 × 1,15 = 230
Уменьшить 200 на 15% = 200 × 0,85 = 170"""
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
• Последовательные изменения: A × (1 ± p/100) × (1 ± q/100)"""

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к меню процентов', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'reference')


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
        # Возвращаемся в предыдущее меню в зависимости от текущего подмодуля
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
    elif text == '💡 Подсказка' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator',
                                                         'random_simulator']:
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

    elif text == '📝 Ответ' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator',
                                                     'random_simulator']:
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
        show_percentage_main_menu(vk, user_id)