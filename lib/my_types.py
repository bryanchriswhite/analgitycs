from datetime import date
from typing import Dict, Tuple, List

FileAuthors = Dict[str, int]
CommitFileAuthors = Dict[str, FileAuthors]
RepoFileAuthors = Dict[str, CommitFileAuthors]
AllRepoFileAuthors = Dict[str, RepoFileAuthors]

                                    #  [ author[ pos name count  pct ] ]
RepoAuthorTotals = List[List[any]]  # List[List[dint, str, int, float]]
TotalList = List[Tuple[date, int, str, float]]
TotalsDict = Dict[str, TotalList]

# test_dict: AllRepoFileAuthors = {
#     'repo name': {
#         '/file/path': {
#             'author name': 12345  # line count
#         }
#     }
# }
