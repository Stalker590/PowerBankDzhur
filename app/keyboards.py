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