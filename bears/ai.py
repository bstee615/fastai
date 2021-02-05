from fastai.learner import *
from pathlib import Path
import pathlib
import os


# Cannot instantiate PosixPath on Windows platform
if os.name == 'nt':
    pathlib.PosixPath = pathlib.WindowsPath


class Predictor:
    """
    Wrap a learner to give user-formatted predictions.
    """
    def __init__(self, model):
        self.inf = load_learner(model)
    
    def predict(self, filepath):
        return self.inf.predict(filepath)


if __name__ == '__main__':
    trained_model = Path('models/bears.pkl')
    p = Predictor(trained_model)
    for img in Path().glob('images/*.jpg'):
        prediction, pred_idx, probs = p.predict(img)
        print(f'{img}: p(image={p.inf.dls.vocab}) = {[f"{p:.2%}" for p in probs]}, {prediction=}')
