from unittest import TestCase, main

from lib import error
from lib.repo import RepoStat
from lib.blame import BlameManager


class TestBlameManager(TestCase):
    test_rs = RepoStat('test', '/no/where', 'https://nowhere.example')

    def test_add(self):
        bm = BlameManager()
        bm.add(self.test_rs)

        actual_rs = bm.repo_stats[self.test_rs.name]
        self.assertEqual(self.test_rs, actual_rs)

    def test_status(self):
        bm = BlameManager()
        bm.add(self.test_rs)

        self.assertRaises(error.ErrRepoNotBlamed, bm.status, self.test_rs.name)


if __name__ == '__main__':
    main()
