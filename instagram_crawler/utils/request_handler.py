import requests

from constants import urls


def request_url(url, headers=urls.HEADER, params=None, is_json=True):
    try:
        response = __call(headers, params, url)
        response.raise_for_status()
    except requests.HTTPError:
        raise requests.HTTPError('Received non 200 status code')
    except requests.RequestException:
        raise requests.RequestException
    else:
        if is_json:
            return response.json()
        else:
            return response


def __call(headers, params, url):
    if headers is None:
        response = requests.get(url)
        if response.status_code != 200:
            print("Received non 200 status code")
    else:
        if params is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, params=params)
    return response
