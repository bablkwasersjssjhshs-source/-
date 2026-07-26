import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ChatMemberStatus

# --- НАСТРОЙКИ БОТА ---
BOT_TOKEN = "8644490388:AAED4r_yPSIvuvAHfW7Vockt984IuE2mezU"
CHANNEL_ID = "@твой_канал" 
CHANNEL_URL_1 = "https://t.me/+rm9ZM7u3KsBmZDRi" 
CHANNEL_URL_2 = "https://t.me/+eUKLegwNZLRhZjYx" 
OTHER_BOT_URL = "https://t.me/raivoeyebot?start=010858C5627474617466" # Ссылка на бота, которого нужно запустить

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для создания клавиатуры
def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            # Две кнопки на каналы в один ряд
            [
                InlineKeyboardButton(text="Подписаться (1)", url=CHANNEL_URL_1),
                InlineKeyboardButton(text="Подписаться (2)", url=CHANNEL_URL_2)
            ],
            # Кнопка для запуска бота отдельным рядом
            [
                InlineKeyboardButton(text="🤖 Запустить бота", url=OTHER_BOT_URL)
            ],
            # Кнопка проверки
            [
                InlineKeyboardButton(text="✅ Я всё выполнил!", callback_data="check_sub")
            ]
        ]
    )
    return keyboard

# Функция для проверки статуса подписки на канал
async def check_sub_status(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        return False

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    is_subscribed = await check_sub_status(message.from_user.id)
    
    if is_subscribed:
        await message.answer("Привет! Условия выполнены. Бот готов к работе! 🚀")
    else:
        await message.answer(
            "Привет! Для использования этого бота необходимо подписаться на каналы и запустить бота по кнопке ниже. 👇",
            reply_markup=get_subscription_keyboard()
        )

# Обработчик кнопки проверки
@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery):
    is_subscribed = await check_sub_status(callback.from_user.id)
    
    if is_subscribed:
        await callback.message.edit_text("Отлично! Доступ к боту открыт. 🔓")
    else:
        await callback.answer("Ты еще не подписался на канал!", show_alert=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

