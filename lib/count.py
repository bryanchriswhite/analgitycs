from concurrent.futures import ThreadPoolExecutor, wait
import re

from lib import git, my_types
from lib.decorator import timed
from lib.util import add_lines

header_re = re.compile(r'\w{,40} \d+ (\d+)(:? (\d+))?')
author_re = re.compile(r'author (.+)$')


# @timed
def commit(executor: ThreadPoolExecutor, repo_root, commit_date: str, filter_func=None, done=None):
    counts = {}
    files = git.ls_files(repo_root=repo_root)
    for f in files:
        if filter_func is not None and filter_func(f):
            continue
        counts[f]: my_types.FileAuthors = executor.submit(file, f, repo_root)

    def _done():
        wait([v for v in counts.values()])
        done()
    executor.submit(_done)
    # TODO: find a better way to get commit_date
    return commit_date, counts


# @timed
def file(f, repo_root):
    counts: my_types.FileAuthors = {}
    last_author_header_ln = 1
    last_header_ln = 1
    last_author_name = None

    for j, line in enumerate(git.blame(f, repo_root)):
        if line == "":
            continue
        header_match = header_re.match(line)
        if header_match is not None:
            header_new_ln = int(header_match.group(1))
            last_header_ln = int(header_new_ln)
            continue
        author_match = author_re.match(line)
        if author_match is not None:
            author = author_match.group(1)
            if last_author_name is None:
                last_author_name = author
                continue
            add_lines(counts, last_author_name, last_author_header_ln, last_header_ln)
            last_author_name = author
            last_author_header_ln = last_header_ln

    add_lines(counts, last_author_name, last_author_header_ln, last_header_ln + 1)
    return counts
