from concurrent.futures import ThreadPoolExecutor, Future, wait, ALL_COMPLETED
from datetime import datetime
from flask_socketio import emit
from typing import List, Dict
import time

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

    # @timed
    def __on_done(self, f):
        error = f.exception()
        if error is not None:
            self.error = error
            raise RuntimeError(error)

        print(f.result()[0].result())
        done, _ = wait(f.result(),
             return_when=ALL_COMPLETED)

        self.data = [f.result() for f in f.result() if f in done]
        self.__end = time.perf_counter()
        emit('blame_done', self.status())

    def done(self):
        return self.__f.done()

    def status(self):
        done = self.done()
        error = str(self.error)
        authors, layers, totals = [], [], []

        if done:
            totals = self.totals()
            authors, layers = self.author_layers()

        return {
            'status': {
                'start': self.__start,
                'end': self.__end,
                'done': done,
                'error': error,
            },
            'authors': authors,
            'layers': layers,
            'totals': totals
        }

    @timed
    def author_layers(self):
        if not self.done() or self.data is None:
            return [], []

        author_ys: Dict[str, List[int]] = {}

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
        return authors, layers

    # TODO: refactor/cleanup
    @timed
    def totals(self):
        if not self.__f.done() or self.data is None:
            return []

        commit_authors = []
        for commit_date, file_authors in self.data:
            new_results = {k: v for k, v in file_authors.items() if v is not None}
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


class BlameManager:
    def __init__(self):
        self.repo_stats = {}
        self.blames = {}

    def add(self, rs: RepoStat):
        if rs.name in self.repo_stats:
            return error.ErrRepoExists(rs.name)

        self.repo_stats[rs.name] = rs
        return rs

    def delete(self, name):
        self.blames.pop(name, None)

    def blame(self, name, range_ref: str, commit_limit: int = 0, ext_whitelist=None):
        if name not in self.repo_stats:
            raise error.ErrRepoMissing(name)

        if name in self.blames:
            return self.blames[name]

        rs = self.repo_stats[name]
        executor = ThreadPoolExecutor(1)
        f = executor.submit(rs.blame,
                            range_ref,
                            commit_limit,
                            ext_whitelist=ext_whitelist)

        # f.add_done_callback(lambda _: executor.shutdown())
        _blame = Blame(f)
        self.blames[name] = _blame
        return _blame
