import asyncio
import multiprocessing as mp
import random
import threading


class ParallelTask:

    tasks = None
    threads = None
    manager = None
    pool = None

    @classmethod
    def init(cls):
        cls.threads = []
        cls.cachedFuncs = []
        cls.pool = mp.Pool(mp.cpu_count())
        cls.manager = mp.Manager()
        cls.tasks = cls.manager.Queue()
        cls.results = cls.manager.Queue()

    @classmethod
    def update(cls):
        pass
        #for t in cls.threads:
            #t.join()

    @classmethod
    def addTask(cls, func, arguments):
        # todo: avoid threading..
        t = threading.Thread(target=func, args=arguments)
        t.setDaemon(True) # allows to exit program no matter running threads
        t.start()

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


