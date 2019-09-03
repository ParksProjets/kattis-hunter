"""

Generate C++ code for getting information about birds.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""


def get_num_birds(N: int, **kargs):
    "Get the number of birds for round rindex and rindex+1."

    return f"""
        if (pState.getRound() == {N})
            mCacheNumber = pState.getNumBirds();
        if (pState.getRound() == {N+1})
            WaitForMs(30 * (mCacheNumber + (20 * pState.getNumBirds())));
    """
