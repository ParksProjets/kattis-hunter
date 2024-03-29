"""

Submit a test and return CPU time.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import re
import time
import requests
from typing import Dict, List, Text
import logging

from .login import login
from .submission import HEADERS, submit_kattis

logger = logging.getLogger(__name__)


# Interval betwwen two logins (in s).
LOGIN_INTERVAL = (6 * 3600)

# Time between two checks (in s).
CHECK_INTERVAL = 3


def retrieve_kattis_result(config: Dict, sid: Text):
    "Retreive result from Kattis."

    # Setup headers to send.
    headers = HEADERS.copy()
    headers["User-Agent"] = config["cache"]["user-agent"]

    # Make the GET request.
    url = config["url"]["result"].format(sid=sid)
    cookies = config["cache"].get("cookies", {})
    res = requests.get(url, headers=headers, cookies=cookies,
        allow_redirects=False)
    config["cache"]["cookies"] = {**cookies, **res.cookies.get_dict()}

    # Not logged, try to login first.
    if res.status_code != 200:
        login(config)
        return None

    # Check if the program execution is completed.
    result = res.json()
    if result["status_id"] < 6:
        return None  # Running or compiling.

    # Make sure we didn't got "Compile Error".
    if "Compile Error" in result["component"]:
        logger.critical("Submission got 'Compile Error'.")

    # Retrieve CPU time.
    match = re.search(r"cpu\">([0-9]+\.[0-9]+)", result["component"])
    rtime = round(float(match.group(1)) * 100)

    # Count number of successful tests.
    numok = result["testcases_number"]
    numok -= int("rejected\" title" in result["component"])

    return (rtime, numok)



def submit(config: Dict, files: List[Text]):
    "Submit a test and return CPU time."

    # We logged too much time ago, log again now.
    logintime = config["cache"].get("login-time", 0)
    if time.time() - logintime > LOGIN_INTERVAL:
        login(config)

    # Submit generated files to Kattis.
    pid = config["url"]["pid"]
    sid = submit_kattis(config, pid, files)

    # Wait until we got the CPU time.
    result = None
    while result is None:
        time.sleep(CHECK_INTERVAL)
        result = retrieve_kattis_result(config, sid)

    logger.debug("Submission done (cpu=%s, numok=%s).", *result)
    return result
