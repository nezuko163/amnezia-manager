from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards import server_menu_kb, main_menu_kb

router = Router()

def get_server_status() -> str:
    # TODO: реальная проверка
    return "🟢 Запущен (порт 51820)"

@router.callback_query(F.data == "server_menu")
async def server_menu(callback: CallbackQuery):
    status = get_server_status()
    await callback.message.edit_text(
        f"🖥️ Управление сервером\n\nСтатус: {status}",
        reply_markup=server_menu_kb()
    )

@router.callback_query(F.data == "server_start")
async def server_start(callback: CallbackQuery):
    # TODO: awg-quick up
    await callback.message.edit_text(
        "▶️ Сервер запускается...\n\nСтатус: 🟢 Запущен",
        reply_markup=server_menu_kb()
    )

@router.callback_query(F.data == "server_restart")
async def server_restart(callback: CallbackQuery):
    # TODO: awg-quick down + up
    await callback.message.edit_text(
        "🔄 Сервер перезапущен\n\nСтатус: 🟢 Запущен",
        reply_markup=server_menu_kb()
    )

@router.callback_query(F.data == "server_stop")
async def server_stop(callback: CallbackQuery):
    # TODO: awg-quick down
    await callback.message.edit_text(
        "⏹️ Сервер остановлен\n\nСтатус: 🔴 Остановлен",
        reply_markup=server_menu_kb()
    )

@router.callback_query(F.data == "server_status")
async def server_status(callback: CallbackQuery):
    # TODO: awg show
    text = (
        "📊 Статус сервера:\n\n"
        "Интерфейс: awg0\n"
        "Порт: 51820\n"
        "IP Forwarding: 🟢\n"
        "Клиентов онлайн: 3"
    )
    await callback.message.edit_text(text, reply_markup=server_menu_kb())

@router.callback_query(F.data == "server_fix")
async def server_fix(callback: CallbackQuery):
    # TODO: починка forwarding + firewall + restart
    await callback.message.edit_text(
        "🔧 Применяю исправления...\n\n"
        "✅ IP Forwarding включён\n"
        "✅ Порт 51820 открыт\n"
        "✅ Сервер перезапущен",
        reply_markup=server_menu_kb()
    )