import unittest
from ai import Predictor
from pathlib import Path

class TestPredictor(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_path = Path('models/bears.pkl')
        self.inf = Predictor(model_path)
        self.images = Path('images')

    def test_predict(self):
        sunbear = self.images / 'black.jpg'
        p = self.inf.predict(sunbear)
        assert p[0] == 'black'

if __name__ == '__main__':
    unittest.main()
