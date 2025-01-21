# Домашнее задание по теме "Асинхронность на практике"

import asyncio
from asyncio import create_task


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1,6):
        await asyncio.sleep(1/power)
        print(f'Силач {name} поднял {i} шар')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    task1 = create_task(start_strongman('Vasya', 5))
    task2 = create_task(start_strongman('Pasha', 4))
    task3 = create_task(start_strongman('Denis', 3))
    await task1
    await task2
    await task3

asyncio.run(start_tournament())