from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить клиента", callback_data="add_client")],
        [InlineKeyboardButton(text="📋 Список клиентов", callback_data="list_clients")],
        [InlineKeyboardButton(text="🗑️ Удалить клиента", callback_data="remove_client")],
        [InlineKeyboardButton(text="🖥️ Управление сервером", callback_data="server_menu")],
    ])

def server_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Запустить", callback_data="server_start")],
        [InlineKeyboardButton(text="🔄 Перезапустить", callback_data="server_restart")],
        [InlineKeyboardButton(text="⏹️ Остановить", callback_data="server_stop")],
        [InlineKeyboardButton(text="📊 Статус", callback_data="server_status")],
        [InlineKeyboardButton(text="🔧 Починить", callback_data="server_fix")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])

def client_actions_kb(safe_name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Получить ссылку", callback_data=f"client_link:{safe_name}")],
        [InlineKeyboardButton(text="👁️ Показать данные", callback_data=f"client_info:{safe_name}")],
        [InlineKeyboardButton(text="📄 Показать конфиг", callback_data=f"client_conf:{safe_name}")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"client_delete:{safe_name}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="list_clients")],
    ])

def confirm_delete_kb(safe_name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"client_delete_confirm:{safe_name}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data=f"client_action:{safe_name}"),
        ]
    ])

def clients_list_kb(clients: list):
    """clients = [(display_name, ip, safe_name), ...]"""
    buttons = []
    for display, ip, safe in clients:
        label = f"{display} | {ip or 'none'}"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"client_action:{safe}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)