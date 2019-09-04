"""

Submit a test and return CPU time.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import time

from .submission import submit_kattis


# Time to wait before checking Kattis result (in s).
TIME_WAIT_CHECK = 25


def retrieve_kattis_result():
    "Retreive result from Kattis."

    # TODO.



def submit(config: Dict, files: List[Text]):
    "Submit a test and return CPU time."

    pid = config["url"]["pid"]
    submit_kattis(config, pid, files)

    # TODO: maybe check several times.
    time.sleep(TIME_WAIT_CHECK)

    # TODO: retrieve CPU time and number of correct env.
