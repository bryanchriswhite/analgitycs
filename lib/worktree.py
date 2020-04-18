from typing import List
import os.path as path
import subprocess


class Worktree:
    __base_cmd: List[str] = ['git', 'worktree']

    def __init__(self, root: str, path: str, hash: str):
        self.__root,\
        self.__path,\
        self.__hash = root, path, hash

    def __enter__(self):
        self.add()
        return self

    def __exit__(self, type, value, tb):
        self.remove()

    def add(self):
        self.__git('add',
                   self.__path,
                   self.__hash)

    def remove(self):
        self.__git('remove', self.__path)

    def path(self):
        return path.join(self.__root, self.__path)

    def __git(self, cmd: str, *args: str):
        p = subprocess.run(self.__base_cmd +
                           [cmd, *args],
                           capture_output=True,
                           cwd=self.__root)
        if p.returncode != 0:
            raise IOError(p.stderr)
        return p
