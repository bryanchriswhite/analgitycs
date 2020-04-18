from concurrent.futures import Future, ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
from datetime import datetime
from dateutil.parser import isoparse
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import numpy as np
import os.path as path
import re

from lib import git, count
from lib.worktree import Worktree
from lib.decorator import timed

# e.g.: 9169d99 (wip, 2020-04-14T17:48:56+02:00)
date_group_re = r'(\d{4,}-\d{2,}-\d{2,}T\d{2,}:\d{2,}:\d{2,}.\d{2,}:\d{2,})'
commit_re = re.compile(r'^(\w+)\s+\(.*,\s+' + date_group_re + r'\)$')
default_max_worktrees = 20
default_max_workers = 15
default_commit_limit = 100
# default_timeout = 60


class RepoBlame:
    @timed
    def __init__(self, root: str, range_ref: str,
                 max_workers=default_max_workers,
                 max_worktrees=default_max_worktrees,
                 commit_limit=default_commit_limit,
                 file_filter=None):
        self.__root = root
        self.__max_workers = max_workers
        self.__max_worktrees = max_worktrees
        self.__commit_limit = commit_limit

        # TODO: shutdown executors
        worktree_executor = ThreadPoolExecutor(self.__max_worktrees)
        commit_fs = self.commits(worktree_executor, range_ref, limit=self.__commit_limit)
        commit_count_fs: List[Future] = []
        wait(commit_fs, return_when=ALL_COMPLETED)
        commits = [f.result() for f in commit_fs if f.result() is not None]
        for commit_hash, commit_date in commits:
            count_executor = ThreadPoolExecutor(self.__max_workers)
            wt = Worktree(self.__root, commit_hash, commit_hash)
            wt.add()
            future = worktree_executor.submit(count.commit,
                                              count_executor,
                                              wt.path(),
                                              commit_date,
                                              file_filter,
                                              done=wt.remove)
            commit_count_fs.append(future)
        self.__commit_count_fs = commit_count_fs

    @timed
    def stackplot(self):
        if self.__commit_count_fs == None or len(self.__commit_count_fs) == 0:
            raise RuntimeError("must call `blame` before `blame_stackplot`")

        commit_authors = []
        for commit_date, file_authors in [f.result() for f in (self.__commit_count_fs)]:
            new_results = {file: f.result() for (file, f) in file_authors.items() if f is not None}
            commit_authors.append((commit_date, new_results))

        commit_totals = self.__sum_commit_lines(commit_authors)
        plt.ylabel('Lines of code')

        commit_dates = [tup[0] for tup in commit_totals]
        author_ys: Dict[str, List[int]] = {}

        # Build `commit_dates` and `author_ys`
        for n, (commit_date, author_lines) in enumerate(commit_totals):
            for author, y in author_ys.items():
                if author not in author_lines.keys():
                    author_ys[author].append(0)
            for author, lines in author_lines.items():
                if author not in author_ys:
                    author_ys[author]: List[int] = [0 for _ in range(n)]
                author_ys[author].append(lines)

        labels = np.array(list(author_ys.keys()))
        ys = np.vstack(list(author_ys.values()))

        # def __date_filter(ds):
        #     for i, d in enumerate(ds):
        #         if i % 20 != 0:
        #             ds[i] = ''
        #         else:
        #             ds[i] = d.isoformat()
        #     return ds
        # x = np.array(__date_filter(commit_dates))
        x = [d.isoformat() for d in commit_dates]
        fig = plt.figure(figsize=(10, 20))
        fig.stackplot(x, *ys, labels=labels)
        plt.legend(loc='upper left')
        plt.title(path.basename(self.__root))
        plt.show()

    @timed
    def commits(self, executor: ThreadPoolExecutor, range_ref: str, limit: int = 0):
        log_lines = git.log(self.__root, range_ref)
        if limit > 0:
            log_lines = log_lines[:limit]

        def parse_line(line):
            if line == "":
                return

            match = commit_re.match(line)
            if match is None:
                return

            commit_hash, commit_date = [match[k] for k in (range(1, 3))]
            if commit_hash is None or commit_date is None:
                return

            return commit_hash, isoparse(commit_date)

        return [executor.submit(parse_line, l) for l in log_lines]

    @staticmethod
    @timed
    def __sum_commit_lines(commit_file_authors: List[Tuple[str, Dict[str, Dict[str, int]]]]):
        commit_dates: List[datetime] = []
        totals = []
        for commit_date, file_authors in commit_file_authors:
            commit_dates.append(commit_date)
            commit_author_totals: Dict[str, int] = {}
            for author_lines in file_authors.values():
                for author, counts in author_lines.items():
                    if author not in commit_author_totals:
                        commit_author_totals[author] = int(0)
                    commit_author_totals[author] += counts
            totals.append((commit_date, commit_author_totals))
        return totals
