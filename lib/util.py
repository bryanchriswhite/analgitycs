from datetime import datetime

from typing import Dict, List, Tuple
import os.path as path

from lib.my_types import AllRepoFileAuthors, FileAuthors, RepoAuthorTotals, TotalsDict


def add_lines(counts: FileAuthors, author, start, end):
    if author not in counts:
        counts[author] = 0
    diff = end - start
    counts[author] += diff


def to_percent(n, total):
    return round((n / total) * 100, 2)


def filter_ext(ext_whitelist, excluded_exts=None):
    def _filter(filename):
        ext = path.splitext(filename)[1]
        exclude = filename == "" or ext not in ext_whitelist
        if exclude and excluded_exts is not None:
            excluded_exts.add(ext)
        return exclude
    return _filter


def format_filename(input):
    return "".join([x if x.isalnum() else "_" for x in input])


def pluck(dict, *args):
    return [dict[arg] for arg in args]