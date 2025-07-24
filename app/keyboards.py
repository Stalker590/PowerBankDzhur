from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅Подивитись товари'),
            KeyboardButton(text='🛠️Допомога')
        ]
    ],
    resize_keyboard=True
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅Подивитись товари'),
            KeyboardButton(text='🛠️Допомога')
        ],
        [
            KeyboardButton(text='➕Додати товар'),
            KeyboardButton(text='🗑️Видалити товар')
        ],
    ],
    resize_keyboard=True
)