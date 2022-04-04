import asyncio
import random
import threading
import multiprocessing
import time


async def worker(id):
    for i in range(10):
        print(f"Worker_{id}: loop={i}")
        await asyncio.sleep(random.random())
        # time.sleep(random.random())


async def main():
    tasks = []
    for w in range(10):
        tasks.append(asyncio.create_task(worker(w)))
    await asyncio.wait(tasks)


asyncio.run(main())
