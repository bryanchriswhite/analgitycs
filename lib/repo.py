from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from datetime import date
from typing import List, Tuple, Dict
import re

from lib import git, count
from lib.worktree import Worktree

commit_re = re.compile(r'^(\w+)\s+\(.*,\s+(\d{4,}-\d{2,}-\d{2,})\)$')
default_max_worktrees = 20
default_max_workers = 15
default_timeout = 60


class RepoStat:
    def __init__(self, root: str,
                 max_workers=default_max_workers,
                 max_worktrees=default_max_worktrees):
        self.__root = root
        self.__max_workers = max_workers
        self.__max_worktrees = max_worktrees

    # TODO: shutdown executors
    def line_authors_range(self, range_ref: str, file_filter=None, timeout=default_timeout):
        worktree_executor = ThreadPoolExecutor(self.__max_worktrees)
        commits = self.commits(worktree_executor, range_ref, timeout)
        commits = [f.result() for f in commits if f.result() is not None]

        #                                 my_types.RepoFileAuthors
        commit_count_fs: List[Future] = []
        # commit_count_fs: List[Tuple[date, Future]] = []
        # commit_count_fs: Dict[date, Future] = []
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

    def commits(self, executor: ThreadPoolExecutor, range_ref: str, timeout=default_timeout):
        log_lines = git.log(self.__root, range_ref)

        def parse_line(line):
            if line == "":
                return

            match = commit_re.match(line)
            if match is None:
                return

            commit_hash, commit_date = [match[k] for k in (range(1, 3))]
            if commit_hash is None or commit_date is None:
                return

            # return commit_hash, date.fromisoformat(commit_date)
            return commit_hash, commit_date

        return as_completed((executor.submit(parse_line, l) for l in log_lines), timeout)
