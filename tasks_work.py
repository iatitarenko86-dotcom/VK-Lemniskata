# tasks_work.py
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from user_states import set_user_state, get_user_state, update_user_data


def create_keyboard(buttons, one_time=False):
    """Создание клавиатуры VK"""
    keyboard = VkKeyboard(one_time=one_time)

    for button in buttons:
        if button == "🔙 Назад" or button == "🔙 В меню":
            keyboard.add_button(button, color=VkKeyboardColor.SECONDARY)
        else:
            keyboard.add_button(button, color=VkKeyboardColor.PRIMARY)

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


def start_work_tasks(vk, user_id, user_data):
    """Начинает работу с задачами на работу"""
    buttons = ['🔙 Назад']
    keyboard = create_keyboard(buttons)

    text = """🛠️ Задачи на работу

Этот раздел находится в разработке.
Скоро здесь появятся интересные задачи!"""

    send_message(vk, user_id, text, keyboard)
    set_user_state(user_id, 'work_tasks', 'main_menu')


def handle_work_tasks(vk, user_id, text, user_data):
    """Обрабатывает сообщения в модуле задач на работу"""
    if text == '🔙 Назад':
        from main import show_text_tasks_menu
        show_text_tasks_menu(vk, user_id)
    else:
        start_work_tasks(vk, user_id, user_data)