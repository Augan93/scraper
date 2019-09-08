import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def request_retry(url):
    try:
        print('Try')
        response = requests_retry_session().get(url)
        if response.status_code == 200:
            return response

    except Exception as x:
        print('It failed. Try with proxies ', x.__class__.__name__)
        return None
