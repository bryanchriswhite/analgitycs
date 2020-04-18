from math import ceil, floor
from typing import Dict, Sized, List
import matplotlib.pyplot as plt
import numpy as np

from lib.my_types import RepoAuthorTotals, TotalsDict


def repo_stackplots(totals_dict: TotalsDict):
    nrows = 2
    fig, ax = plt.subplots(nrows, ceil(4 / nrows), figsize=(10, 15))
    plt.ylabel('Lines of code')
    plt_index = 0

    for repo, commit_totals in totals_dict.items():
        i = floor(plt_index / 2)
        j = plt_index % 2

        commit_dates = [tup[0] for tup in commit_totals]
        author_ys: Dict[str, List[int]] = {}

        # Build `commit_dates` and `author_ys`
        for n, (commit_date, author_lines) in enumerate(commit_totals):
            for author, y in author_ys.items():
                if author not in author_lines.keys():
                    author_ys[author].append(0)
            for author, lines in author_lines.items():
                if author not in author_ys:
                    author_ys[author]: List[int] = [0 for _ in range(n)]
                author_ys[author].append(lines)

        labels = np.array(list(author_ys.keys()))
        ys = np.vstack(list(author_ys.values()))

        x = [d.isoformat() for d in commit_dates]
        ax[i, j].stackplot(x, *ys, labels=labels)
        ax[i, j].legend(loc='upper left')

        plt_index += 1
    plt.show()
