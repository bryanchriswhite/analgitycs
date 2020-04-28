from concurrent.futures import Future, ThreadPoolExecutor, wait, ALL_COMPLETED
from dateutil.parser import isoparse
from typing import List
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


class RepoStat:
    def __init__(self, name: str, path: str,
                 url: str = '',
                 max_workers=default_max_workers,
                 max_worktrees=default_max_worktrees):
        self.name = name
        self.path = path
        self.url = url
        self.max_workers = max_workers
        self.max_worktrees = max_worktrees

    @timed
    def blame(self, range_ref: str, commit_limit: int = default_commit_limit, file_filter=None):
        commit_limit = int(commit_limit)

        # TODO: shutdown executors
        worktree_executor = ThreadPoolExecutor(self.max_worktrees)
        commit_fs = self.commits(worktree_executor, range_ref, limit=commit_limit)
        commit_count_fs: List[Future] = []
        wait(commit_fs, return_when=ALL_COMPLETED)
        commits = [f.result() for f in commit_fs if f.result() is not None]
        for commit_hash, commit_date in commits:
            count_executor = ThreadPoolExecutor(self.max_workers)
            wt = Worktree(self.path, commit_hash, commit_hash)
            wt.add()
            future = worktree_executor.submit(count.commit,
                                              count_executor,
                                              wt.path(),
                                              commit_date,
                                              file_filter,
                                              done=wt.remove)
            commit_count_fs.append(future)
        return commit_count_fs

    @timed
    def commits(self, executor: ThreadPoolExecutor, range_ref: str, limit: int = 0):
        log_lines = git.log(self.path, range_ref)
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
