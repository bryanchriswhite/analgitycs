from typing import Sized
from math import ceil, floor

import matplotlib.pyplot as plt
import numpy as np

from lib import my_types


def repo_stackplots(totals_dict: my_types.TotalsDict):
    totals_to_graph: my_types.Dict[str, my_types.RepoAuthorTotals] = totals_dict
    repo_names: Sized[str] = totals_dict.keys()

    nrows = 2
    fig, ax = plt.subplots(nrows, ceil(len(repo_names) / nrows), figsize=(10,15))
    plt.ylabel('Lines of code')
    plt_index = 0

    # TODO: add time
    x = np.arange(100)
    # x = np.array([])

    for repo, total_list in totals_to_graph.items():
        i = floor(plt_index / 2)
        j = plt_index % 2

        total_list = total_list[:10]
        total_list.reverse()

        ys = [n[2] for n in total_list]
        labels = [n[1] for n in total_list]

        ax[i,j].stackplot(x, *ys, labels=labels)
        ax[i,j].legend(loc='upper left')

        plt_index += 1
    plt.show()
