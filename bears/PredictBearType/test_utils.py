import unittest
import tempfile
from PredictBearType.utils import download_file
from pathlib import Path

class TestUtils(unittest.TestCase):
    def test_download_works(self):
        with tempfile.TemporaryDirectory() as tempdir_path:
            tempdir = Path(tempdir_path)
            download_file(tempdir/'content', 'https://www.expresstorussia.com/files/pages/015159.jpg')

    def test_not_url(self):
        with tempfile.TemporaryDirectory() as tempdir_path:
            self.assertRaises(AssertionError, lambda: download_file(Path(tempdir_path)/'content', 'hello!'))

if __name__ == '__main__':
    unittest.main()
