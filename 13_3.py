import os
import logging
from aiogram import Bot, Dispatcher, types, Router
import asyncio

from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("API_TOKEN")
api = API_TOKEN
bot = Bot(token= api)

router = Router()
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)



@dp.message(Command("start"))
async def start_command(message: Message):
    welcome_message = "Привет! Я ваш бот, чем могу помочь?"
    await message.answer(welcome_message)

    logger.info(f'Ответ бота: {welcome_message}')

@dp.message(lambda message: message.text in ["Urban", "hello"])
async def urban_message(message: Message):
    print("Urban message")

@dp.message()
async def all_message(message):
    print('Мы получили сообщение!')

async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())

