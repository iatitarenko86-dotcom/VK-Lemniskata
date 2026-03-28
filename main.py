# main.py
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import tasks_movement
import tasks_work
import tasks_concentration
import tasks_percentage
import random
import sys
import logging

# Импортируем функции управления состояниями из отдельного модуля
from user_states import set_user_state, get_user_state, get_current_module, get_current_submodule, update_user_data

# ==================== НАСТРОЙКИ БОТА ====================
VK_TOKEN = "vk1.a.1Cc1AmWfxFj2cJKCrf3Ld0qt9SK2aB7GNAwpytcqagDAaPnnmMV_Zqh-ErurdR-aNC3cPAn0viRAiBE9GxZ6AyJFZaQeVPOiTebNIPFCAxndkwASigcx13QbzGa89U9AyMs2nxhcEqi8NGO7u-mDPXhaDj3X3GjZSiq7g7B87mQkKN7jV-l7S_pIZKQGjMe7AZAvWU9WDp_PqIUN5dQl9Q"
GROUP_ID = 237129293
LOG_LEVEL = "INFO"
MAX_MESSAGE_LENGTH = 4096
API_VERSION = "5.131"

# ==================== НАСТРОЙКА ЛОГИРОВАНИЯ ====================
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== ИНИЦИАЛИЗАЦИЯ VK ====================
def init_vk():
    """Инициализация подключения к VK"""
    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN, api_version=API_VERSION)
        vk = vk_session.get_api()

        group_info = vk.groups.getById(group_id=GROUP_ID)
        logger.info(f"✅ Подключение к ВК успешно")
        logger.info(f"📱 Сообщество: {group_info[0]['name']} (ID: {group_info[0]['id']})")

        return vk_session, vk

    except Exception as e:
        logger.error(f"❌ Ошибка подключения к ВК: {e}")
        sys.exit(1)

# Инициализация
vk_session, vk = init_vk()

# Инициализация Long Poll
try:
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    logger.info("✅ Long Poll успешно запущен")
except Exception as e:
    logger.error(f"❌ Ошибка инициализации Long Poll: {e}")
    sys.exit(1)

# Словарь для хранения данных пользователей
user_data = {}

# ==================== СЛОВАРЬ НАЗВАНИЙ КНОПОК ====================
BUTTONS = {
    "back": "🔙 Назад",
    "back_to_main": "🔙 В меню",
    "back_to_types": "🔙 К задачам",
    "back_to_menu": "🔙 В меню",
    "back_to_simulator": "🔙 К тренажеру",
    "back_to_examples": "🔙 К примерам",
    "back_to_lessons": "🔙 К урокам",
    "text_tasks": "📝 Задачи",
    "section2": "📚 Раздел 2",
    "help": "❓ Помощь",
    "movement": "🚗 Движение",
    "work": "🛠️ Работа",
    "concentration": "🧪 Концентрация",
    "percentage": "📊 Проценты",
    "reference": "📚 Справка",
    "examples": "📝 Примеры",
    "training": "🎓 Обучение",
    "simulator": "🎯 Тренажер",
    "easy": "🟢 Легкий",
    "medium": "🟡 Средний",
    "hard": "🔴 Сложный",
    "random": "🎲 Случайно",
    "hint": "💡 Подсказка",
    "answer": "📝 Ответ",
    "next_task": "➡️ Далее",
    "new_task": "🔄 Новая",
    "prev_lesson": "⬅️ Назад",
    "next_lesson": "➡️ Далее",
    "example_1": "📖 Пример 1",
    "example_2": "📖 Пример 2",
    "example_3": "📖 Пример 3",
    "example_4": "📖 Пример 4",
    "example_5": "📖 Пример 5",
    "example_6": "📖 Пример 6",
    "example_7": "📖 Пример 7",
    "lesson_1": "📖 Урок 1",
    "lesson_2": "📖 Урок 2",
    "lesson_3": "📖 Урок 3",
}

# ==================== ФУНКЦИИ ДЛЯ КЛАВИАТУР ====================
def create_keyboard(buttons, one_time=False, columns=2):
    """Создание клавиатуры VK"""
    keyboard = VkKeyboard(one_time=one_time)

    for i, button in enumerate(buttons):
        if "Назад" in button or "В меню" in button or "К задачам" in button:
            color = VkKeyboardColor.SECONDARY
        elif button.startswith("🟢"):
            color = VkKeyboardColor.POSITIVE
        elif button.startswith("🔴"):
            color = VkKeyboardColor.NEGATIVE
        else:
            color = VkKeyboardColor.PRIMARY

        keyboard.add_button(button, color=color)

        if (i + 1) % columns == 0 and i < len(buttons) - 1:
            keyboard.add_line()

    return keyboard.get_keyboard()


