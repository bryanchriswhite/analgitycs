from typing import Dict, Tuple, List

FileAuthors = Dict[str, int]
CommitFileAuthors = Dict[str, FileAuthors]
RepoFileAuthors = Dict[str, CommitFileAuthors]
AllRepoFileAuthors = Dict[str, RepoFileAuthors]

                                    #  [ author[ pos name count  pct ] ]
RepoAuthorTotals = List[List[any]]  # List[List[dint, str, int, float]]
            # isodate --v
TotalList = List[Tuple[str, int, str, float]]
                  # isodate --v
TotalsDict = Dict[str, Tuple[str, TotalList]]

# test_dict: AllRepoFileAuthors = {
#     'repo name': {
#         '/file/path': {
#             'author name': 12345  # line count
#         }
#     }
# }
