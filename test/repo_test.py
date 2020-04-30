from concurrent.futures import Future
import unittest

from lib import util
from lib.repo import RepoStat

test_ext_wlist = (".go", ".proto", ".c", ".h", ".sh", ".md", ".xml", ".wixproj", ".wsx", ".cs")
# test_file_filter = util.filter_ext(test_ext_wlist)


class TestRepoStat(unittest.TestCase):
    def test_blame(self):
        test_rs = RepoStat('storj', '/home/bwhite/Projects/analgitycs/storj')
        fs = test_rs.blame('master', commit_limit=10, ext_whitelist=test_ext_wlist)

        print(fs[0].result())


if __name__ == '__main__':
    unittest.main()
