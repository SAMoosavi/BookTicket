from requests import request, Response, RequestException
from time import sleep


def api_handler(url, params=None, headers=None, json=None, method="get", error_msg="") -> Response:
    while True:
        try:
            response = request(method, url, params=params, headers=headers, json=json)
            # print("url ", response.url)
            if 200 <= response.status_code < 300:
                return response
            else:
                raise RequestException(response.text)
        except RequestException as e:
            print(f"Error in API handler: {e}")
            if error_msg:
                print(error_msg)
            sleep(60)
