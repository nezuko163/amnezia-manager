from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards import clients_list_kb, client_actions_kb, confirm_delete_kb, main_menu_kb

router = Router()

# --- FSM ---
class AddClientFSM(StatesGroup):
    waiting_name = State()

# --- Заглушки (потом заменим реальными вызовами) ---
def get_clients() -> list:
    """Возвращает [(display_name, ip, safe_name), ...]"""
    return [
        ("Мой телефон", "10.8.0.2", "client_мой_телефон"),
        ("Мой мак", "10.8.0.3", "client_мой_мак"),
        ("Оля ноут", None, "client_оля_ноут"),
    ]

def get_client_info(safe_name: str) -> dict:
    return {
        "display": "Мой телефон",
        "ip": "10.8.0.2",
        "endpoint": "1.2.3.4:51820",
        "handshake": "2 минуты назад",
        "transfer": "10 MB ↓ / 2 MB ↑",
        "public_key": "ABC123...",
    }

def get_client_conf(safe_name: str) -> str:
    return "[Interface]\nPrivateKey = ...\nAddress = 10.8.0.2/32\n\n[Peer]\nPublicKey = ..."

def get_client_link(safe_name: str) -> str:
    return "vpn://BASE64ENCODEDCONF?name=МойТелефон"

# --- Handlers ---

@router.callback_query(F.data == "list_clients")
async def list_clients(callback: CallbackQuery):
    clients = get_clients()
    if not clients:
        await callback.message.edit_text("📋 Клиентов нет", reply_markup=main_menu_kb())
        return
    await callback.message.edit_text("📋 Список клиентов:", reply_markup=clients_list_kb(clients))

@router.callback_query(F.data == "add_client")
async def add_client_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddClientFSM.waiting_name)
    await callback.message.edit_text("✏️ Введи название устройства:")

@router.message(AddClientFSM.waiting_name)
async def add_client_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("❌ Название не может быть пустым")
        return
    await state.clear()
    # TODO: вызов awg-add-client
    await message.answer(
        f"✅ Клиент <b>{name}</b> создан!\n\n"
        f"IP: <code>10.8.0.X</code>\n\n"
        f"<code>vpn://...</code>",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data.startswith("client_action:"))
async def client_action(callback: CallbackQuery):
    safe_name = callback.data.split(":", 1)[1]
    info = get_client_info(safe_name)
    text = f"👤 <b>{info['display']}</b>\nIP: <code>{info['ip']}</code>"
    await callback.message.edit_text(text, parse_mode="HTML",
                                     reply_markup=client_actions_kb(safe_name))

@router.callback_query(F.data.startswith("client_info:"))
async def client_info(callback: CallbackQuery):
    safe_name = callback.data.split(":", 1)[1]
    info = get_client_info(safe_name)
    text = (
        f"👤 <b>{info['display']}</b>\n"
        f"IP: <code>{info['ip']}</code>\n"
        f"Endpoint: <code>{info['endpoint']}</code>\n"
        f"Handshake: {info['handshake']}\n"
        f"Трафик: {info['transfer']}\n"
        f"Public key: <code>{info['public_key']}</code>"
    )
    await callback.message.edit_text(text, parse_mode="HTML",
                                     reply_markup=client_actions_kb(safe_name))

@router.callback_query(F.data.startswith("client_conf:"))
async def client_conf(callback: CallbackQuery):
    safe_name = callback.data.split(":", 1)[1]
    conf = get_client_conf(safe_name)
    await callback.message.edit_text(
        f"📄 Конфиг:\n<pre>{conf}</pre>",
        parse_mode="HTML",
        reply_markup=client_actions_kb(safe_name)
    )

@router.callback_query(F.data.startswith("client_link:"))
async def client_link(callback: CallbackQuery):
    safe_name = callback.data.split(":", 1)[1]
    link = get_client_link(safe_name)
    await callback.message.edit_text(
        f"🔗 VPN ссылка:\n<code>{link}</code>",
        parse_mode="HTML",
        reply_markup=client_actions_kb(safe_name)
    )

@router.callback_query(F.data.startswith("client_delete:"))
async def client_delete_confirm(callback: CallbackQuery):
    safe_name = callback.data.split(":", 1)[1]
    info = get_client_info(safe_name)
    await callback.message.edit_text(
        f"🗑️ Удалить <b>{info['display']}</b>?",
        parse_mode="HTML",
        reply_markup=confirm_delete_kb(safe_name)
    )

@router.callback_query(F.data.startswith("client_delete_confirm:"))
async def client_delete_do(callback: CallbackQuery):
    safe_name = callback.data.split(":", 1)[1]
    info = get_client_info(safe_name)
    # TODO: вызов awg-remove-client
    await callback.message.edit_text(
        f"✅ Клиент <b>{info['display']}</b> удалён",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )