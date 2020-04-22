import unittest

from lib import error


class TestErrors(unittest.TestCase):
    def test_response_error_str(self):
        msg = 'test response error'
        err = error.ResponseError(msg)
        self.assertEqual(str(err), msg)

    # def test_err_repo_missing(self):
    #     name = 'test-repo'
    #     expected_msg = f'no repo with {name}'
    #     err = error.ErrRepoMissing(name)
    #     print(str(err))
    #     self.assertEqual(expected_msg, str(err))
