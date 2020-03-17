import asyncio
import queue
import random
import threading


class TaskManager:

    q: queue.Queue = queue.Queue()
    threads = []
    threadCount = 1

    @classmethod
    def init(cls):
        pass

    @classmethod
    def worker(cls):
        while True:
            item1 = cls.q.get(True, 1)
            if item1 is None:
                break
            item1[0](item1[1])
            cls.q.task_done()
            #cls.q.join()

    @classmethod
    def addTask(cls, func, args, threadCount=4):

        t = threading.Thread(target=func, args=args)
        t.start()
        #time.sleep(0.01)
        t.join()
        #for i in range(cls.threadCount):
        #    t = threading.Thread(target=cls.worker, args=cls.q)
        #    t.start()
        #    time.sleep(0.5)
        #    cls.threads.append(t)
#
        #cls.q.put((func, args))
        #cls.q.join()
#
        #for i in range(cls.threadCount):
        #    cls.q.put(None)
#
        #for t in cls.threads:
        #    t.join()

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
