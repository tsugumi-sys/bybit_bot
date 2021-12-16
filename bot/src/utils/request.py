import requests
from typing import Any, Union, Dict
from pybit.exceptions import FailedRequestError, InvalidRequestError


def request_predict_endpoint(url: str) -> Union[Dict, str]:
    # [TODO]
    # Is this code is proper in terms of typing?
    try:
        res: Any = requests.get(url).json
    except requests.exceptions.Timeout:
        res = f"Exception: requests.exceptions.Timeout raised in GET request for {url}"
    except requests.exceptions.TooManyRedirects:
        res = f"Exception:  requests.exceptions.TooManyRedirects raised in GET request for {url}"
    except requests.exceptions.RequestException:
        res = f"Exception: requests.exceptions.RequestException raised in GET request for {url}"

    return res


def request_bybit_api(request: Any) -> Union[Dict, str]:
    try:
        res: Dict = request()
        return res
    except InvalidRequestError as e:
        return e.message
    except FailedRequestError as e:
        return e.message
