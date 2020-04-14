from typing import Dict, Tuple, List

FileAuthors = Dict[str, int]
RepoFileAuthors = Dict[str, FileAuthors]
AllRepoFileAuthors = Dict[str, RepoFileAuthors]

                                    #  [ author[ pos name count  pct ] ]
RepoAuthorTotals = List[List[any]]  # List[List[int, str, int, float]]
TotalList = List[Tuple[int, str, float]]
TotalsDict = Dict[str, TotalList]

# test_dict: AllRepoFileAuthors = {
#     'repo name': {
#         '/file/path': {
#             'author name': 12345  # line count
#         }
#     }
# }
