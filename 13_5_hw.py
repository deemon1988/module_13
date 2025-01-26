# Домашнее задание по теме "Машина состояний"

import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

API_TOKEN = ''
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    address, age, growth, weight = State(), State(), State(), State()


@dp.message_handler(text=['Calories'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weihgt(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    msg = (10 * data['weight']) + (6.25 * data['growth']) - ((5 * data['age']) + 5)
    await message.answer(f'Ваша норма каллорий: {msg}')
    await state.finish()


@dp.message_handler(text=['заказать'])
async def buy(message):
    await message.answer('Введите свой адрес доставки')
    await UserState.address.set()


@dp.message_handler(state=UserState.address)
async def fsm_handler(message, state):
    await state.update_data(first=message.text)
    data = await state.get_data()
    logging.info(f"адрес доставки: {data['first']}")
    await message.answer(f"Доставка будет отправлена на {data['first']}")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text=['hi'])
async def hello_message(message):
    await message.answer("Hello message")


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filemode='w', encoding='utf-8', filename='log_file.log',
                        format="%(asctime)s | %(levelname)s | %(message)s")
    executor.start_polling(dp, skip_updates=True)
