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


def sum_repo_commit_lines(repo_results: Dict[str, List[Tuple[str, Dict[str, Dict[str, int]]]]]):
    totals: TotalsDict = {}
    commit_dates: List[datetime] = []
    for repo, commit_file_authors in repo_results.items():
        print(f'len(commit_file_authors {len(commit_file_authors)}')
        print(commit_file_authors[0])
        # Sort all authors' history
        # commit_author_line_counts.sort(key=lambda x: x[0])

        if repo not in totals:
            totals[repo] = []
        for commit_date, file_authors in commit_file_authors:
            commit_dates.append(commit_date)
            commit_author_totals: Dict[str, int] = {}
            for author_lines in file_authors.values():
                for author, counts in author_lines.items():
                    if author not in commit_author_totals:
                        commit_author_totals[author] = int(0)
                    commit_author_totals[author] += counts
            totals[repo].append((commit_date, commit_author_totals))
        print(f'len(totals[repo]): {len(totals[repo])}')

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
