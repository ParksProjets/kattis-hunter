"""

Skip environnements that we h

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import List


def envhash_static(R: List, **kargs):
    "Static code for that contains env hash."

    L = sum(int(e["done"]) for e in R)
    if L == 0: return None

    result = "#define cEnvHashLen %d" % L
    hashes = ", ".join(str(e["hash"]) for e, _ in zip(R, range(L)))
    result += "\nuint64_t cEnvHashes[cEnvHashLen] = { %s };" % hashes

    return result


def envhash_shoot(N: int, E: int, R: List, **kargs):
    "Shoot function for generating env hash."

    Nmax = min(N+2, R[E]["rounds"][0]["num-birds"])
    content = [
        "mCacheNumber += pState.getBird(%s).getObservation(0) * %s;" % (
            i, 9 ** (i-N)) for i in range(N, Nmax)
    ]

    return """
        %s
        WaitForMs(100 * mCacheNumber);
    """ % (("\n" + " " * 8).join(content))



# Static code for skipping an environment.
ENVSKIP_STATIC = """

void Player::setupEnvSkip(const GameState &pState)
{
    uint64_t hash = pState.getNumBirds();
    for (int i = 0; i < pState.getNumBirds(); i++)
        hash += (pState.getBird(i).getObservation(0) << (i*4 + 5));

    int index = 0;
    for (; index < cEnvHashLen; index++) {
        if (cEnvHashes[index] == hash)
            break;
    }

    if (index != cEnvHashLen)
        mSkipThisEnv = true;
}

"""

# Shoot code for skipping an environment.
ENVSKIP_SHOOT = """
    if (pState.getRound() == 0 && pState.getBird(0).getSeqLength() == 1)
        setupEnvSkip(pState);
    if (mSkipThisEnv)
        return cDontShoot;
"""

# Guess function for skipping an environment.
ENVSKIP_GUESS = """
    if (mSkipThisEnv)
        return lGuesses;
"""

# Reveal function for skipping an environment.
ENVSKIP_REVEAL = """
    if (mSkipThisEnv)
        return;
"""
