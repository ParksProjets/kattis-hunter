"""

Intervals for running Kattis Hunter.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

import time
import random
from datetime import datetime
from dateutil import parser
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


def add_noise(ttime: int):
    "Add some noise on the given time."

    l = random.uniform(0, 1)
    return ttime + (l * ttime * 0.15)



def time_next_interval(inters: List[Tuple], tnow: int):
    "Time to wait for being in the next interval."

    # We are before first interval.
    if tnow < inters[0][0]:
        return add_noise(inters[0][0] - tnow)

    # We are after the last interval.
    if tnow >= inters[-1][1]:
        return add_noise(((24 * 3600) - tnow) + inters[0][0])

    # Find interval right before and after us.
    for t1, t2 in zip(inters, inters[1:]):
        if tnow >= t1[1] and tnow < t2[0]:
            break
    else:
        return -1  # We are already in an interval.

    return add_noise(t2[0] - tnow)



def wait_in_interval(inters: List[Tuple], tnow: int):
    "Wait a time in the given interval."

    # Find the interval in which we currently are.
    for (tfrom, tto, tint) in inters:
        if tfrom <= tnow and tnow < tto:
            break
    else:
        logger.critical("Can't find interval for %d.", int(tnow))

    return add_noise(tint)



def wait_interval(intervals: List[Tuple]):
    "Wait for the next run, according to interval configuration."

    # Caclulate the number of seconds from midnight.
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tnow = (now - midnight).total_seconds()

    # Get time to wait.
    twait = time_next_interval(intervals, tnow)
    if twait == -1:
        twait = wait_in_interval(intervals, tnow)

    # Now wait for some time.
    logger.info("We are waiting for %dmin %ds.", twait // 60, twait % 60)
    time.sleep(twait)



def decode_intervals(intervals: List[Dict]) -> List[Tuple]:
    "Decode interval list from config."

    # Last midnight time.
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Unserialize times.
    return [(
        (parser.parse(info["from"]) - midnight).total_seconds(),
        (parser.parse(info["to"]) - midnight).total_seconds(),
        (parser.parse(info["interval"]) - midnight).total_seconds()
    ) for info in intervals]
