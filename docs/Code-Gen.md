# Code generation

## Wait for a given time (ms)

As we use CPU time to retieve information from a Kattis execution, we have to
make our program waiting for the right amount of time. We can't use the `sleep`
function because it does not use CPU (the Linux kernel puts the process in sleep
mode). This why we are using a busy waiting procedure.

```c++
#include <chrono>


void WaitForMs(int target)
{
    auto begin = std::chrono::high_resolution_clock::now();

    while (true) {
        auto end = std::chrono::high_resolution_clock::now();
        auto dur = end - begin;
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(dur).count();
        if (ms >= target)
            exit(1);  // Cause a runtime error.
    }
}

```


## Get the number of birds in each round

This is the first thing we need to do: knowing how many birds we have in each
round. As there are between 1 and 20 birds per round we can encode two round at
each execution (using a base 20 number). Finally we multiply the encoded number
by 3 to reduce fluctuations of time.

| Parameter | Description               |
|-----------|---------------------------|
| `N`       | Target rounds (N and N+1) |

```c++
Action Player::shoot(const GameState &pState, const Deadline &pDue)
{
    if (pState.getRound() == N)
        mCacheNumber = pState.getNumBirds();
    if (pState.getRound() == (N+1))
        WaitForMs(30 * (mCacheNumber + (20 * pState.getRound())));
}
```


## Get bird species

TODO.

| Parameter | Description             |
|-----------|-------------------------|
| `N`       | Target birds (N to N+3) |

```c++
std::vector<ESpecies> Player::guess(const GameState &pState, const Deadline &pDue)
{
    std::vector<ESpecies> lGuesses(pState.getNumBirds(), SPECIES_PIGEON);
    return lGuesses;
}


void Player::reveal(const GameState &pState, const .. &pSpecies, ..)
{
    for (int i = 0; i < pSpecies.size(); i++) {
        mCacheIndex++;

        if (mCacheIndex > N) {
            mCacheNumber += pSpecies[i] * mBaseShift;
            mBaseShift *= 6;
        }

        if (mCacheIndex == (N+4))
            WaitForMs(10 * mCacheNumber);
    }
}
```


## Get bird directions

TODO.

```c++
Action Player::shoot(const GameState &pState, const Deadline &pDue)
{
    if (pState.getRound() == R && pState.getNumBirds() == N) {

    }
}
```


## Skip an entire environnement

When you are targeting the second environnement you have to skip the first one.
The quickest way to do that is to not shoot during the whole environnement or
kill a Black Stork. But to achieve that you must know first in which
environnement you currently are. For that, we hash the first directions of birds
of the first round of each environnement.

| Parameter | Description                        |
|-----------|------------------------------------|
| `E`       | Index of the current environnement |

```c++
// List of known env hashes.
#define cEnvHashLen 1
uint64_t cEnvHashes[cEnvHashLen] = { 71450663 };


Action Player::shoot(const GameState &pState, const Deadline &pDue)
{
    // Check if it's a known env. It's that's the case, setup skip variables.
    if (pState.getRound() == 0 && pState.getBird(0).getSeqLength() == 1)
        setupEnvSkip(pState);

    // We need to skip this env.
    if (mSkipThisEnv)
        return cDontShoot;
}


void Player::setupEnvSkip(const GameState &pState)
{
    // Calculate hash for this env.
    uint64_t hash = pState.getNumBirds();
    for (int i = 0; i < std::min((int)pState.getNumBirds(), 14); i++)
        hash += ((uint64_t)pState.getBird(i).getObservation(0) << (i*4 + 5));

    // Check if the hash is known.
    int index = 0;
    for (; index < cEnvHashLen; index++) {
        if (cEnvHashes[index] == hash)
            break;
    }

    // Hash was found: env is known, we need to skip it.
    if (index == cEnvHashLen)
        mSkipThisEnv = true;
}
```
