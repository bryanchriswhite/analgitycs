from lib.my_types import TotalsDict


def leaderboard(totals_dict: TotalsDict):
    for repo, total_list in totals_dict.items():
        print(repo)
        __print_totals(total_list[:10])
        print()


def __print_totals(t):
    for i, _, author, total, pct in t:
        print(str.format("#{}: {} ({}% | {})", i, author, pct, total))
