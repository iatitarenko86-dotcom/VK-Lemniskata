# user_states.py
"""
Модуль для управления состояниями пользователей.
Хранит информацию о текущем модуле и подмодуле, в котором находится пользователь.
"""

user_states = {}


def set_user_state(user_id, module, sub_module=None, additional_data=None):
    """Устанавливает состояние пользователя
    
    Args:
        user_id: ID пользователя ВКонтакте
        module: Название модуля (например, 'movement_tasks', 'concentration_tasks')
        sub_module: Название подмодуля (например, 'easy_simulator', 'main_menu')
        additional_data: Дополнительные данные (словарь)
    """
    if user_id not in user_states:
        user_states[user_id] = {}
    
    # Сохраняем текущий модуль
    user_states[user_id]['current_module'] = module
    
    # Сохраняем подмодуль если передан
    if sub_module:
        user_states[user_id]['sub_module'] = sub_module
    
    # Сохраняем дополнительные данные
    if additional_data:
        user_states[user_id].update(additional_data)


def get_user_state(user_id):
    """Получает состояние пользователя
    
    Returns:
        dict: Словарь с данными пользователя, или пустой словарь, если пользователь не найден
    """
    return user_states.get(user_id, {})


def get_current_module(user_id):
    """Получает текущий модуль пользователя
    
    Returns:
        str: Название текущего модуля, или пустая строка, если пользователь не найден
    """
    return user_states.get(user_id, {}).get('current_module', '')


def get_current_submodule(user_id):
    """Получает текущий подмодуль пользователя
    
    Returns:
        str: Название текущего подмодуля, или пустая строка, если пользователь не найден
    """
    return user_states.get(user_id, {}).get('sub_module', '')


def update_user_data(user_id, data):
    """Обновляет дополнительные данные пользователя
    
    Args:
        user_id: ID пользователя ВКонтакте
        data: Словарь с данными для обновления
    """
    if user_id not in user_states:
        user_states[user_id] = {}
    
    user_states[user_id].update(data)


def get_user_data(user_id, key=None):
    """Получает данные пользователя
    
    Args:
        user_id: ID пользователя ВКонтакте
        key: Ключ для получения конкретного значения (опционально)
    
    Returns:
        Если key указан: значение по ключу или None
        Если key не указан: весь словарь данных пользователя или пустой словарь
    """
    if user_id not in user_states:
        return None if key else {}
    
    if key:
        return user_states[user_id].get(key)
    
    return user_states[user_id]


def clear_user_state(user_id):
    """Очищает состояние пользователя"""
    if user_id in user_states:
        del user_states[user_id]


def is_user_in_module(user_id, module):
    """Проверяет, находится ли пользователь в указанном модуле"""
    return get_current_module(user_id) == module


def is_user_in_submodule(user_id, submodule):
    """Проверяет, находится ли пользователь в указанном подмодуле"""
    return get_current_submodule(user_id) == submodule


def reset_user_state(user_id):
    """Сбрасывает состояние пользователя (очищает все данные)"""
    if user_id in user_states:
        user_states[user_id] = {}
    else:
        user_states[user_id] = {}


def get_all_user_states():
    """Возвращает все состояния пользователей (для отладки)"""
    return user_states


def get_user_count():
    """Возвращает количество активных пользователей"""
    return len(user_states)