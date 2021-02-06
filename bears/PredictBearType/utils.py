import logging
import requests
import validators


def download_file(file, url):
    """
    Download a file to local storage.
    """
    assert validators.url(url)
    r = requests.get(url)
    logging.info(f'Status code {r.status_code}.')
    with file.open('wb') as f:
        f.write(r.content)
