from concurrent.futures import Future, ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
from datetime import datetime
from dateutil.parser import isoparse
from typing import List, Tuple, Dict
import re, time

import matplotlib.pyplot as plt
import numpy as np

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


class RepoStat:
    def __init__(self, root: str,
                 max_workers=default_max_workers,
                 max_worktrees=default_max_worktrees):
        self.__root = root
        self.__max_workers = max_workers
        self.__max_worktrees = max_worktrees

    @timed
    def blame(self, range_ref: str, commit_limit=default_commit_limit, file_filter=None):
        # TODO: shutdown executors
        worktree_executor = ThreadPoolExecutor(self.__max_worktrees)
        commit_fs = self.commits(worktree_executor, range_ref, limit=commit_limit)
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
        return commit_count_fs

    # def blame_async(self, range_ref,
    #                 commit_limit=default_commit_limit,
    #                 file_filter=None):
    #
    #     start = self.__blame_start = time.perf_counter()
    #
    #     executor = ThreadPoolExecutor(0)
    #     return executor.submit(self.blame,
    #                            range_ref,
    #                            commit_limit,
    #                            file_filter=file_filter)

    # def blame_stackplot(self, commit_totals, figsize=(10, 10)):
    #     commit_dates = [tup[0] for tup in commit_totals]
    #     author_ys: Dict[str, List[int]] = {}
    #
    #     # Build `commit_dates` and `author_ys`
    #     for n, (commit_date, author_lines) in enumerate(commit_totals):
    #         for author, y in author_ys.items():
    #             if author not in author_lines.keys():
    #                 author_ys[author].append(0)
    #         for author, lines in author_lines.items():
    #             if author not in author_ys:
    #                 author_ys[author]: List[int] = [0 for _ in range(n)]
    #             author_ys[author].append(lines)
    #
    #     labels = np.array(list(author_ys.keys()))
    #     ys = np.vstack(list(author_ys.values()))
    #
    #     # def __date_filter(ds):
    #     #     for i, d in enumerate(ds):
    #     #         if i % 20 != 0:
    #     #             ds[i] = ''
    #     #         else:
    #     #             ds[i] = d.isoformat()
    #     #     return ds
    #     # x = np.array(__date_filter(commit_dates))
    #     x = [d.isoformat() for d in commit_dates]
    #     fig, ax = plt.subplots(figsize=figsize, dpi=80)
    #     ax.stackplot(x, *ys, labels=labels)
    #     ax.legend(loc='upper left')
    #     # ax.ylabel('Lines of code')
    #     # plt.title(path.basename(self.__root))
    #     plt.show()

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


