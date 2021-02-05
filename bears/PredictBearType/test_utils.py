import unittest
import tempfile
from PredictBearType.utils import download_file


class TestUtils(unittest.TestCase):
    def test_download_works(self):
        with tempfile.NamedTemporaryFile() as fd:
            download_file(fd, 'https://www.expresstorussia.com/files/pages/015159.jpg')

    def test_not_url(self):
        with tempfile.NamedTemporaryFile() as fd:
            self.assertRaises(AssertionError, lambda: download_file(fd, 'hello!'))

if __name__ == '__main__':
    unittest.main()