def send_message(user_id, text, keyboard=None):
    """Отправка сообщения"""
    try:
        params = {
            'user_id': user_id,
            'message': text[:MAX_MESSAGE_LENGTH],
            'random_id': random.randint(1, 2 ** 31)
        }

        if keyboard:
            params['keyboard'] = keyboard

        vk.messages.send(**params)
        logger.debug(f"✅ Сообщение отправлено {user_id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения {user_id}: {e}")
        return False


# ==================== МЕНЮ ====================
def show_main_menu(user_id, show_welcome=False):
    """Отображает главное меню"""
    buttons = [BUTTONS["text_tasks"], BUTTONS["section2"], BUTTONS["help"]]
    keyboard = create_keyboard(buttons, columns=2)

    if show_welcome:
        text = """👋 Добро пожаловать в бот-тренажер! 📚

Здесь вы можете тренироваться в решении текстовых задач по математике.

🏠 Главное меню
Выберите раздел:"""
    else:
        text = "🏠 Главное меню\n\nВыберите раздел:"

    send_message(user_id, text, keyboard)
    set_user_state(user_id, 'main_menu', '')


def show_text_tasks_menu(user_id):
    """Отображает меню текстовых задач"""
    buttons = [
        BUTTONS["movement"],
        BUTTONS["work"],
        BUTTONS["concentration"],
        BUTTONS["percentage"],
        BUTTONS["back_to_main"]
    ]
    keyboard = create_keyboard(buttons, columns=2)

    text = "📝 Текстовые задачи\n\nВыберите тип задач:"
    send_message(user_id, text, keyboard)
    set_user_state(user_id, 'text_tasks_menu', '')


def show_help(user_id):
    """Показывает справку"""
    text = """ℹ️ Помощь по боту-тренажеру

1️⃣ Начало работы: Напишите любое сообщение для отображения меню
2️⃣ Навигация: Используйте кнопки для перехода между разделами
3️⃣ Задачи: Выберите тип задач для тренировки
4️⃣ Уровни: Легкий, Средний, Сложный или Случайный
5️⃣ Управление: Подсказка, Ответ, Новая задача

Для возврата в главное меню используйте кнопку '🔙 Назад'"""
    send_message(user_id, text)


def show_section2(user_id):
    """Показывает раздел 2"""
    text = """📚 Раздел 2

Этот раздел находится в разработке...
Скоро здесь появятся новые материалы!

🔜 Следите за обновлениями!"""
    send_message(user_id, text)


# ==================== МЕНЮ ДЛЯ МОДУЛЕЙ ====================
def show_movement_main_menu(vk, user_id):
    """Меню задач на движение"""
    keyboard = VkKeyboard()
    keyboard.add_button('📚 Справка', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📝 Примеры', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎓 Обучение', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🎯 Тренажер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)

    text = """🚗 Задачи на движение

Выберите раздел для изучения:
• 📚 Справка - формулы и теория
• 📝 Примеры - готовые решения
• 🎓 Обучение - пошаговое изучение
• 🎯 Тренажер - практические задания"""

    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'main_menu')


def show_concentration_main_menu(vk, user_id):
    """Меню задач на концентрацию"""
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

    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'main_menu')


def show_percentage_main_menu(vk, user_id):
    """Меню задач на проценты"""
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

    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'main_menu')


def show_work_main_menu(vk, user_id):
    """Меню задач на работу"""
    text = """🛠️ Задачи на работу

Этот раздел находится в разработке."""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)
    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'work_tasks', 'main_menu')


