# Домашнее задание по теме "Инлайн клавиатуры".

import aiogram
import asyncio
from aiogram import Bot, Dispatcher, executor, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

BOT_TOKEN = ''
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='')
kb.add(button, button2)

inline_kb = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(button4, button3)


class UserState(StatesGroup):
    age, growth, weight = State(), State(), State()


@dp.message_handler(commands=['start'])
async def starter(message):
    user = message.from_user.username
    await message.answer(f'Hello, {user} !', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def choise(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Сколько Вам лет ?')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer("Ваш рост ?")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer("Ваш вес ?")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def msg(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    msg = (10 * data['weight']) + (6.25 * data['growth']) - ((5 * data['age']) + 5)
    await message.answer(f"Ваша норма калорий: {msg}")
    await state.finish()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f"для рассчета используется формула Миффлина-Сан Жеора: \n "
                              f"(10 * вес) + (6.25 * рост) - ((5 * возраст) + 5)")
    await call.answer()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Send /start for beggining')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
