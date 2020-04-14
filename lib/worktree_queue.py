from typing import List
from queue import SimpleQueue
import subprocess


class WorktreeQueue:
    __base_cmd: List[str] = ['git', 'worktree']

    def __init__(self, repo_root: str, max_worktrees: int):
        self.__repo_root = repo_root
        self.__max = max_worktrees

    def __enter__(self):
        # init queue
        self.__q = SimpleQueue()

        # set up n workers with loop
        # workers pull from queue

        # for i in range(0, self.__max):
        # self.add_worktree(f'worktree{i}', 'master')
        # self.move_worktree(f'worktree{i}', '')
        return self

    def __exit__(self, type, value, tb):
        for i in range(0, self.__max):
            self.remove_worktree(f'worktree{i}')

    def __git(self, cmd: str, *args: str):
        p = subprocess.run(self.__base_cmd +
                           [cmd, *args],
                           capture_output=True,
                           cwd=self.__repo_root)
        if p.returncode != 0:
            raise IOError(p.stderr)
        return p

    def add_worktree(self, path: str, hash: str):
        self.__git('add', path, hash)

    def remove_worktree(self, path: str):
        self.__git('remove', path)

    def get_root(self):
        return self.__repo_root