# ==================== ОБРАБОТЧИК СООБЩЕНИЙ ====================
def handle_message(event):
    """Обрабатывает входящие сообщения"""
    user_id = event.obj.message['from_id']
    text = event.obj.message['text'].strip()

    logger.info(f"📨 Сообщение от {user_id}: {text[:50]}")

    # Инициализация пользователя
    if user_id not in user_data:
        user_data[user_id] = {}

    current_module = get_current_module(user_id)

    # Кнопка "Назад в главное меню"
    if text == BUTTONS["back_to_main"]:
        show_main_menu(user_id)
        return

    # Обработка модулей
    if current_module == 'movement_tasks':
        try:
            tasks_movement.handle_movement_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле движения: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'concentration_tasks':
        try:
            tasks_concentration.handle_concentration_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле концентрации: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'percentage_tasks':
        try:
            tasks_percentage.handle_percentage_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле процентов: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'work_tasks':
        try:
            tasks_work.handle_work_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле работы: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'text_tasks_menu':
        handle_text_tasks_menu(user_id, text)

    elif current_module in ['main_menu', '']:
        handle_main_menu(user_id, text)

    else:
        show_main_menu(user_id)


def handle_main_menu(user_id, text):
    """Обрабатывает сообщения в главном меню"""
    if text == BUTTONS["text_tasks"]:
        show_text_tasks_menu(user_id)
    elif text == BUTTONS["section2"]:
        show_section2(user_id)
    elif text == BUTTONS["help"]:
        show_help(user_id)
    else:
        show_main_menu(user_id)


def handle_text_tasks_menu(user_id, text):
    """Обрабатывает сообщения в меню текстовых задач"""
    if text == BUTTONS["movement"]:
        show_movement_main_menu(vk, user_id)
    elif text == BUTTONS["work"]:
        show_work_main_menu(vk, user_id)
    elif text == BUTTONS["concentration"]:
        show_concentration_main_menu(vk, user_id)
    elif text == BUTTONS["percentage"]:
        show_percentage_main_menu(vk, user_id)
    else:
        show_text_tasks_menu(user_id)


# ==================== ЗАПУСК БОТА ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот-тренажер ВКонтакте")
    print("=" * 50)
    print(f"📱 ID сообщества: {GROUP_ID}")
    print("📡 Ожидание сообщений...")
    print("=" * 50)

    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['from_id'] > 0:
                    handle_message(event)
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")# main.py
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import tasks_movement
import tasks_work
import tasks_concentration
import tasks_percentage
import random
import sys
import logging

# Импортируем функции управления состояниями из отдельного модуля
from user_states import set_user_state, get_user_state, get_current_module, get_current_submodule, update_user_data

# ==================== НАСТРОЙКИ БОТА ====================
VK_TOKEN = "vk1.a.1Cc1AmWfxFj2cJKCrf3Ld0qt9SK2aB7GNAwpytcqagDAaPnnmMV_Zqh-ErurdR-aNC3cPAn0viRAiBE9GxZ6AyJFZaQeVPOiTebNIPFCAxndkwASigcx13QbzGa89U9AyMs2nxhcEqi8NGO7u-mDPXhaDj3X3GjZSiq7g7B87mQkKN7jV-l7S_pIZKQGjMe7AZAvWU9WDp_PqIUN5dQl9Q"
GROUP_ID = 237129293
LOG_LEVEL = "INFO"
MAX_MESSAGE_LENGTH = 4096
API_VERSION = "5.131"

# ==================== НАСТРОЙКА ЛОГИРОВАНИЯ ====================
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== ИНИЦИАЛИЗАЦИЯ VK ====================
def init_vk():
    """Инициализация подключения к VK"""
    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN, api_version=API_VERSION)
        vk = vk_session.get_api()

        group_info = vk.groups.getById(group_id=GROUP_ID)
        logger.info(f"✅ Подключение к ВК успешно")
        logger.info(f"📱 Сообщество: {group_info[0]['name']} (ID: {group_info[0]['id']})")

        return vk_session, vk

    except Exception as e:
        logger.error(f"❌ Ошибка подключения к ВК: {e}")
        sys.exit(1)

# Инициализация
vk_session, vk = init_vk()

# Инициализация Long Poll
try:
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    logger.info("✅ Long Poll успешно запущен")
except Exception as e:
    logger.error(f"❌ Ошибка инициализации Long Poll: {e}")
    sys.exit(1)

# Словарь для хранения данных пользователей
user_data = {}

