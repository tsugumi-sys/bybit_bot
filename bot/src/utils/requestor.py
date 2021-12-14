import requests
from typing import Union, Dict


def get_request(url: str) -> Union[Dict, str]:
    try:
        res = requests.get(url).json
    except requests.exceptions.Timeout:
        res = f"Exception: requests.exceptions.Timeout raised in GET request for {url}"
    except requests.exceptions.TooManyRedirects:
        res = f"Exception:  requests.exceptions.TooManyRedirects raised in GET request for {url}"
    except requests.exceptions.RequestException:
        res = f"Exception: requests.exceptions.RequestException raised in GET request for {url}"

    return res
