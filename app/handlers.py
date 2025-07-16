from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
import asyncio
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

import app.keyboards as kb
from app.PowerBank import power_banks

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer_photo(photo = 'https://ibb.co/yBMvf80D',
    caption=f"""
    Привіт! Я Бот по продажі Павербанків по дешевій ціні по опту! 

    Щоб подивитись список товарів, натисни кнопку "Купити"! 

    Ось наші контакти:
    {config.Number_Phone}

    TG: {config.TG_Nick}

    Email: {config.Email}
    """
    ,reply_markup=kb.main)
@router.message(
    F.text.in_([
        "Купити", "Купити!", "купити", "buy",
        "Купити Павербанк", "Купити Павербанк!", "купити Павербанк",
        "buy Павербанк", "купить", "Купить","✅Подивитись товари"
    ])
)
async def handle_buy(message: Message):
    power_bank_list_text = ""
    await message.answer("Ось список товарів:")
    for power_bank in power_banks:
        power_bank_list_text += str(f"/{power_bank.number}. {power_bank.name}, Вмістимість - {power_bank.capacity} mAh, Ціна - {power_bank.price}₴") + "\n\n"
    await message.answer(str(power_bank_list_text))