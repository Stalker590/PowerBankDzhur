from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F
import sys
import os
import app.keyboards as kb
from app.database import get_all_power_banks


# Додаємо шлях до config у попередній теці
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

router = Router()

async def format_power_bank_list():
    power_banks = get_all_power_banks()
    if not power_banks:
        return "Наразі товарів немає."
    lines = []
    for pb in power_banks:
        name, price, capacity, description, number = pb
        lines.append(f"/{number}. {name}, Вмістимість - {capacity} mAh, Ціна - {price}₴")
    return "\n\n".join(lines)
    

@router.message(CommandStart())
async def start(message: Message):
    greeting_text = (
        f"Привіт! Я Бот по продажі Павербанків по дешевій ціні по опту!\n\n"
        f"Щоб подивитись список товарів, натисни кнопку \"Купити\"!\n\n"
        f"Ось наші контакти:\n"
        f"{config.Number_Phone}\n\n"
        f"TG: {config.TG_Nick}\n\n"
        f"Email: {config.Email}"
    )
    await message.answer(
        text=greeting_text,
        reply_markup=kb.main
    )

@router.message(
    F.text.lower().in_([
        "купити", "купити!", "buy",
        "купити павербанк", "купити павербанк!", "buy павербанк",
        "купить", "купить", "✅подивитись товари"
    ])
)
async def handle_buy(message: Message):
    await message.answer("Ось список товарів:")
    power_bank_list_text = await format_power_bank_list()
    await message.answer(power_bank_list_text)
