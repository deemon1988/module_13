import aiogram
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup



BOT_TOKEN = ''
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Информация', callback_data='info')
kb.add(button)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='info')],
        [KeyboardButton(text='shop'),
         KeyboardButton(text='donate')
         ]
    ], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def starter(message):
    await message.answer('Hello, i am bot helping your', reply_markup=kb)

@dp.message_handler(text='info')
async def button_info(message):
    await message.answer('Информация о боте')

@dp.callback_query_handler(text='info')
async def infor(call):
    await call.message.answer("Information about a bot")
    await call.answer()

@dp.message_handler()
async def all_message(message):
    await message.answer("send /start for beginning", reply_markup=start_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
