import aiogram
from aiogram import Bot, Dispatcher
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = ''
bot = Bot(API_TOKEN)

dp =Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb.row(button1, button2)


class UserState(StatesGroup):
    age, growth = State(), State()


@dp.message_handler(text='Информация')
async def information(message):
    await message.answer('Информация о боте')

@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Сколько вам полных лет ?')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def growth_message(message, state):
    try:
        user_age = int(message.text)
        if not 0 <= user_age < 100:
            await message.reply("Возраст должен быть в диапазоне от 0 до 100")
            return
        await state.update_data(age=user_age)
        await message.answer('Введите ваш рост')
        await UserState.growth.set()
    except ValueError:
        await message.reply("Пожалуйста, введите целое число.")

@dp.message_handler(state=UserState.growth)
async def finish_message(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer(f"Ваши данные:\n возраст: {data['age']}, рост: {data['growth']}")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler()
async def all_message(message):
    await message.answer(f'Чтобы продолжить введите /start')

if __name__ == '__main__':
    executor.start_polling(dp)