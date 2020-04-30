from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor, wait, ALL_COMPLETED
from dateutil.parser import isoparse
from multiprocessing import cpu_count
import re
from typing import List

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

    def blame(self, range_ref: str, commit_limit: int = default_commit_limit, ext_whitelist=None):
        commit_limit = int(commit_limit)

        # TODO: shutdown executors
        commit_log_pool = ThreadPoolExecutor(self.max_workers)
        commit_fs = self.commits(commit_log_pool, range_ref, limit=commit_limit)
        commit_count_fs: List[Future] = []
        wait(commit_fs, return_when=ALL_COMPLETED)

        # TODO:
        process_exec = ProcessPoolExecutor(cpu_count())

        commits = [f.result() for f in commit_fs if f.result() is not None]
        for commit_hash, commit_date in commits:
            wt = Worktree(self.path, commit_hash, commit_hash)
            future = process_exec.submit(count.commit,
                                         self.max_workers,
                                         wt,
                                         commit_date,
                                         ext_whitelist)
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

        # TODO: try
        # return executor.map(log_lines, parse_line)
        return [executor.submit(parse_line, l) for l in log_lines]
