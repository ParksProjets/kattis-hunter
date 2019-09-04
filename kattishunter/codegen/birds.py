"""

Generate C++ code for getting information about birds.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""


def num_birds_shoot(N: int, **kargs):
    "Get the number of birds for round rindex and rindex+1."

    return f"""
        if (pState.getRound() == {N})
            mCacheNumber = pState.getNumBirds();
        if (pState.getRound() == {N+1})
            WaitForMs(30 * (mCacheNumber + (20 * pState.getNumBirds())));
    """



def species_guess(**kargs):
    "Guess function for getting species."

    return """
        std::vector<ESpecies> lSGuesses(pState.getNumBirds(), SPECIES_PIGEON);
        return lSGuesses;
    """


def species_reveal(N: int, **kargs):
    "Reveal function for getting species."

    return """
        for (int i = 0; i < pSpecies.size(); i++) {
            mCacheIndex++;

            if (mCacheIndex > %s) {
                mCacheNumber += pSpecies[i] * mBaseShift;
                mBaseShift *= 6;
            }

            if (mCacheIndex == %s)
                WaitForMs(40 * mCacheNumber);
        }
    """ % (N, N+3)
