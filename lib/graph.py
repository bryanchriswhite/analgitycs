from datetime import date
from math import ceil, floor
from typing import Dict, Sized, List
import matplotlib.pyplot as plt
import numpy as np

from lib.my_types import RepoAuthorTotals, TotalsDict


def repo_stackplots(totals_dict: TotalsDict):
    # repo_names: Sized[str] = totals_dict.keys()
    repo_names: List[str] = totals_dict.keys()

    nrows = 2
    # fig, ax = plt.subplots(nrows, ceil(len(repo_names) / nrows), figsize=(10, 15))
    fig, ax = plt.subplots(nrows, ceil(4 / nrows), figsize=(10, 15))
    plt.ylabel('Lines of code')
    plt_index = 0

    # TODO: add time
    # commit_dates = np.arange(100)
    # commit_dates = np.arange(2)
    # commit_dates = np.array([0, 1, 2, 3])

    for repo, commit_totals in totals_dict.items():
        i = floor(plt_index / 2)
        j = plt_index % 2

        # Sort all authors' history
        commits = [(date.fromisoformat(d), v) for d, v in totals_dict['uplink-c'].items()]
        commits.sort(key=lambda x: x[0])

        # commit_dates = [date.fromisoformat(d) for d in commit_totals.keys()]
        commit_dates: Sized[date] = []
        author_ys: Dict[str, List[int]] = {}

        # Build `commit_dates` and `author_ys`
        for commit_date, author_lines in commits:
            commit_dates.append(commit_date)
            for author, lines in author_lines.items():
                if author not in author_ys:
                    author_ys[author]: List[int] = [0 for _ in range(len(commit_dates) - 1)]
                author_ys[author].append(lines)

        print(commit_dates)
        print()
        print(author_ys)
        print()
        print([x for x in author_ys.values()])

        # ys = [t.values() for t in commit_totals.values()]
        # ys = [[for author, count in t.items()] for commit_date, t in commit_totals]

    #     ys = [[n[2]] for n in total_list]
    #     labels = [n[1] for n in total_list]
        labels = author_ys.keys()

        ax[i,j].stackplot(commit_dates, author_ys.values(), labels=labels)
        ax[i,j].legend(loc='upper left')

        plt_index += 1
    plt.show()

#         date_hashes: List[Tuple[date, str]] = [(d, h) for h, d in commits.items()]
#         date_hashes.sort(key=lambda n: n[0], reverse=True)

#         date_hashes_len = len(date_hashes)
#         if max_samples > date_hashes_len:
#             max_samples = date_hashes_len

#         interval = floor(len(date_hashes) / max_samples)

#         for i, date_hash in enumerate(date_hashes):
#             if i % interval == 0:
#                 samples.append(date_hash)

#         repo_samples[repo] = samples