# ==================== СЛОВАРЬ НАЗВАНИЙ КНОПОК ====================
BUTTONS = {
    "back": "🔙 Назад",
    "back_to_main": "🔙 В меню",
    "back_to_types": "🔙 К задачам",
    "back_to_menu": "🔙 В меню",
    "back_to_simulator": "🔙 К тренажеру",
    "back_to_examples": "🔙 К примерам",
    "back_to_lessons": "🔙 К урокам",
    "text_tasks": "📝 Задачи",
    "section2": "📚 Раздел 2",
    "help": "❓ Помощь",
    "movement": "🚗 Движение",
    "work": "🛠️ Работа",
    "concentration": "🧪 Концентрация",
    "percentage": "📊 Проценты",
    "reference": "📚 Справка",
    "examples": "📝 Примеры",
    "training": "🎓 Обучение",
    "simulator": "🎯 Тренажер",
    "easy": "🟢 Легкий",
    "medium": "🟡 Средний",
    "hard": "🔴 Сложный",
    "random": "🎲 Случайно",
    "hint": "💡 Подсказка",
    "answer": "📝 Ответ",
    "next_task": "➡️ Далее",
    "new_task": "🔄 Новая",
    "prev_lesson": "⬅️ Назад",
    "next_lesson": "➡️ Далее",
    "example_1": "📖 Пример 1",
    "example_2": "📖 Пример 2",
    "example_3": "📖 Пример 3",
    "example_4": "📖 Пример 4",
    "example_5": "📖 Пример 5",
    "example_6": "📖 Пример 6",
    "example_7": "📖 Пример 7",
    "lesson_1": "📖 Урок 1",
    "lesson_2": "📖 Урок 2",
    "lesson_3": "📖 Урок 3",
}

# ==================== ФУНКЦИИ ДЛЯ КЛАВИАТУР ====================
def create_keyboard(buttons, one_time=False, columns=2):
    """Создание клавиатуры VK"""
    keyboard = VkKeyboard(one_time=one_time)

    for i, button in enumerate(buttons):
        if "Назад" in button or "В меню" in button or "К задачам" in button:
            color = VkKeyboardColor.SECONDARY
        elif button.startswith("🟢"):
            color = VkKeyboardColor.POSITIVE
        elif button.startswith("🔴"):
            color = VkKeyboardColor.NEGATIVE
        else:
            color = VkKeyboardColor.PRIMARY

        keyboard.add_button(button, color=color)

        if (i + 1) % columns == 0 and i < len(buttons) - 1:
            keyboard.add_line()

    return keyboard.get_keyboard()


def send_message(user_id, text, keyboard=None):
    """Отправка сообщения"""
    try:
        params = {
            'user_id': user_id,
            'message': text[:MAX_MESSAGE_LENGTH],
            'random_id': random.randint(1, 2 ** 31)
        }

        if keyboard:
            params['keyboard'] = keyboard

        vk.messages.send(**params)
        logger.debug(f"✅ Сообщение отправлено {user_id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения {user_id}: {e}")
        return False


# ==================== МЕНЮ ====================
def show_main_menu(user_id, show_welcome=False):
    """Отображает главное меню"""
    buttons = [BUTTONS["text_tasks"], BUTTONS["section2"], BUTTONS["help"]]
    keyboard = create_keyboard(buttons, columns=2)

    if show_welcome:
        text = """👋 Добро пожаловать в бот-тренажер! 📚

Здесь вы можете тренироваться в решении текстовых задач по математике.

🏠 Главное меню
Выберите раздел:"""
    else:
        text = "🏠 Главное меню\n\nВыберите раздел:"

    send_message(user_id, text, keyboard)
    set_user_state(user_id, 'main_menu', '')


def show_text_tasks_menu(user_id):
    """Отображает меню текстовых задач"""
    buttons = [
        BUTTONS["movement"],
        BUTTONS["work"],
        BUTTONS["concentration"],
        BUTTONS["percentage"],
        BUTTONS["back_to_main"]
    ]
    keyboard = create_keyboard(buttons, columns=2)

    text = "📝 Текстовые задачи\n\nВыберите тип задач:"
    send_message(user_id, text, keyboard)
    set_user_state(user_id, 'text_tasks_menu', '')


def show_help(user_id):
    """Показывает справку"""
    text = """ℹ️ Помощь по боту-тренажеру

1️⃣ Начало работы: Напишите любое сообщение для отображения меню
2️⃣ Навигация: Используйте кнопки для перехода между разделами
3️⃣ Задачи: Выберите тип задач для тренировки
4️⃣ Уровни: Легкий, Средний, Сложный или Случайный
5️⃣ Управление: Подсказка, Ответ, Новая задача

Для возврата в главное меню используйте кнопку '🔙 Назад'"""
    send_message(user_id, text)


