import multiprocessing
import multiprocessing as mp
import threading
from multiprocessing.context import Process
from multiprocessing.pool import Pool


class ParallelTask:

    manager = None
    pool = None

    @classmethod
    def init(cls):
        cls.pool = mp.Pool(mp.cpu_count())
        cls.manager = mp.Manager()
        cls.tasks = cls.manager.Queue()
        cls.results = cls.manager.Queue()

    @classmethod
    def addTask(cls, func, arguments: tuple):
        # todo: avoid threading..
        t = threading.Thread(target=func, args=arguments)
        t.start()
        t.join()

    @classmethod
    def update(cls):
        pass
