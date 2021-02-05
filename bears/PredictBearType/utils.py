import logging
import requests
import validators


def download_file(fd, url):
    """
    Download a file to local storage.
    """
    assert validators.url(url)
    r = requests.get(url)
    logging.info(f'Status code {r.status_code}.')
    fd.write(r.content)
