import asyncio
import random
import threading
from multiprocessing.pool import ThreadPool


class ParallelTask:

    @classmethod
    def init(cls):
        pass

    @classmethod
    def addTask(cls, func, args):
        t = threading.Thread(target=func, args=args)
        # t.setDaemon(True)
        t.start()
        t.join()
        #pool = ThreadPool(processes=1)
        #result = pool.apply_async(func, args)
        #return result.get()

    @classmethod
    async def addTaskAsync(cls, func):
        await cls.randSleep()
        await asyncio.create_task(func)
        await cls.randSleep()
        # task.cancel()

    @classmethod
    async def randSleep(cls, a=1, b=3):
        i = random.randint(a, b)
        await asyncio.sleep(i)


