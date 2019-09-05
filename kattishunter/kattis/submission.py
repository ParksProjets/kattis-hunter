"""

Submit files for a Kattis problem.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
import re
from typing import Dict, List, Text
import requests
import logging

from .login import login

logger = logging.getLogger(__name__)


# Base headers to use.
HEADERS = {
    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def retreive_csrf_token(config: Dict, pid: Text, retry = True):
    "Retreive CSRF token from the submit page."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]

    # Make the GET request.
    url = config["url"]["submit"].format(pid=pid)
    cookies = config["cache"].get("cookies", {})
    res = requests.get(url, headers=headers, cookies=cookies,
        allow_redirects=False)
    config["cache"]["cookies"] = {**cookies, **res.cookies.get_dict()}

    # Not logged, try to login first.
    if res.status_code != 200:
        if not retry:
            logger.critical("Can't retrieve submit page from Kattis.")
        login(config)
        return retreive_csrf_token(config, pid, False)

    # Find the CSRF token in response body.
    pattern = r"name=\"csrf_token\".*?value=\"([0-9a-z]+)\""
    match = re.search(pattern, res.text)
    if match is None:
        logger.critical("Can't find CSRF token in submit page.")

    return match.group(1)



def read_file(filename: Text):
    "Read a single file to send."

    with open(filename, "rb") as file:
        return file.read()


def read_files(files: List[Text]):
    "Read files to send."

    return [(
        "sub_file[]",
        (path.basename(file), read_file(file), "application/octet-stream")
    ) for file in files]



def submit_kattis(config: Dict, pid: Text, files: List[Text]):
    "Submit files to a Kattis problem."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]

    # Setup data to send.
    data = {
        "csrf_token": retreive_csrf_token(config, pid),
        "type": "files",
        "sub_code": "",
        "problem": pid,
        "language": "C++",
        "submit": "Submit",
        "submit_ctr": 10
    }

    # URL, files and cookies to use.
    url = config["url"]["submit"].format(pid=pid)
    files = read_files(files)
    cookies = config["cache"]["cookies"]

    # Make the POST request.
    logger.debug("Submitting %d files for '%s'.", len(files), pid)
    res = requests.post(url, data=data, files=files, headers=headers,
        cookies=cookies)
    config["cache"]["cookies"] = {**cookies, **res.cookies.get_dict()}

    # Find submisson ID.
    match = re.match(r"^.*/submissions/([0-9]+)$", res.url)
    if not match:
        logger.critical("Can't find submission ID from URL '%s'.", res.url)

    sid = match.group(1)
    logger.debug("Files sent to submission %s.", sid)
    return sid
