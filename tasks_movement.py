# tasks_movement.py
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from user_states import set_user_state, get_user_state, update_user_data
from simulator_movement1 import SimulatorMovement1
from simulator_movement2 import SimulatorMovement2
from simulator_movement3 import SimulatorMovement3
from simulator_movement4 import SimulatorMovement4

# Глобальный словарь для хранения тренажеров по пользователям
тренажеры_пользователей = {}


# ==================== ФУНКЦИИ ДЛЯ СОЗДАНИЯ КЛАВИАТУР ====================
def create_keyboard(buttons, one_time=False):
    """Создание клавиатуры VK с автоматическим разбиением по 4 кнопки в строке"""
    keyboard = VkKeyboard(one_time=one_time)

    # Максимальное количество кнопок в строке для VK
    MAX_BUTTONS_PER_ROW = 4

    for i, button in enumerate(buttons):
        # Определяем цвет кнопки
        if "Назад" in button or "В меню" in button or "К задачам" in button or "К тренажеру" in button:
            color = VkKeyboardColor.SECONDARY
        elif button.startswith("🟢"):
            color = VkKeyboardColor.POSITIVE
        elif button.startswith("🔴"):
            color = VkKeyboardColor.NEGATIVE
        elif button.startswith("📖") or button.startswith("📝") or button.startswith("🎓") or button.startswith("📚"):
            color = VkKeyboardColor.PRIMARY
        else:
            color = VkKeyboardColor.PRIMARY

        # Добавляем кнопку
        keyboard.add_button(button, color=color)

        # Добавляем новую строку после каждых MAX_BUTTONS_PER_ROW кнопок
        # и не добавляем после последней кнопки
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


# ==================== ГЛАВНОЕ МЕНЮ ДВИЖЕНИЯ ====================
def show_movement_main_menu(vk, user_id):
    """Отображает главное меню задач на движение"""
    keyboard = VkKeyboard()

    # Строка 1: 2 кнопки
    keyboard.add_button('📚 Справочный материал', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📝 Примеры задач', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 2: 2 кнопки
    keyboard.add_button('🎓 Обучение', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🎯 Тренажер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 3: 1 кнопка (назад)
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)

    text = """🚗 Задачи на движение

Выберите раздел для изучения:

• 📚 Справочный материал - формулы и теория
• 📝 Примеры задач - готовые решения
• 🎓 Обучение - пошаговое изучение
• 🎯 Тренажер - практические задания"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'main_menu')


# ==================== НАЧАЛО РАБОТЫ ====================
def start_movement_tasks(vk, user_id, user_data):
    """Начинает работу с задачами на движение"""
    show_movement_main_menu(vk, user_id)


# ==================== МЕНЮ ТРЕНАЖЕРА ====================
def show_simulator_menu(vk, user_id):
    """Отображает меню тренажера"""
    keyboard = VkKeyboard()

    # Строка 1: 2 кнопки
    keyboard.add_button('🟢 Легкий уровень', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('🟡 Средний уровень', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 2: 2 кнопки
    keyboard.add_button('🔴 Сложный уровень', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('🎲 Случайная задача', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 3: 1 кнопка (назад)
    keyboard.add_button('🔙 Назад к меню движения', color=VkKeyboardColor.SECONDARY)

    text = """🎯 Тренажер: Задачи на движение

Выберите уровень сложности:

• 🟢 Легкий - 12 базовых задач
• 🟡 Средний - 11 задач средней сложности
• 🔴 Сложный - 9 комплексных задач
• 🎲 Случайная - задача любого уровня"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'simulator_menu')


# ==================== ЗАПУСК ЛЕГКОГО УРОВНЯ ====================
def start_easy_simulator(vk, user_id):
    """Запускает легкий уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorMovement1()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorMovement1):
                тренажеры_пользователей[user_id] = SimulatorMovement1()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'легкий'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🟢 Легкий уровень тренажера\n\n{задача}\n\nВведите ответ в чат:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'movement_tasks', 'easy_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при запуске легкого уровня: {str(e)}")
        show_simulator_menu(vk, user_id)


# ==================== ЗАПУСК СРЕДНЕГО УРОВНЯ ====================
def start_medium_simulator(vk, user_id):
    """Запускает средний уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorMovement2()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorMovement2):
                тренажеры_пользователей[user_id] = SimulatorMovement2()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'средний'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🟡 Средний уровень тренажера\n\n{задача}\n\nВведите ответ в чат:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'movement_tasks', 'medium_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при запуске среднего уровня: {str(e)}")
        show_simulator_menu(vk, user_id)


