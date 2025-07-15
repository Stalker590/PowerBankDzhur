from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
import asyncio

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Привіт! Я Бот по продажі Павербанків по дешевій ціні по опту!')

@router.message(
    F.text.in_([
        "Купити", "Купити!", "купити", "buy",
        "Купити Павербанк", "Купити Павербанк!", "купити Павербанк",
        "buy Павербанк", "купить", "Купить"
    ])
)
async def handle_buy(message: Message):
    await message.answer("Ось список товарів:")