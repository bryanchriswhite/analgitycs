from datetime import date

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
    totals: Dict[str, Dict[str, Dict[str, int]]] = {}

    for repo, commit_author_line_counts in repo_counts.items():
        if repo not in totals:
            totals[repo] = {}
        for commit_date, files_author_line_counts in commit_author_line_counts.items():
            if commit_date not in totals[repo]:
                totals[repo][commit_date] = {}
            for author_line_counts in files_author_line_counts.values():
                for author, counts in author_line_counts.items():
                    if author not in totals[repo][commit_date]:
                        totals[repo][commit_date][author] = 0
                    totals[repo][commit_date][author] += counts

    # totals_dict: TotalsDict = {}
    # total_list: List[Tuple[int, str, float]]
    # for repo, totals in totals.items():
    #     for commit_date, total in totals:
    #
    #     # [(k, v, to_percent(v, total_lines[repo])) for cd,  in totals.items()]
    #
    #         total_list: List[Tuple[int, str, float]] = [(*tup, to_percent(tup[1], total_lines[repo])) for tup in totals.items()]
    #         total_list.sort(key=lambda x: x[1], reverse=True)
    #         total_list: RepoAuthorTotals = [[i + 1, *tup] for i, tup in enumerate(total_list)]
    #
    #         # TODO: MAY BE MORE THAN ONE COMMIT PER DAY!!!
    #         if commit_date not in totals_dict[repo]:
    #             totals_dict[repo][commit_date] = {}
    #         totals_dict[repo][commit_date] = total_list
    # return totals_dict, total_lines
    return totals
