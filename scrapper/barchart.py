# import json
from urllib.parse import unquote

import requests

# from bs4 import BeautifulSoup

s = requests.session()


def web_scrapper(url: str) -> requests.models.Response:
    start_url = url
    start_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    s.get(start_url, headers=start_headers)
    cookie_dict = s.cookies.get_dict()
    cookie_str = "; ".join([x + "=" + y for x, y in cookie_dict.items()])  # get all the cookies you need
    cookie_str += "; bcFreeUserPageView=0;"
    xsrf_token = unquote(cookie_dict["XSRF-TOKEN"])  # it was url encoded
    headers = {
        "Accept": "*/*",
        "Cookie": cookie_str,
        "Referer": "https://www.barchart.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Xsrf-Token": xsrf_token,
    }
    data = s.get(url, headers=headers)
    if data.status_code == 200:
        print("Authentification Successfull")
    else:
        print(f"Authentification Failed with status code {data.status_code}")
    return data


data = web_scrapper("https://www.barchart.com/")