def show_section2(user_id):
    """Показывает раздел 2"""
    text = """📚 Раздел 2

Этот раздел находится в разработке...
Скоро здесь появятся новые материалы!

🔜 Следите за обновлениями!"""
    send_message(user_id, text)


# ==================== МЕНЮ ДЛЯ МОДУЛЕЙ ====================
def show_movement_main_menu(vk, user_id):
    """Меню задач на движение"""
    keyboard = VkKeyboard()
    keyboard.add_button('📚 Справка', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📝 Примеры', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🎓 Обучение', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🎯 Тренажер', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)

    text = """🚗 Задачи на движение

Выберите раздел для изучения:
• 📚 Справка - формулы и теория
• 📝 Примеры - готовые решения
• 🎓 Обучение - пошаговое изучение
• 🎯 Тренажер - практические задания"""

    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'movement_tasks', 'main_menu')


def show_concentration_main_menu(vk, user_id):
    """Меню задач на концентрацию"""
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

    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'concentration_tasks', 'main_menu')


def show_percentage_main_menu(vk, user_id):
    """Меню задач на проценты"""
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

    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'percentage_tasks', 'main_menu')


def show_work_main_menu(vk, user_id):
    """Меню задач на работу"""
    text = """🛠️ Задачи на работу

Этот раздел находится в разработке."""
    keyboard = VkKeyboard()
    keyboard.add_button('🔙 Назад к типам задач', color=VkKeyboardColor.SECONDARY)
    send_message(user_id, text, keyboard.get_keyboard())
    set_user_state(user_id, 'work_tasks', 'main_menu')


# ==================== ОБРАБОТЧИК СООБЩЕНИЙ ====================
def handle_message(event):
    """Обрабатывает входящие сообщения"""
    user_id = event.obj.message['from_id']
    text = event.obj.message['text'].strip()

    logger.info(f"📨 Сообщение от {user_id}: {text[:50]}")

    # Инициализация пользователя
    if user_id not in user_data:
        user_data[user_id] = {}

    current_module = get_current_module(user_id)

    # Кнопка "Назад в главное меню"
    if text == BUTTONS["back_to_main"]:
        show_main_menu(user_id)
        return

    # Обработка модулей
    if current_module == 'movement_tasks':
        try:
            tasks_movement.handle_movement_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле движения: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'concentration_tasks':
        try:
            tasks_concentration.handle_concentration_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле концентрации: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'percentage_tasks':
        try:
            tasks_percentage.handle_percentage_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле процентов: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'work_tasks':
        try:
            tasks_work.handle_work_tasks(vk, user_id, text, user_data)
        except Exception as e:
            logger.error(f"Ошибка в модуле работы: {e}")
            send_message(user_id, f"❌ Ошибка: {str(e)}")
            show_text_tasks_menu(user_id)

    elif current_module == 'text_tasks_menu':
        handle_text_tasks_menu(user_id, text)

    elif current_module in ['main_menu', '']:
        handle_main_menu(user_id, text)

    else:
        show_main_menu(user_id)


def handle_main_menu(user_id, text):
    """Обрабатывает сообщения в главном меню"""
    if text == BUTTONS["text_tasks"]:
        show_text_tasks_menu(user_id)
    elif text == BUTTONS["section2"]:
        show_section2(user_id)
    elif text == BUTTONS["help"]:
        show_help(user_id)
    else:
        show_main_menu(user_id)


def handle_text_tasks_menu(user_id, text):
    """Обрабатывает сообщения в меню текстовых задач"""
    if text == BUTTONS["movement"]:
        show_movement_main_menu(vk, user_id)
    elif text == BUTTONS["work"]:
        show_work_main_menu(vk, user_id)
    elif text == BUTTONS["concentration"]:
        show_concentration_main_menu(vk, user_id)
    elif text == BUTTONS["percentage"]:
        show_percentage_main_menu(vk, user_id)
    else:
        show_text_tasks_menu(user_id)


# ==================== ЗАПУСК БОТА ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Бот-тренажер ВКонтакте")
    print("=" * 50)
    print(f"📱 ID сообщества: {GROUP_ID}")
    print("📡 Ожидание сообщений...")
    print("=" * 50)

    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['from_id'] > 0:
                    handle_message(event)
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
