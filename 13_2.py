import asyncio
import time

# 1 usage
async def get_temp():
    print("Первое показание")
    await asyncio.sleep(2)
    print("25 C")

# 1 usage
async def get_pres():

    await asyncio.sleep(4)
    print("Второе показание")
    print("101 kPa")

# 1 usage
async def main():
    print("Старт")
    task1 = asyncio.create_task(get_temp())
    task2 = asyncio.create_task(get_pres())
    await task1
    await task2
    print("Финиш")

start = time.time()
asyncio.run(main())
finish = time.time()

print(f"Working time = {round(finish-start, 2)} seconds")