from datetime import date
from math import ceil, floor
from typing import Dict, Sized, List
import matplotlib.pyplot as plt
import numpy as np

from lib.my_types import RepoAuthorTotals, TotalsDict


def repo_stackplots(totals_dict: TotalsDict):
    # repo_names: Sized[str] = totals_dict.keys()
    repo_names: List[str] = list(totals_dict.keys())

    nrows = 2
    # fig, ax = plt.subplots(nrows, ceil(len(repo_names) / nrows), figsize=(10, 15))
    fig, ax = plt.subplots(nrows, ceil(4 / nrows), figsize=(10, 15))
    plt.ylabel('Lines of code')
    plt_index = 0

    for repo, commit_totals in totals_dict.items():
        i = floor(plt_index / 2)
        j = plt_index % 2

        # Sort all authors' history
        # commit_totals.sort(key=lambda x: x[0])

        # commit_dates = [date.fromisoformat(d) for d in commit_totals.keys()]
        commit_dates = [tup[0] for tup in commit_totals]
        # commit_dates: Sized[date] = list()
        author_ys: Dict[str, List[int]] = {}

        # Build `commit_dates` and `author_ys`
        for n, (commit_date, author_lines) in enumerate(commit_totals):
            # commit_dates.append(date.fromisoformat(commit_date))
            # commit_dates.append(commit_date)
            for author, y in author_ys.items():
                if author not in author_lines.keys():
                    author_ys[author].append(0)
            for author, lines in author_lines.items():
                if author not in author_ys:
                    author_ys[author]: List[int] = [0 for _ in range(n)]
                author_ys[author].append(lines)

        # print(commit_dates)
        # print()
        # print(author_ys)
        # print()
        # print([x for x in author_ys.values()])

        # ys = [t.values() for t in commit_totals.values()]
        # ys = [[for author, count in t.items()] for commit_date, t in commit_totals]

        #     ys = [[n[2]] for n in total_list]
        #     labels = [n[1] for n in total_list]
        labels = np.array(list(author_ys.keys()))
        ys = np.array([np.array(x) for x in author_ys.values()])
        # np.vstack(author_ys.values())

        print(f'len commit dates & ys: {[len(y) for y in (commit_dates, *ys)]}')
        for v in author_ys.values():
            print(v)
            print()
        # print([type(y) for y in ys])
        # print(type(ys[0][0]))
        # print(type(ys))
        # print(ys)

        # x = [0, 1, 2, 3]
        x = [d.isoformat() for d in commit_dates]
        y1 = [1, 1, 1, 1]
        y2 = [2, 2, 2, 2]
        y3 = [3, 3, 3, 3]
        y4 = [4, 4, 4, 4]
        # ys = [y1, y2, y3, y4]
        ax[i, j].stackplot(x, *ys, labels=labels)
        ax[i, j].legend(loc='upper left')

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
