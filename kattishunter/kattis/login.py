"""

Log in KTH Kattis.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import requests
import re
from typing import Dict
import logging

logger = logging.getLogger(__name__)


# Base headers to use.
HEADERS = {
    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def retreive_csrf_token(config: Dict):
    "Retreive CSRF token from the login page."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]

    # Make the GET request and store cookies.
    url = config["url"]["login"]
    res = requests.get(url, headers=headers)
    config["cache"]["cookies"] = res.cookies.get_dict()

    # Find the CSRF token in response body.
    pattern = r"name=\"csrf_token\".*?value=\"([0-9a-z]+)\""
    match = re.search(pattern, res.text)
    if match is None:
        logger.critical("Can't find CSRF token in login page.")

    return match.group(1)



def login(config: Dict):
    "Log in KTH Kattis."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    # Setup data to send.
    data = {
        "csrf_token": retreive_csrf_token(config),
        "user": config["user"]["email"],
        "password": config["user"]["password"],
        "submit": "Submit"
    }

    # URL and cookies to use.
    url = config["url"]["login"]
    cookies = config["cache"]["cookies"]

    # Make the POST request and store cookies.
    res = requests.post(url, data=data, headers=headers, cookies=cookies)
    config["cache"]["cookies"] = {**cookies, **res.cookies.get_dict()}

    if "/users/" not in res.url:
        logger.critical("User credentials are not valid.")
