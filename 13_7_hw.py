# Домашнее задание по теме "Клавиатура кнопок".

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio

API_TOKEN = ''
bot = Bot(token=API_TOKEN)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb.row(button, button2)

dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age, growth, weight = State(), State(), State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    user = message.from_user
    await message.answer(f"Привет, {user.first_name} я Бот помогающий твоему здоровью!", reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Информация о боте!')


@dp.message_handler(text='Рассчитать')
async def set_age(message, state):
    await message.answer('Сколько вам лет?')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите ваш рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите ваш вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def get_msg(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма каллорий {data['age']},{data['growth']},{data['weight']}", reply_markup=kb)
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer(f"Чтобы начать введите /start")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
