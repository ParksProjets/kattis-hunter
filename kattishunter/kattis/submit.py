"""

Submit files to a Kattis problem.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import os.path as path
from typing import Dict, List, Text


# Base headers to use.
HEADERS = {
    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def retreive_csrf_token(config: Dict):
    "Retreive CSRF token from the submit page."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]

    # Make the GET request.
    url = config["url"]["submit"]
    res = requests.get(url, headers=headers)

    import ipdb; ipdb.set_trace()

    # Find the CSRF token in response body.
    pattern = r"name=\"csrf_token\".*?value=\"([0-9a-z]+)\""
    match = re.search(pattern, res.text)
    if match is None:
        logger.critical("Can't find CSRF token in submit page.")

    return match.group(1)



def read_file(file: Text):
    "Read a single file to send."

    with open(file, "rb") as sfile:
        return sfile.read()


def read_files(files: List[Text]):
    "Read files to send."

    return [(
        "sub_file[]",
        (path.basename(file), read_file(file), "application/octet-stream")
    ) for file in files]



def submit(config: Dict, pid: Text, files: List[Text]):
    "Submit files to a Kattis problem."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]

    # Setup data to send.
    data = {
        "csrf_token": retreive_csrf_token(config),
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

    # Make the POST request
    res = requests.post(url, data=data, files=files, headers=headers,
        cookies=cookies)

    import ipdb; ipdb.set_trace()
