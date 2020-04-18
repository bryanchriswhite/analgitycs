from concurrent.futures import Future, ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
from dateutil.parser import isoparse
from typing import List, Tuple, Dict
import re

from lib import git, count
from lib.worktree import Worktree

# e.g.: 9169d99 (wip, 2020-04-14 17:48:56 +0200)
date_group_re = r'(\d{4,}-\d{2,}-\d{2,}T\d{2,}:\d{2,}:\d{2,}.\d{2,}:\d{2,})'
commit_re = re.compile(r'^(\w+)\s+\(.*,\s+' + date_group_re + r'\)$')
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
    def line_authors_range(self, range_ref: str, file_filter=None, limit=0):
        worktree_executor = ThreadPoolExecutor(self.__max_worktrees)
        commit_fs = self.commits(worktree_executor, range_ref, limit=limit)
        # commits = [f.result() for f in commits if f.result() is not None]

        #                                 my_types.RepoFileAuthors
        commit_count_fs: List[Future] = []
        # commit_count_fs: List[Tuple[date, Future]] = []
        # commit_count_fs: Dict[date, Future] = []
        # print(wait(commit_fs))
        wait(commit_fs, return_when=ALL_COMPLETED)
        commits = [f.result() for f in commit_fs]
        # print(f'commits {commits}')
        print(f'len(commits) {len(commits)}')
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

            # return commit_hash, datetime.fromisoformat(commit_date)
            return commit_hash, isoparse(commit_date)
        return [executor.submit(parse_line, l) for l in log_lines]
