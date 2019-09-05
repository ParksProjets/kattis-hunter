"""

Generate C++ code for getting information about birds.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import List


def num_birds_shoot(N: int, **kargs):
    "Get the number of birds for round rindex and rindex+1."

    return f"""
        if (pState.getRound() == {N})
            mCacheNumber = (pState.getNumBirds() - 1);
        if (pState.getRound() == {N+1})
            WaitForMs(30 * (mCacheNumber + (20 * (pState.getNumBirds() - 1))));
    """



def species_guess(**kargs):
    "Guess function for getting species."

    return """
        std::vector<ESpecies> lSGuesses(pState.getNumBirds(), SPECIES_PIGEON);
        return lSGuesses;
    """


def species_reveal(N: int, E: int, R: List, **kargs):
    "Reveal function for getting species."

    Nmax = min(N+3, R[E]["num-birds"])

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
    """ % (N, Nmax)



def directions_for(round_i: int, bird_i: int, code_i: int, code_max: int):
    "Generate direction code for the given bird."

    obs_i = bird_i + 1
    content = "mCacheNumber += pState.getBird(%s).getObservation(%s) * %s;" % (
        bird_i, obs_i, (9 ** code_i))

    if code_i == code_max:
        content += "\n%sWaitForMs(20 * mCacheNumber);" % (" " * 12)

    return """
        if (pState.getRound() == %s && pState.getBird(0).getSeqLength() == %s) {
            %s
        }
    """ % (round_i, (obs_i + 1), content)


def directions_shoot(N: int, E: int, R: List, **kargs):
    "Shoot function for getting bird directions."

    index, N0 = (0, N)
    Nmax = min(N+3, R[E]["num-birds"])
    result = ""

    for ri, r in enumerate(R[E]["rounds"]):
        for i in range(N, min(Nmax, index + r["num-birds"])):
            result += directions_for(ri, i - index, N - N0, Nmax - N0 - 1)
            N += 1
        index += r["num-birds"]

    return result
