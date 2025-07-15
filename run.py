from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
import asyncio
import config
import logging

bot = Bot(config.TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Привіт! Я Бот по продажі Павербанків по дешевій ціні по опту!')

@dp.message(
    F.text.in_([
        "Купити", "Купити!", "купити", "buy",
        "Купити Павербанк", "Купити Павербанк!", "купити Павербанк",
        "buy Павербанк", "купить", "Купить"
    ])
)
async def handle_buy(message: Message):
    await message.answer("Ось список товарів:")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')