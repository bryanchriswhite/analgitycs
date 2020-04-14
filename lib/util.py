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


def repo_counts_to_totals_dict(repo_counts: AllRepoFileAuthors):
    totals: Dict[str, Dict[str, int]] = {}
    total_lines: Dict[str, int] = {}

    for repo, files_author_line_counts in repo_counts.items():
        repo_totals: Dict[str, int] = {}
        total_lines[repo] = 0

        for author_line_counts in files_author_line_counts.values():
            for author, counts in author_line_counts.items():
                total_lines[repo] += counts

                if author not in repo_totals:
                    repo_totals[author] = 0
                repo_totals[author] += counts
        totals[repo] = repo_totals

    totals_dict: TotalsDict = {}
    for repo, totals in totals.items():
        total_list: List[Tuple[int, str, float]] = [(*tup, to_percent(tup[1], total_lines[repo])) for tup in totals.items()]
        total_list.sort(key=lambda x: x[1], reverse=True)
        total_list: RepoAuthorTotals = [[i + 1, *tup] for i, tup in enumerate(total_list)]

        totals_dict[repo] = total_list
    return totals_dict, total_lines
