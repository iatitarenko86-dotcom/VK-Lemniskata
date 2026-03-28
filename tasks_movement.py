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

    MAX_BUTTONS_PER_ROW = 4

    for i, button in enumerate(buttons):
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


# ==================== ГЛАВНОЕ МЕНЮ ДВИЖЕНИЯ ====================
def show_movement_main_menu(vk, user_id):
    """Отображает главное меню задач на движение"""
    keyboard = VkKeyboard()

    keyboard.add_button('📚 Справочный материал', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📝 Примеры задач', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎓 Обучение', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🎯 Тренажер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)

    text = """🚗 Задачи на движение

Выберите раздел для изучения:

• 📚 Справочный материал - формулы и теория
• 📝 Примеры задач - готовые решения
• 🎓 Обучение - пошаговое изучение
• 🎯 Тренажер - практические задания"""

    send_message(vk, user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'main_menu')


def start_movement_tasks(vk, user_id, user_data):
    """Начинает работу с задачами на движение"""
    show_movement_main_menu(vk, user_id)


# ==================== МЕНЮ ТРЕНАЖЕРА ====================
def show_simulator_menu(vk, user_id):
    """Отображает меню тренажера"""
    keyboard = VkKeyboard()

    keyboard.add_button('🟢 Легкий уровень', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('🟡 Средний уровень', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔴 Сложный уровень', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('🎲 Случайная задача', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
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

        уровень_данные = {
            'легкий': {'эмодзи': '🟢', 'текст': 'Легкий уровень тренажера'},
            'средний': {'эмодзи': '🟡', 'текст': 'Средний уровень тренажера'},
            'сложный': {'эмодзи': '🔴', 'текст': 'Сложный уровень тренажера'},
            'случайные': {'эмодзи': '🎲', 'текст': 'Случайная задача'}
        }

        данные_уровня = уровень_данные.get(уровень, {'эмодзи': '🎯', 'текст': 'Тренажер'})

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
                задача = тренажер.получить_текущую_задачу()

                send_message(vk, user_id,
                             f"{данные_уровня['эмодзи']} {данные_уровня['текст']}\n\n"
                             f"✅ Правильно!\n\n"
                             f"{задача}\n\n"
                             "Введите ответ в чат:",
                             keyboard.get_keyboard())
            else:
                if уровень != 'случайные':
                    final_keyboard = VkKeyboard()
                    final_keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

                    send_message(vk, user_id,
                                 f"✅ Поздравляем!\n\n"
                                 f"🎉 Вы успешно решили все задачи {уровень} уровня!\n\n"
                                 f"Можете вернуться в меню тренажера или выбрать другой уровень.",
                                 final_keyboard.get_keyboard())
                else:
                    задача = тренажер.получить_следующую_задачу()
                    send_message(vk, user_id,
                                 f"✅ Правильно!\n\n"
                                 f"🎲 Следующая случайная задача:\n\n"
                                 f"{задача}\n\n"
                                 "Введите ответ в чат:",
                                 keyboard.get_keyboard())
        else:
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
            if hasattr(тренажер, 'текущая_задача'):
                тренажер.текущая_задача += 1

            задача = тренажер.получить_текущую_задачу()

            keyboard = VkKeyboard()
            keyboard.add_button('💡 Подсказка', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('📝 Показать ответ', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('🔙 Назад к тренажеру', color=VkKeyboardColor.SECONDARY)

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
        "Основные формулы движения:\n"
        "• S = v × t - расстояние\n"
        "• v = S / t - скорость\n"
        "• t = S / v - время\n\n"
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


# ==================== МЕНЮ ПРИМЕРОВ ====================
def show_examples_menu(vk, user_id):
    """Отображает меню примеров задач"""
    keyboard = VkKeyboard()

    keyboard.add_button('🚗 Пример 1: Два автомобиля', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🚂 Пример 2: Поезд и мост', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🚢 Пример 3: Два теплохода', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🚶 Пример 4: Пешеход и велосипедист', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🏙️ Пример 5: А→Б→А со скоростью', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🏎️ Пример 6: Болиды по кругу', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🛶 Пример 7: Лодка по реке', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к меню движения', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id,
                 "📝 Примеры задач на движение\n\n"
                 "Выберите пример для изучения:",
                 keyboard.get_keyboard())

    set_user_state(user_id, 'movement_tasks', 'examples_menu')


# ==================== ПРИМЕРЫ ЗАДАЧ (сокращенные для краткости) ====================
def send_example_1(vk, user_id):
    example_text = """🚗 Пример 1: Два автомобиля

Условие: Из двух городов, расстояние между которыми 420 км, одновременно навстречу друг другу выехали два автомобиля. Скорость первого 60 км/ч, второго — 80 км/ч. Через сколько часов они встретятся?

Решение:
v = 60 + 80 = 140 км/ч
t = 420 / 140 = 3 часа

Ответ: через 3 часа"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_2(vk, user_id):
    example_text = """🚂 Пример 2: Поезд и мост

Условие: Поезд длиной 250 м проезжает мост длиной 150 м за 20 секунд. Найдите скорость поезда в км/ч.

Решение:
S = 250 + 150 = 400 м
v = 400 / 20 = 20 м/с
v = 20 × 3.6 = 72 км/ч

Ответ: 72 км/ч"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_3(vk, user_id):
    example_text = """🚢 Пример 3: Два теплохода

Условие: Два теплохода вышли одновременно навстречу друг другу из двух портов, расстояние между которыми 300 км. Скорость первого 20 км/ч, второго — 30 км/ч. Через сколько часов они встретятся?

Решение:
v = 20 + 30 = 50 км/ч
t = 300 / 50 = 6 часов

Ответ: через 6 часов"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_4(vk, user_id):
    example_text = """🚶 Пример 4: Пешеход и велосипедист

Условие: Из одной точки в противоположных направлениях одновременно вышли пешеход (5 км/ч) и велосипедист (15 км/ч). Какое расстояние будет между ними через 2 часа?

Решение:
v = 5 + 15 = 20 км/ч
S = 20 × 2 = 40 км

Ответ: 40 км"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_5(vk, user_id):
    example_text = """🏙️ Пример 5: А→Б→А со скоростью

Условие: Автомобиль выехал из А в Б (180 км). На обратном пути увеличил скорость на 5 км/ч и затратил на 24 минуты меньше. Найдите скорость из А в Б.

Решение:
Пусть x - скорость из А в Б
180/x - 180/(x+5) = 0.4
x² + 5x - 2250 = 0
x = 45

Ответ: 45 км/ч"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_6(vk, user_id):
    example_text = """🏎️ Пример 6: Болиды по кругу

Условие: Два болида стартуют из диаметрально противоположных точек круговой трассы (19.5 км). Скорость одного на 13 км/ч больше. Через сколько минут поравняются?

Решение:
S₀ = 19.5 / 2 = 9.75 км
t = 9.75 / 13 = 0.75 часа = 45 минут

Ответ: через 45 минут"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


def send_example_7(vk, user_id):
    example_text = """🛶 Пример 7: Лодка по реке

Условие: Лодка прошла 10 км по озеру и 4 км против течения (скорость течения 3 км/ч) за 1 час. Найдите собственную скорость.

Решение:
10/v + 4/(v-3) = 1
v² - 17v + 30 = 0
v = 15 (v=2 не подходит)

Ответ: 15 км/ч"""
    
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к примерам', color=VkKeyboardColor.SECONDARY)
    send_message(vk, user_id, example_text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_example')


# ==================== ОБУЧЕНИЕ ====================
def show_training_menu(vk, user_id):
    """Отображает меню обучения"""
    keyboard = VkKeyboard()

    keyboard.add_button('📖 Урок 1: Основные формулы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 2: Движение навстречу', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📖 Урок 3: Движение вдогонку', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к меню движения', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id,
                 "🎓 Обучение: Задачи на движение\n\n"
                 "Выберите урок для изучения:",
                 keyboard.get_keyboard())

    set_user_state(user_id, 'movement_tasks', 'training_menu')


def send_lesson(vk, user_id, lesson_number):
    """Отправляет урок"""
    lessons = {
        1: """📖 Урок 1: Основные формулы движения

Основные формулы:
• S = v × t - расстояние
• v = S / t - скорость
• t = S / v - время

Единицы измерения:
• 1 м/с = 3.6 км/ч
• 1 км/ч ≈ 0.278 м/с""",
        
        2: """📖 Урок 2: Движение навстречу друг другу

Формула скорости сближения:
v = v₁ + v₂

Формула времени встречи:
t = S / (v₁ + v₂)

Алгоритм:
1. Найти скорость сближения (сумма скоростей)
2. Разделить расстояние на скорость сближения
3. Получить время встречи""",
        
        3: """📖 Урок 3: Движение вдогонку

Формула скорости сближения:
v = v₁ - v₂ (если v₁ > v₂)

Формула времени сближения:
t = S₀ / (v₁ - v₂)

Алгоритм:
1. Найти начальное расстояние S₀
2. Найти скорость сближения (разность скоростей)
3. Разделить S₀ на скорость сближения"""
    }
    
    lesson_content = lessons.get(lesson_number, lessons[1])
    update_user_data(user_id, {'current_lesson': lesson_number})

    keyboard = VkKeyboard()
    keyboard.add_button('⬅️ Предыдущий урок', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('➡️ Следующий урок', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к урокам', color=VkKeyboardColor.SECONDARY)

    send_message(vk, user_id, lesson_content, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'viewing_lesson')


# ==================== ОСНОВНОЙ ОБРАБОТЧИК ====================
def handle_movement_tasks(vk, user_id, text, user_data):
    """Обрабатывает сообщения в модуле задач на движение"""
    user_state = get_user_state(user_id)
    current_submodule = user_state.get('sub_module', '')

    # ========== ОБРАБОТКА КНОПОК НАЗАД ==========
    if text == '🔙 Назад к типам задач':
        from main import show_text_tasks_menu
        show_text_tasks_menu(user_id)
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
        системные_кнопки = [
            '💡 Подсказка', '📝 Показать ответ', '🔙 Назад к тренажеру', '➡️ Следующая задача',
            '🔄 Новая задача', '📚 Справочный материал', '📝 Примеры задач', '🎓 Обучение',
            '🎯 Тренажер', '🟢 Легкий уровень', '🟡 Средний уровень', '🔴 Сложный уровень',
            '🎲 Случайная задача', '🔙 Назад к меню движения', '🔙 Назад к типам задач',
            '🔙 Назад к примерам', '🔙 Назад к урокам'
        ]

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

    # ========== ВЫБОР ПРИМЕРОВ ==========
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
    elif text == '💡 Подсказка' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
        send_simulator_hint(vk, user_id)
    elif text == '📝 Показать ответ' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator', 'random_simulator']:
        show_simulator_answer(vk, user_id)
    elif text == '➡️ Следующая задача' and current_submodule in ['easy_simulator', 'medium_simulator', 'hard_simulator']:
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
        show_movement_main_menu(vk, user_id)
