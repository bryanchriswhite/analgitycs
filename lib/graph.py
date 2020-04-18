from math import ceil, floor
from typing import Dict, Sized, List
import matplotlib.pyplot as plt
import numpy as np

from lib.my_types import RepoAuthorTotals, TotalsDict


def repo_stackplots(totals_dict: TotalsDict):
    # nrows = len(totals_dict.keys())
    nrows = 4
    fig, ax = plt.subplots(nrows, 1, figsize=(10, 20))
    plt.ylabel('Lines of code')
    plt_index = 0

    for repo, commit_totals in totals_dict.items():
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
        ax[plt_index].stackplot(x, *ys, labels=labels)
        ax[plt_index].legend(loc='upper left')

        plt_index += 1
    plt.show()
