from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import app.keyboards as kb
import app.database as db
from aiogram import Router
from app.main_handlers import format_power_bank_list
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

admin_router = Router()

@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer(
        f"Привіт! Я Бот по по адміністрування нашого магазину!\n\n"
        f"Знизу є необхідні кнопки,щоб керувати ним\"!\n\n"
        f"Основний бот нашого магазину: {config.NAME_MAIN_BOT}"
        ,reply_markup = kb.admin_panel)

class AddProduct(StatesGroup):
    name = State()
    price = State()
    capacity = State()
    description = State()
    number = State()

@admin_router.message(F.text == "➕Додати товар")
async def add_product(message: Message, state: FSMContext):
    print("add_product called")
    await message.answer("Введіть назву товару:")
    await state.set_state(AddProduct.name)

@admin_router.message(AddProduct.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть ціну товару:")
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer("Введіть ємність товару (mAh):")
    await state.set_state(AddProduct.capacity)

@admin_router.message(AddProduct.capacity)
async def process_capacity(message: Message, state: FSMContext):
    await state.update_data(capacity=int(message.text))
    await message.answer("Введіть опис товару:")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введіть номер товару:")
    await state.set_state(AddProduct.number)

@admin_router.message(AddProduct.number)
async def process_number(message: Message, state: FSMContext):
    await state.update_data(number=int(message.text))
    data = await state.get_data()
    if db.add_power_bank(data['name'], data['price'], data['capacity'], data['description'], data['number']):
        await message.answer("Товар успішно додано!")
    else:
        await message.answer("Помилка: Товар з таким номером вже існує.")
    await state.clear()

@admin_router.message(F.text == "✅Подивитись товари")
async def show_products(message: Message):
    print("show_products called")
    await message.answer("Ось список товарів:")
    power_bank_list_text = await format_power_bank_list()
    await message.answer(power_bank_list_text)

class DeleteProduct(StatesGroup):
    waiting_for_number = State()

@admin_router.message(F.text == "🗑️Видалити товар")
async def ask_product_number(message: Message, state: FSMContext):
    await message.answer("Введіть номер товару, який ви хочете видалити:")
    await state.set_state(DeleteProduct.waiting_for_number)

@admin_router.message(DeleteProduct.waiting_for_number)
async def delete_product(message: Message, state: FSMContext):
    try:
        number = int(message.text)
        if db.delete_power_bank(number):
            await message.answer("Товар успішно видалено.")
        else:
            await message.answer("Не знайдено товар з таким номером.")
    except ValueError:
        await message.answer("Будь ласка, введіть правильне число.")
    await state.clear()




