from re import compile as re_compile

from lib.util import add_lines
from lib import git, my_types

header_re = re_compile("\w{,40} \d+ (\d+)(:? (\d+))?")
author_re = re_compile("author (.+)$")


def repo(executor, repo_root, filter_func=None):
    counts = {}
    files = git.ls_files(repo_root=repo_root)
    for f in files:
        if filter_func is not None and filter_func(f):
            continue
        counts[f]: my_types.FileAuthors = executor.submit(__count_file, f, repo_root)
    return counts


def __count_file(f, repo_root):
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
