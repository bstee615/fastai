import logging

import azure.functions as func
from pathlib import Path
from ai import Predictor
import requests
import tempfile
import json


# https://docs.microsoft.com/en-us/azure/azure-functions/machine-learning-pytorch?tabs=bash#update-the-function-to-run-predictions
def main(req: func.HttpRequest) -> func.HttpResponse:
    model_path = Path('models/bears.pkl')
    predictor = Predictor(model_path)

    image_url = req.params.get('img')
    if not image_url:
        logging.error('No image URL in request.')
        return func.HttpResponse(status_code=400)
    logging.info(f'Image URL received: {image_url}. Downloading...')
    r = requests.get(image_url)
    logging.info(f'Status code {r.status_code}.')
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        content_file = tmpdir / 'content'
        logging.info(f'Saving to {content_file}.')
        with content_file.open('wb') as f:
            f.write(r.content)
        results = predictor.predict(content_file)
        logging.info(results)
    
    payload = {
        "prediction": results[0],
        "probabilities": results[2].tolist(),
    }

    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(payload), headers = headers)