# ==================== ЗАПУСК СЛОЖНОГО УРОВНЯ ====================
def start_hard_simulator(vk, user_id):
    """Запускает сложный уровень тренажера"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorMovement3()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorMovement3):
                тренажеры_пользователей[user_id] = SimulatorMovement3()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'сложный'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🔴 Сложный уровень тренажера\n\n{задача}\n\nВведите ответ в чат:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'movement_tasks', 'hard_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при запуске сложного уровня: {str(e)}")
        show_simulator_menu(vk, user_id)


# ==================== ЗАПУСК СЛУЧАЙНЫХ ЗАДАЧ ====================
def start_random_simulator(vk, user_id):
    """Запускает режим случайных задач"""
    try:
        if user_id not in тренажеры_пользователей:
            тренажеры_пользователей[user_id] = SimulatorMovement4()
        else:
            if not isinstance(тренажеры_пользователей[user_id], SimulatorMovement4):
                тренажеры_пользователей[user_id] = SimulatorMovement4()

        тренажер = тренажеры_пользователей[user_id]
        задача = тренажер.начать_уровень()

        update_user_data(user_id, {
            'тренажер_активен': True,
            'уровень_тренажера': 'случайные'
        })

        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('🔄 Новая задача', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"🎲 Случайная задача\n\n{задача}\n\nВведите ответ в чат:",
                     keyboard.get_keyboard())

        set_user_state(user_id, 'movement_tasks', 'random_simulator')
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при запуске случайных задач: {str(e)}")
        show_simulator_menu(vk, user_id)


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

        # Определяем текст и эмодзи для уровня
        уровень_данные = {
            'легкий': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
            'средний': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
            'сложный': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'},
            'случайные': {'эмодзи': '🎲', 'текст': 'Случайная задача'}
        }

        данные_уровня = уровень_данные.get(уровень, {'эмодзи': '🎯', 'текст': 'Тренажер'})

        # Создаем разметку кнопок
        keyboard = VkKeyboard()

        if уровень == 'случайные':
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая задача', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
        else:
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        if успех:
            if "Следующая задача" in сообщение:
                # Показываем следующую задачу
                задача = тренажер.получить_текущую_задачу()

                send_message(vk, user_id,
                             f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n"
                             f"✅ Правильно!\n\n"
                             f"{задача}\n\n"
                             "Введите ответ в чат:",
                             keyboard.get_keyboard())
            else:
                # Все задачи решены (только для уровневых тренажеров)
                if уровень != 'случайные':
                    final_keyboard = VkKeyboard()
                    final_keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

                    send_message(vk, user_id,
                                 f"✅ Поздравляем!\n\n"
                                 f"🎉 Вы успешно решили все задачи {уровень} уровня!\n\n"
                                 f"Можете вернуться в меню тренажера или выбрать другой уровень.",
                                 final_keyboard.get_keyboard())
                else:
                    # Для случайных задач просто показываем следующую
                    задача = тренажер.получить_следующую_задачу()
                    send_message(vk, user_id,
                                 f"✅ Правильно!\n\n"
                                 f"🎲 Следующая случайная задача:\n\n"
                                 f"{задача}\n\n"
                                 "Введите ответ в чат:",
                                 keyboard.get_keyboard())
        else:
            # Неправильный ответ
            задача = тренажер.получить_текущую_задачу()

            send_message(vk, user_id,
                         f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n"
                         f"{сообщение}\n\n"
                         f"{задача}\n\n"
                         "Введите ответ в чат:",
                         keyboard.get_keyboard())
    except Exception as e:
        keyboard = VkKeyboard()
        keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

        send_message(vk, user_id,
                     f"❌ Ошибка при проверке ответа: {str(e)}\n\n"
                     "Попробуйте еще раз или вернитесь в меню:",
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
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая задача', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)
        else:
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
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
            keyboard.add_button('🔄 Новая задача', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

            send_message(vk, user_id,
                         f"🎲 Случайная задача\n\n"
                         f"{ответ}\n\n"
                         "Нажмите 'Новая задача' для продолжения:",
                         keyboard.get_keyboard())
        else:
            # Определяем уровень для уровневых тренажеров
            уровень_данные = {
                'easy_simulator': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
                'medium_simulator': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
                'hard_simulator': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'}
            }

            данные_уровня = уровень_данные.get(submodule, {'эмодзи': '🎯', 'текст': 'Тренажер'})

            keyboard = VkKeyboard()
            keyboard.add_button('➡️ Следующая задача', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

            send_message(vk, user_id,
                         f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n"
                         f"{ответ}\n\n"
                         "Нажмите 'Следующая задача' для продолжения:",
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
            # Для случайных задач получаем новую задачу
            задача = тренажер.получить_следующую_задачу()

            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('🔄 Новая задача', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

            send_message(vk, user_id,
                         f"🎲 Случайная задача\n\n"
                         f"{задача}\n\n"
                         "Введите ответ в чат:",
                         keyboard.get_keyboard())
        else:
            # Для уровневых тренажеров переходим к следующей задаче
            if hasattr(тренажер, 'текущая_задача'):
                тренажер.текущая_задача += 1

            задача = тренажер.получить_текущую_задачу()

            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

            # Определяем уровень
            уровень_данные = {
                'easy_simulator': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
                'medium_simulator': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
                'hard_simulator': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'}
            }

            данные_уровня = уровень_данные.get(submodule, {'эмодзи': '🎯', 'текст': 'Тренажер'})

            send_message(vk, user_id,
                         f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n"
                         f"{задача}\n\n"
                         "Введите ответ в чат:",
                         keyboard.get_keyboard())
    except Exception as e:
        send_message(vk, user_id, f"❌ Ошибка при переходе к следующей задаче: {str(e)}")


# ==================== СПРАВОЧНЫЙ МАТЕРИАЛ ====================
def send_reference_material(vk, user_id):
    """Отправляет справочный материал по задачам на движение"""
    reference_text = (
        "📚 Справочный материал по задачам на движение\n\n"
        "Здесь вы найдете все основные формулы, понятия и теории:\n\n"
        "Основные формулы движения:\n"
        "┌─────────────────────┬─────────────────────┬─────────────────────┐\n"
        "│      Формула        │     Обозначение     │      Единицы        │\n"
        "├─────────────────────┼─────────────────────┼─────────────────────┤\n"
        "│   S = v × t         │ S - расстояние      │ км, м               │\n"
        "│   v = S / t         │ v - скорость        │ км/ч, м/с           │\n"
        "│   t = S / v         │ t - время           │ ч, мин, с           │\n"
        "└─────────────────────┴─────────────────────┴─────────────────────┘\n\n"
        "Единицы измерения:\n"
        "• 1 м/с = 3.6 км/ч\n"
        "• 1 км/ч ≈ 0.278 м/с\n"
        "• 1 час = 60 минут = 3600 секунд\n\n"
        "Для подробного изучения перейдите по ссылке:\n"
        "https://disk.yandex.ru/i/a1LXK4704Y7hMQ"
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к меню движения', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, reference_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'reference')


# ==================== МЕНЮ ПРИМЕРОВ (7 КНОПОК) ====================
def show_examples_menu(vk, user_id):
    """Отображает меню примеров задач с 7 кнопками, разбитыми на строки"""
    keyboard = VkKeyboard()

    # Строка 1: 4 кнопки
    keyboard.add_button('🚗 Пример 1: Два автомобиля', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🚂 Пример 2: Поезд и мост', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🚢 Пример 3: Два теплохода', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🚶 Пример 4: Пешеход и велосипедист', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 2: 3 кнопки
    keyboard.add_button('🏙️ Пример 5: А→Б→А со скоростью', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🏎️ Пример 6: Болиды по кругу', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🛶 Пример 7: Лодка по реке', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 3: 1 кнопка (назад)
    keyboard.add_button('🔙 Назад к меню движения', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id,
                 "📝 Примеры задач на движение\n\n"
                 "Выберите пример для изучения:\n\n"
                 "Каждый пример содержит:\n"
                 "• Полное условие задачи\n"
                 "• Таблицу данных\n"
                 "• Развернутое решение\n"
                 "• Итоговый ответ",
                 keyboard.get_keyboard())

    set_user_state(user_id, 'movement_tasks', 'examples_menu')


# ==================== ПРИМЕРЫ ЗАДАЧ ====================
def send_example_1(vk, user_id):
    """Отправляет пример 1: Два автомобиля"""
    example_text = (
        "🚗 Пример 1: Два автомобиля\n\n"
        "Условие задачи:\n"
        "Из двух городов, расстояние между которыми 420 км, одновременно навстречу друг другу выехали два автомобиля. "
        "Скорость первого автомобиля 60 км/ч, скорость второго — 80 км/ч. Через сколько часов они встретятся?\n\n"
        "Таблица данных:\n"
        "┌─────────────────────┬──────────┬──────────┐\n"
        "│      Параметр       │ 1-й авто │ 2-й авто │\n"
        "├─────────────────────┼──────────┼──────────┤\n"
        "│   Скорость (км/ч)   │    60    │    80    │\n"
        "│   Расстояние (км)   │    ?     │    ?     │\n"
        "│   Время (ч)         │    t     │    t     │\n"
        "├─────────────────────┼──────────┴──────────┤\n"
        "│   Общее расстояние  │      420 км         │\n"
        "└─────────────────────┴─────────────────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Определяем тип движения:\n"
        "   Движение навстречу друг другу.\n\n"
        "2. Находим скорость сближения:\n"
        "   При движении навстречу скорости складываются:\n"
        "   v = v₁ + v₂ = 60 + 80 = 140 км/ч\n\n"
        "3. Находим время встречи:\n"
        "   Используем формулу t = S / v:\n"
        "   t = 420 / 140 = 3 часа\n\n"
        "4. Проверяем решение:\n"
        "   • За 3 часа первый автомобиль проедет: 60 × 3 = 180 км\n"
        "   • За 3 часа второй автомобиль проедет: 80 × 3 = 240 км\n"
        "   • Сумма: 180 + 240 = 420 км ✓\n\n"
        "5. Формулируем ответ:\n"
        "   Ответ: автомобили встретятся через 3 часа.\n\n"
        "Формула для запоминания:\n"
        "t = S / (v₁ + v₂) - время встречи при движении навстречу."
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_2(vk, user_id):
    """Отправляет пример 2: Поезд и мост"""
    example_text = (
        "🚂 Пример 2: Поезд и мост\n\n"
        "Условие задачи:\n"
        "Поезд длиной 250 м проезжает мост длиной 150 м за 20 секунд. "
        "С какой скоростью движется поезд? Ответ дайте в км/ч.\n\n"
        "Таблица данных:\n"
        "┌───────────────────────┬────────────┬──────────┐\n"
        "│      Параметр         │   Значение │ Единицы  │\n"
        "├───────────────────────┼────────────┼──────────┤\n"
        "│ Длина поезда          │    250     │    м     │\n"
        "│ Длина моста           │    150     │    м     │\n"
        "│ Время проезда         │    20      │    с     │\n"
        "│ Скорость (м/с)        │     ?      │   м/с    │\n"
        "│ Скорость (км/ч)       │     ?      │  км/ч    │\n"
        "└───────────────────────┴────────────┴──────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Анализируем условие:\n"
        "   При проезде моста поезд проходит путь, равный сумме своей длины и длины моста.\n\n"
        "2. Находим полный путь:\n"
        "   S = длина поезда + длина моста\n"
        "   S = 250 + 150 = 400 м\n\n"
        "3. Находим скорость в м/с:\n"
        "   Используем формулу v = S / t:\n"
        "   v = 400 / 20 = 20 м/с\n\n"
        "4. Переводим скорость в км/ч:\n"
        "   1 м/с = 3.6 км/ч\n"
        "   v = 20 × 3.6 = 72 км/ч\n\n"
        "5. Проверяем единицы измерения:\n"
        "   Время дано в секундах, путь в метрах → скорость в м/с.\n"
        "   Ответ нужно дать в км/ч → делаем перевод.\n\n"
        "6. Формулируем ответ:\n"
        "   Ответ: скорость поезда 72 км/ч.\n\n"
        "Важное замечание:\n"
        "В задачах с протяженными объектами (поездами, тоннелями, мостами) нужно учитывать полный путь, который проходит объект."
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_3(vk, user_id):
    """Отправляет пример 3: Два теплохода"""
    example_text = (
        "🚢 Пример 3: Два теплохода\n\n"
        "Условие задачи:\n"
        "Два теплохода вышли одновременно навстречу друг другу из двух портов, расстояние между которыми 300 км. "
        "Скорость первого теплохода 20 км/ч, второго — 30 км/ч. Через сколько часов они встретятся?\n\n"
        "Таблица данных:\n"
        "┌─────────────────────┬────────────┬────────────┐\n"
        "│      Параметр       │ Теплоход 1 │ Теплоход 2 │\n"
        "├─────────────────────┼────────────┼────────────┤\n"
        "│   Скорость (км/ч)   │     20     │     30     │\n"
        "│   Время (ч)         │     t      │     t      │\n"
        "│   Расстояние (км)   │     ?      │     ?      │\n"
        "├─────────────────────┼────────────┴────────────┤\n"
        "│   Общее расстояние  │       300 км            │\n"
        "└─────────────────────┴─────────────────────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Анализируем тип движения:\n"
        "   Теплоходы движутся навстречу друг другу.\n\n"
        "2. Применяем формулу для встречного движения:\n"
        "   Скорость сближения равна сумме скоростей:\n"
        "   v = v₁ + v₂ = 20 + 30 = 50 км/ч\n\n"
        "3. Находим время встречи:\n"
        "   t = S / v = 300 / 50 = 6 часов\n\n"
        "4. Дополнительно находим расстояния:\n"
        "   • Путь первого теплохода: S₁ = 20 × 6 = 120 км\n"
        "   • Путь второго теплохода: S₂ = 30 × 6 = 180 км\n"
        "   • Проверка: 120 + 180 = 300 км ✓\n\n"
        "5. Интерпретируем результат:\n"
        "   Теплоходы встретятся через 6 часов после начала движения.\n"
        "   Место встречи находится на расстоянии 120 км от первого порта\n"
        "   и 180 км от второго порта.\n\n"
        "6. Формулируем ответ:\n"
        "   Ответ: теплоходы встретятся через 6 часов.\n\n"
        "Формула:\n"
        "t = S / (v₁ + v₂)"
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_4(vk, user_id):
    """Отправляет пример 4: Пешеход и велосипедист"""
    example_text = (
        "🚶 Пример 4: Пешеход и велосипедист\n\n"
        "Условие задачи:\n"
        "Из одной точки в противоположных направлениях одновременно вышли пешеход и велосипедист. "
        "Скорость пешехода 5 км/ч, велосипедиста — 15 км/ч. Какое расстояние будет между ними через 2 часа?\n\n"
        "Таблица данных:\n"
        "┌─────────────────────┬────────────┬─────────────────┐\n"
        "│      Параметр       │  Пешеход   │ Велосипедист    │\n"
        "├─────────────────────┼────────────┼─────────────────┤\n"
        "│   Скорость (км/ч)   │     5      │       15        │\n"
        "│   Время (ч)         │     2      │        2        │\n"
        "│   Расстояние (км)   │     ?      │        ?        │\n"
        "└─────────────────────┴────────────┴─────────────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Анализируем тип движения:\n"
        "   Движение в противоположных направлениях из одной точки.\n\n"
        "2. Способ 1: Через скорость удаления\n"
        "   • Скорость удаления: v = v₁ + v₂ = 5 + 15 = 20 км/ч\n"
        "   • Расстояние через 2 часа: S = v × t = 20 × 2 = 40 км\n\n"
        "3. Способ 2: Через индивидуальные пути\n"
        "   • Путь пешехода: S₁ = 5 × 2 = 10 км\n"
        "   • Путь велосипедиста: S₂ = 15 × 2 = 30 км\n"
        "   • Общее расстояние: S = S₁ + S₂ = 10 + 30 = 40 км\n\n"
        "4. Проверяем логику решения:\n"
        "   Через 1 час: расстояние = 5 + 15 = 20 км\n"
        "   Через 2 часа: расстояние = 20 × 2 = 40 км\n"
        "   Оба способа дают одинаковый результат.\n\n"
        "5. Выбираем оптимальный способ:\n"
        "   Для движения в противоположных направлениях удобнее использовать\n"
        "   скорость удаления (v₁ + v₂), так как это сокращает вычисления.\n\n"
        "6. Формулируем ответ:\n"
        "   Ответ: через 2 часа расстояние между ними будет 40 км.\n\n"
        "Формула для запоминания:\n"
        "При движении в противоположных направлениях: v = v₁ + v₂"
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_5(vk, user_id):
    """Отправляет пример 5: А→Б→А со скоростью"""
    example_text = (
        "🏙️ Пример 5: А→Б→А со скоростью\n\n"
        "Условие задачи:\n"
        "Автомобиль выехал с постоянной скоростью из города А в город Б, расстояние между которыми равно 180 км. "
        "На следующий день он отправился обратно в А, увеличив скорость на 5 км/ч, в результате чего затратил на обратный путь на 24 минуты меньше. "
        "Найдите скорость автомобиля на пути из А в Б.\n\n"
        "Таблица данных:\n"
        "┌─────────────────────┬───────────────┬───────────────┐\n"
        "│      Параметр       │   Туда (А→Б)  │  Обратно (Б→А)│\n"
        "├─────────────────────┼───────────────┼───────────────┤\n"
        "│   Расстояние (км)   │      180      │      180      │\n"
        "│   Скорость (км/ч)   │       x       │     x + 5     │\n"
        "│   Время (ч)         │     180/x     │  180/(x+5)    │\n"
        "├─────────────────────┼───────────────┴───────────────┤\n"
        "│   Разница во времени│        24 минуты = 0.4 часа    │\n"
        "└─────────────────────┴───────────────────────────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Вводим переменную:\n"
        "   Пусть x - скорость из А в Б (км/ч)\n"
        "   Тогда скорость обратно: x + 5 (км/ч)\n\n"
        "2. Записываем выражения для времени:\n"
        "   • Время туда: t₁ = 180 / x (часов)\n"
        "   • Время обратно: t₂ = 180 / (x + 5) (часов)\n\n"
        "3. Составляем уравнение:\n"
        "   Разница во времени: 24 минуты = 24/60 = 0.4 часа\n"
        "   t₁ - t₂ = 0.4\n"
        "   180/x - 180/(x + 5) = 0.4\n\n"
        "4. Решаем уравнение:\n"
        "   Умножаем обе части на x(x + 5):\n"
        "   180(x + 5) - 180x = 0.4x(x + 5)\n"
        "   180x + 900 - 180x = 0.4x² + 2x\n"
        "   900 = 0.4x² + 2x\n\n"
        "5. Приводим к квадратному уравнению:\n"
        "   0.4x² + 2x - 900 = 0\n"
        "   Умножаем на 5 для удобства:\n"
        "   2x² + 10x - 4500 = 0\n"
        "   Делим на 2:\n"
        "   x² + 5x - 2250 = 0\n\n"
        "6. Находим корни:\n"
        "   Дискриминант: D = 5² - 4×1×(-2250) = 25 + 9000 = 9025\n"
        "   √D = √9025 = 95\n"
        "   x₁ = (-5 + 95)/2 = 90/2 = 45\n"
        "   x₂ = (-5 - 95)/2 = -100/2 = -50 (не подходит, скорость > 0)\n\n"
        "7. Проверяем решение:\n"
        "   • Скорость туда: 45 км/ч, время: 180/45 = 4 часа\n"
        "   • Скорость обратно: 50 км/ч, время: 180/50 = 3.6 часа\n"
        "   • Разница: 4 - 3.6 = 0.4 часа = 24 минуты ✓\n\n"
        "8. Формулируем ответ:\n"
        "   Ответ: скорость автомобиля на пути из А в Б равна 45 км/ч.\n\n"
        "Алгоритм решения:\n"
        "1. Ввести переменную для неизвестной скорости\n"
        "2. Выразить время для каждого направления\n"
        "3. Составить уравнение на основе разницы во времени\n"
        "4. Решить квадратное уравнение\n"
        "5. Выбрать положительный корень"
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_6(vk, user_id):
    """Отправляет пример 6: Болиды по кругу"""
    example_text = (
        "🏎️ Пример 6: Болиды по кругу\n\n"
        "Условие задачи:\n"
        "Два болида стартуют одновременно в одном направлении из двух диаметрально противоположных точек круговой трассы, длина которой равна 19,5 км. "
        "Через сколько минут болиды поравняются в первый раз, если скорость одного из них на 13 км/ч больше скорости другого?\n\n"
        "Таблица данных:\n"
        "┌───────────────────────┬──────────────┬──────────────┐\n"
        "│      Параметр         │  Медленный   │  Быстрый     │\n"
        "├───────────────────────┼──────────────┼──────────────┤\n"
        "│   Длина трассы        │     19.5 км                 │\n"
        "│   Начальное расстояние│    9.75 км (половина)       │\n"
        "│   Скорость (км/ч)     │      v       │    v + 13    │\n"
        "│   Время встречи (ч)   │      t       │      t       │\n"
        "└───────────────────────┴──────────────┴──────────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Анализируем условие:\n"
        "   • Болиды стартуют из диаметрально противоположных точек\n"
        "   • Значит, начальное расстояние между ними равно половине длины трассы\n"
        "   • S₀ = 19.5 / 2 = 9.75 км\n"
        "   • Движение в одном направлении\n\n"
        "2. Вводим переменные:\n"
        "   Пусть v - скорость медленного болида (км/ч)\n"
        "   Тогда скорость быстрого: v + 13 (км/ч)\n\n"
        "3. Определяем тип движения:\n"
        "   Движение вдогонку. Быстрый болид должен догнать медленного.\n"
        "   Скорость сближения: v₁ - v₂ = (v + 13) - v = 13 км/ч\n\n"
        "4. Составляем уравнение:\n"
        "   Для движения вдогонку: t = S₀ / (v₁ - v₂)\n"
        "   t = 9.75 / 13\n\n"
        "5. Вычисляем время:\n"
        "   t = 9.75 / 13 = 0.75 часа\n\n"
        "6. Переводим в минуты:\n"
        "   0.75 часа × 60 = 45 минут\n\n"
        "7. Проверяем логику:\n"
        "   За 0.75 часа быстрый болид проедет на 13 × 0.75 = 9.75 км больше,\n"
        "   чем медленный, что как раз равно начальному расстоянию.\n\n"
        "8. Особенность кругового движения:\n"
        "   При движении по кругу из диаметрально противоположных точек\n"
        "   вдогонку нужно преодолеть половину круга, а не целый круг.\n\n"
        "9. Формулируем ответ:\n"
        "   Ответ: болиды поравняются в первый раз через 45 минут.\n\n"
        "Формула для запоминания:\n"
        "Для движения вдогонку по кругу из диаметрально противоположных точек:\n"
        "t = (L/2) / (v₁ - v₂), где L - длина круга."
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_7(vk, user_id):
    """Отправляет пример 7: Лодка по реке"""
    example_text = (
        "🛶 Пример 7: Лодка по реке\n\n"
        "Условие задачи:\n"
        "Моторная лодка прошла 10 км по озеру и 4 км против течения реки, затратив на весь путь 1 час. "
        "Найдите собственную скорость лодки, если скорость течения реки равна 3 км/ч.\n\n"
        "Таблица данных:\n"
        "┌───────────────────────┬────────────────┬───────────────┐\n"
        "│      Параметр         │  По озеру      │ Против течения│\n"
        "├───────────────────────┼────────────────┼───────────────┤\n"
        "│   Расстояние (км)     │      10        │       4       │\n"
        "│   Собственная скорость│      v         │      v        │\n"
        "│   Скорость течения    │       0        │       3       │\n"
        "│   Фактическая скорость│      v         │     v - 3     │\n"
        "│   Время (ч)           │     10/v       │   4/(v - 3)   │\n"
        "├───────────────────────┼────────────────┴───────────────┤\n"
        "│   Общее время         │           1 час                │\n"
        "└───────────────────────┴────────────────────────────────┘\n\n"
        "Развернутое решение:\n\n"
        "1. Анализируем условие:\n"
        "   • По озеру: движение в стоячей воде, скорость = v\n"
        "   • Против течения: скорость = v - 3 (течение замедляет)\n"
        "   • Общее время: 1 час\n\n"
        "2. Вводим переменную:\n"
        "   Пусть v - собственная скорость лодки (км/ч)\n\n"
        "3. Записываем выражения для времени:\n"
        "   • Время по озеру: t₁ = 10 / v\n"
        "   • Время против течения: t₂ = 4 / (v - 3)\n\n"
        "4. Составляем уравнение:\n"
        "   t₁ + t₂ = 1\n"
        "   10/v + 4/(v - 3) = 1\n\n"
        "5. Решаем уравнение:\n"
        "   Умножаем обе части на v(v - 3):\n"
        "   10(v - 3) + 4v = v(v - 3)\n"
        "   10v - 30 + 4v = v² - 3v\n"
        "   14v - 30 = v² - 3v\n\n"
        "6. Приводим к квадратному уравнению:\n"
        "   v² - 3v - 14v + 30 = 0\n"
        "   v² - 17v + 30 = 0\n\n"
        "7. Находим корни:\n"
        "   Дискриминант: D = (-17)² - 4×1×30 = 289 - 120 = 169\n"
        "   √D = √169 = 13\n"
        "   v₁ = (17 + 13)/2 = 30/2 = 15\n"
        "   v₂ = (17 - 13)/2 = 4/2 = 2\n\n"
        "8. Проверяем корни:\n"
        "   • При v = 15 км/ч:\n"
        "     - По озеру: 10/15 = 2/3 часа = 40 минут\n"
        "     - Против течения: 4/(15-3) = 4/12 = 1/3 часа = 20 минут\n"
        "     - Общее: 40 + 20 = 60 минут = 1 час ✓\n"
        "   • При v = 2 км/ч:\n"
        "     - Против течения: v - 3 = -1 (скорость отрицательная!) - не подходит\n\n"
        "9. Интерпретируем результат:\n"
        "   Собственная скорость лодки должна быть больше скорости течения (3 км/ч),\n"
        "   иначе она не сможет двигаться против течения.\n\n"
        "10. Формулируем ответ:\n"
        "    Ответ: собственная скорость лодки равна 15 км/ч.\n\n"
        "Алгоритм решения задач с течением:\n"
        "1. vₛ - собственная скорость в стоячей воде\n"
        "2. vₜ - скорость течения\n"
        "3. По течению: v = vₛ + vₜ\n"
        "4. Против течения: v = vₛ - vₜ"
    )

    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


# ==================== ОБУЧЕНИЕ ====================
def show_training_menu(vk, user_id):
    """Отображает меню обучения"""
    keyboard = VkKeyboard()

    # Строка 1: 3 кнопки
    keyboard.add_button('📖 Урок 1: Основные формулы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 2: Движение навстречу', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 3: Движение вдогонку', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()

    # Строка 2: 1 кнопка (назад)
    keyboard.add_button('🔙 Назад к меню движения', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id,
                 "🎓 Обучение: Задачи на движение\n\n"
                 "Выберите урок для изучения:\n\n"
                 "Пошаговое изучение тем:\n"
                 "1. Основные формулы и понятия\n"
                 "2. Движение навстречу друг другу\n"
                 "3. Движение вдогонку",
                 keyboard.get_keyboard())

    set_user_state(user_id, 'movement_tasks', 'training_menu')


def send_lesson(vk, user_id, lesson_number):
    """Отправляет урок"""
    if lesson_number == 1:
        lesson_content = get_lesson_1_content()
    elif lesson_number == 2:
        lesson_content = get_lesson_2_content()
    elif lesson_number == 3:
        lesson_content = get_lesson_3_content()
    else:
        lesson_content = get_lesson_1_content()

    # Сохраняем текущий урок
    update_user_data(user_id, {'current_lesson': lesson_number})

    keyboard = VkKeyboard()
    keyboard.add_button('⬅️ Предыдущий урок', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('➡️ Следующий урок', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к урокам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, lesson_content, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_lesson')


def get_lesson_1_content():
    """Контент урока 1"""
    return (
        "📖 Урок 1: Основные формулы движения\n\n"
        "Основные формулы:\n\n"
        "1. Расстояние: S = v × t\n"
        "   где S - расстояние, v - скорость, t - время\n\n"
        "2. Скорость: v = S / t\n"
        "3. Время: t = S / v\n\n"
        "Единицы измерения:\n"
        "• 1 м/с = 3.6 км/ч\n"
        "• 1 км/ч ≈ 0.278 м/с\n"
        "• 1 час = 60 минут = 3600 секунд\n\n"
        "Пример:\n"
        "Автомобиль проехал 180 км за 3 часа. Найти скорость.\n"
        "v = 180 / 3 = 60 км/ч"
    )


def get_lesson_2_content():
    """Контент урока 2"""
    return (
        "📖 Урок 2: Движение навстречу друг другу\n\n"
        "Формула скорости сближения:\n"
        "v = v₁ + v₂\n\n"
        "Формула времени встречи:\n"
        "t = S / (v₁ + v₂)\n\n"
        "Пример:\n"
        "Из пунктов A и B, расстояние между которыми 120 км, выехали два автомобиля. "
        "Скорость первого 40 км/ч, второго — 60 км/ч.\n\n"
        "Решение:\n"
        "1. v = 40 + 60 = 100 км/ч\n"
        "2. t = 120 / 100 = 1.2 часа = 1 ч 12 мин\n\n"
        "Ответ: встретятся через 1 час 12 минут.\n\n"
        "Алгоритм решения:\n"
        "1. Найти скорость сближения (сумма скоростей)\n"
        "2. Разделить расстояние на скорость сближения\n"
        "3. Получить время встречи"
    )


def get_lesson_3_content():
    """Контент урока 3"""
    return (
        "📖 Урок 3: Движение вдогонку\n\n"
        "Формула скорости сближения:\n"
        "v = v₁ - v₂ (если v₁ > v₂)\n\n"
        "Формула времени сближения:\n"
        "t = S₀ / (v₁ - v₂)\n"
        "где S₀ - начальное расстояние\n\n"
        "Пример:\n"
        "Из пункта A в пункт B выехал велосипедист со скоростью 12 км/ч. "
        "Через 2 часа из A в том же направлении выехал мотоциклист со скоростью 20 км/ч. "
        "Через сколько часов мотоциклист догонит велосипедиста?\n\n"
        "Решение:\n"
        "1. За 2 часа велосипедист проехал: 12 × 2 = 24 км\n"
        "2. Скорость сближения: 20 - 12 = 8 км/ч\n"
        "3. Время: t = 24 / 8 = 3 часа\n\n"
        "Ответ: мотоциклист догонит через 3 часа.\n\n"
        "Алгоритм решения:\n"
        "1. Найти расстояние, которое прошёл первый объект до старта второго\n"
        "2. Найти скорость сближения (разность скоростей)\n"
        "3. Разделить начальное расстояние на скорость сближения"
    )


# ==================== ОБРАБОТЧИК СООБЩЕНИЙ ====================
def handle_movement_tasks(vk, user_id, text, user_data):
    """Обрабатывает сообщения в модуле задач на движение"""
    user_state = get_user_state(user_id)
    current_submodule = user_state.get('sub_module', '')

    # ========== ОБРАБОТКА КНОПКИ НАЗАД ==========
    if text == '🔙 Назад к типам задач':
        from main import show_text_tasks_menu
        show_text_tasks_menu(vk, user_id)
        return

    if text == '🔙 Назад к меню движения':
        show_movement_main_menu(vk, user_id)
        return

    if text == '🔙 Назад к примерам':
        show_examples_menu(vk, user_id)
        return

    if text == '🔙 Назад к урокам':
        show_training_menu(vk, user_id)
        return

    if text == '🔙 Назад к тренажеру':
        show_simulator_menu(vk, user_id)
        return

    # ========== ОБРАБОТКА ВВОДА ОТВЕТА В ТРЕНАЖЕРАХ ==========
    if current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
        # Список всех кнопок, которые НЕ считаются ответом пользователя
        системные_кнопки = [
            '💡 Подсказка', '📝 Показать ответ', '🔙 Назад к тренажеру', '➡️ Следующая задача',
            '🔄 Новая задача', '📚 Справочный материал', '📝 Примеры задач', '🎓 Обучение',
            '🎯 Тренажер', '🟢 Легкий уровень', '🟡 Средний уровень', '🔴 Сложный уровень',
            '🎲 Случайная задача', '🔙 Назад к меню движения', '🔙 Назад к типам задач',
            '🔙 Назад к примерам', '🔙 Назад к урокам', '📖 Урок 1: Основные формулы',
            '📖 Урок 2: Движение навстречу', '📖 Урок 3: Движение вдогонку',
            '🚗 Пример 1: Два автомобиля', '🚂 Пример 2: Поезд и мост', '🚢 Пример 3: Два теплохода',
            '🚶 Пример 4: Пешеход и велосипедист', '🏙️ Пример 5: А→Б→А со скоростью',
            '🏎️ Пример 6: Болиды по кругу', '🛶 Пример 7: Лодка по реке'
        ]

        # Если это НЕ системная кнопка, то это ответ пользователя
        if text not in системные_кнопки:
            уровень_соответствие = {
                'easy_simulator': 'легкий',
                'medium_simulator': 'средний',
                'hard_simulator': 'сложный',
                'random_simulator': 'случайные'
            }
            уровень = уровень_соответствие.get(current_submodule, 'легкий')
            handle_simulator_input(vk, user_id, text, уровень)
            return

    # ========== ГЛАВНОЕ МЕНЮ ДВИЖЕНИЯ ==========
    if text == '📚 Справочный материал':
        send_reference_material(vk, user_id)
    elif text == '📝 Примеры задач':
        show_examples_menu(vk, user_id)
    elif text == '🎓 Обучение':
        show_training_menu(vk, user_id)
    elif text == '🎯 Тренажер':
        show_simulator_menu(vk, user_id)

    # ========== ВЫБОР ПРИМЕРОВ ИЗ МЕНЮ (7 КНОПОК) ==========
    elif text == '🚗 Пример 1: Два автомобиля':
        send_example_1(vk, user_id)
    elif text == '🚂 Пример 2: Поезд и мост':
        send_example_2(vk, user_id)
    elif text == '🚢 Пример 3: Два теплохода':
        send_example_3(vk, user_id)
    elif text == '🚶 Пример 4: Пешеход и велосипедист':
        send_example_4(vk, user_id)
    elif text == '🏙️ Пример 5: А→Б→А со скоростью':
        send_example_5(vk, user_id)
    elif text == '🏎️ Пример 6: Болиды по кругу':
        send_example_6(vk, user_id)
    elif text == '🛶 Пример 7: Лодка по реке':
        send_example_7(vk, user_id)

    # ========== ТРЕНАЖЕР УРОВНЕЙ ==========
    elif text == '🟢 Легкий уровень':
        start_easy_simulator(vk, user_id)
    elif text == '🟡 Средний уровень':
        start_medium_simulator(vk, user_id)
    elif text == '🔴 Сложный уровень':
        start_hard_simulator(vk, user_id)
    elif text == '🎲 Случайная задача':
        start_random_simulator(vk, user_id)

    # ========== КНОПКИ В ТРЕНАЖЕРЕ ==========
    elif text == '💡 Подсказка' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator',
                                                         'random_simulator']:
        send_simulator_hint(vk, user_id)
    elif text == '📝 Показать ответ' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator',
                                                              'random_simulator']:
        show_simulator_answer(vk, user_id)
    elif text == '➡️ Следующая задача' and current_submodule in ['easy_simulator', 'medium_simulator',
                                                                 'hard_simulator']:
        next_simulator_task(vk, user_id)
    elif text == '🔄 Новая задача' and current_submodule == 'random_simulator':
        next_simulator_task(vk, user_id)

    # ========== НАВИГАЦИЯ В УРОКАХ ==========
    elif text == '➡️ Следующий урок' and current_submodule == 'viewing_lesson':
        current_lesson = user_state.get('current_lesson', 1)
        next_lesson = current_lesson + 1 if current_lesson < 3 else 1
        send_lesson(vk, user_id, next_lesson)
    elif text == '⬅️ Предыдущий урок' and current_submodule == 'viewing_lesson':
        current_lesson = user_state.get('current_lesson', 1)
        prev_lesson = current_lesson - 1 if current_lesson > 1 else 3
        send_lesson(vk, user_id, prev_lesson)

    # ========== ВЫБОР УРОКОВ ==========
    elif text == '📖 Урок 1: Основные формулы':
        send_lesson(vk, user_id, 1)
    elif text == '📖 Урок 2: Движение навстречу':
        send_lesson(vk, user_id, 2)
    elif text == '📖 Урок 3: Движение вдогонку':
        send_lesson(vk, user_id, 3)

    else:
        # Если сообщение не распознано, показываем главное меню движения
        show_movement_main_menu(vk, user_id)