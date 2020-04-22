from concurrent.futures import Future
import unittest

from lib.blame import Blame

class TestBlameManager(unittest.TestCase):
    def test_done(self):
        expected_result = "Hello, world!"

        f = Future()
        b = Blame(f)
        self.assertFalse(b.done())

        f.set_result(expected_result)
        self.assertTrue(b.done())

    def test_errors(self):
        bs = []
        for e in [RuntimeError('test error'), RuntimeWarning('test warning')]:
            f = Future()
            f.set_exception(e)
            bs.append(Blame(f))

        for b in bs:
            try:
                f.result()
            except RuntimeError as e:
                self.assertEqual(str(e), 'test error')
            except RuntimeWarning as e:
                self.assertEqual(str(e), 'test warning')

if __name__ == '__main__':
    unittest.main()