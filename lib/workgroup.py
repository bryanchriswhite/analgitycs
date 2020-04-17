from concurrent.futures import ThreadPoolExecutor
import os.path as path
from queue import SimpleQueue
import subprocess
from threading import Lock
from typing import List

from lib import util, count


class Workgroup:
    class Executor:
        def __init__(self, max_workers: int):
            self.__executor = ThreadPoolExecutor(max_workers)

        def map(self, func, args):
            # print(f'map called with func: {func} and sample {sample}')
            args = [[self.__executor, *arg] for arg in args]
            for arg in args:
                print(arg)
            return self.__executor.map(func, args)

        def shutdown(self, wait=True):
            self.__executor.shutdown(wait=wait)

    __base_cmd: List[str] = ['git', 'worktree']
    __lock: Lock = Lock()
    __running: bool = False
    __worktrees: List[str] = []


    def __init__(self, max_workers: int):
        self.__max_workers = max_workers
        self.__q = SimpleQueue()

    def __enter__(self):
        self.__executor = Workgroup.Executor(self.__max_workers)
        return self.__executor

    def __exit__(self, type, value, tb):
        self.__executor.shutdown()

        # self.__dequeue_ex.map(
        #     self.remove_worktree,
        #     (f'worktree{i}' for i in range(self.__max_workers)))

        # self.__enqueue_ex.shutdown(wait=True)
        # self.__dequeue_ex.shutdown(wait=True)

    def enqueue(self, *items):
        # TODO: timeout
        self.__enqueue_ex.map(self.__q.put, items)

    def __run(self):
        self.__enqueue_ex = ThreadPoolExecutor(self.__max_workers)
        self.__dequeue_ex = ThreadPoolExecutor(self.__max_workers)

        # def go_worktree():
        #     with

        # with self.__dequeue_ex as executor:
        #     # TODO: use timeout
        #     while not self.__q.empty():
        #         item = self.__q.get()
        #         executor.submit(go_worktree, [
        #             item[1]
        #         ])
