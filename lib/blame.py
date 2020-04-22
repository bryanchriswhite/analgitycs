from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime
from typing import List, Dict
import time

import numpy as np

from lib import error
from lib.repo import RepoStat
from lib.decorator import timed

class Blame:
    def __init__(self, f: Future):
        self.__start = time.perf_counter()
        self.__f = f
        self.data = None
        self.error = None
        self.__end = None

        f.add_done_callback(self.__on_done)

    def __on_done(self, f):
        self.__end = time.perf_counter()
        error = f.exception()
        if error is not None:
            self.error = error
            return
        # self.data = self.__unwrap_results(f)
        print(f.result())
        self.data = f.result()

    # def __unwrap_results(self, f: Future):
    #     return [{author:total} for ]

    def done(self):
        return self.__f.done()

    def status(self):
        done = self.done()
        error = str(self.error)
        end = self.__end or time.perf_counter()
        authors, layers, totals = [], [], []

        if done:
            totals = self.totals()
            authors, layers = self.author_layers()

        duration = round(end - self.__start, 2)

        return {
            'status': {
                'running': f'{round(duration, 2)}s',
                'done': done,
                'error': error,
            },
            'authors': authors,
            'layers': layers,
            'totals': totals
        }

    def author_layers(self):
        if not self.__f.done() or self.data is None:
            return []

        # commit_dates = [tup[0] for tup in self.data]
        author_ys: Dict[str, List[int]] = {}

        # Build `commit_dates` and `author_ys`
        for n, (commit_date, author_lines) in enumerate(self.totals()):
            for author, y in author_ys.items():
                if author not in author_lines.keys():
                    author_ys[author].append(0)
            for author, lines in author_lines.items():
                if author not in author_ys:
                    author_ys[author]: List[int] = [0 for _ in range(n)]
                author_ys[author].append(lines)

        authors = list(author_ys.keys())
        layers = list(author_ys.values())
        # print()
        # print()
        # print()
        # print(authors)
        # print()
        # print()
        # print()
        # print(layers)
        # print()
        # print()
        # print()
        return authors, layers


    # TODO: refactor/cleanup
    @timed
    def totals(self):
        if not self.__f.done() or self.data is None:
            return []

        commit_authors = []
        for commit_date, file_authors in [f.result() for f in self.data]:
            new_results = {file: f.result() for (file, f) in file_authors.items() if f is not None}
            commit_authors.append((commit_date, new_results))

        commit_dates: List[datetime] = []
        totals = []
        for commit_date, file_authors in commit_authors:
            commit_dates.append(commit_date)
            commit_author_totals: Dict[str, int] = {}
            for author_lines in file_authors.values():
                for author, counts in author_lines.items():
                    if author not in commit_author_totals:
                        commit_author_totals[author] = int(0)
                    commit_author_totals[author] += counts
            totals.append((commit_date, commit_author_totals))
        return totals


class BlameManager():
    def __init__(self):
        self.__repo_stats = {}
        self.__blames = {}

    def add(self, name, root,
            max_workers=None,
            max_worktrees=None,
            file_filter=None):
        # print(f'root {root}')
        # print(f'max_workers {max_workers}')
        # print(f'max_worktrees {max_worktrees}')

        if name in self.__repo_stats:
            return error.ErrRepoExists(name)
            # return RuntimeError(f)

        rs = RepoStat(root,
                      max_workers=max_workers,
                      max_worktrees=max_worktrees)
        self.__repo_stats[name] = rs
        return rs

    def delete(self, name):
        self.__blames.pop(name, None)

    def blame(self, name, range_ref: str, commit_limit: int = 0, file_filter=None):
        if name not in self.__repo_stats:
            raise error.ErrRepoMissing(name)

        if name in self.__blames:
            return self.__blames[name]

        rs = self.__repo_stats[name]
        executor = ThreadPoolExecutor(1)
        f = executor.submit(rs.blame,
                            range_ref,
                            commit_limit,
                            file_filter=file_filter)

        _blame = Blame(f)
        self.__blames[name] = _blame
        return _blame

    def status(self, name: str):
        if name not in self.__repo_stats:
            raise error.ErrRepoMissing(name)
        if name not in self.__blames:
            raise error.ErrRepoNotBlamed(name)
        return self.__blames[name].status()
