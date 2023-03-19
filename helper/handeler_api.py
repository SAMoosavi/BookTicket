from requests import request, Response, RequestException
from time import sleep


def api_handler(url, params=None, headers=None, json=None, method="get", error_msg="") -> Response:
    while True:
        try:
            response = request(method, url, params=params, headers=headers, json=json)
            return response
        except RequestException as e:
            print(f"Error in API handler: {e}")
            if error_msg:
                print(error_msg)
            sleep(20)
