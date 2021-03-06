import logging

import azure.functions as func
from pathlib import Path
from ai import Predictor
import tempfile
import json
from PredictBearType.utils import download_file


# https://docs.microsoft.com/en-us/azure/azure-functions/machine-learning-pytorch?tabs=bash#update-the-function-to-run-predictions
def main(req: func.HttpRequest) -> func.HttpResponse:
    model_path = Path('models/bears.pkl')
    predictor = Predictor(model_path)

    image_url = req.params.get('url')
    if not image_url:
        errMsg = 'No image URL in request.'
        logging.error(errMsg)
        return func.HttpResponse(json.dumps({"error": errMsg}), status_code=400)
    logging.info(f'Image URL received: {image_url}.')
    
    with tempfile.TemporaryDirectory() as content_dir_path:
        content_dir = Path(content_dir_path)
        content_file = content_dir / 'content'
        logging.info(f'Downloading to {content_file}.')
        try:
            download_file(content_file, image_url)
        except AssertionError:
            logging.error(f'Invalid image URL: {image_url}')
            return func.HttpResponse(json.dumps({"error": 'Invalid image URL'}), status_code=400)
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
