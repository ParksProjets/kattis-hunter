"""

Generate C++ code for the final code.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""

from typing import List, Text


# Player class attributes.
ANSWER_ATTRIBUTES = """

void findEnvironmentIndex(const GameState &pState);

int mEnvIndex = 0;
int mCurrentScore = 0;
std::vector<ESpecies> mGuesses;

"""


# Static code for answer.
ANSWER_STATIC = """
void Player::findEnvironmentIndex(const GameState &pState)
{
    uint64_t hash = pState.getNumBirds();
    for (size_t i = 0; i < pState.getNumBirds(); i++)
        hash += (pState.getBird(i).getObservation(0) << (i*4 + 5));

    for (; mEnvIndex < cEnvHashLen; mEnvIndex++) {
        if (cEnvHashes[mEnvIndex] == hash)
            break;
    }
}
"""


# Shoot function content.
ANSWER_SHOOT = """
    int turn = pState.getBird(0).getSeqLength();
    if (pState.getRound() == 0 && turn == 1)
        findEnvironmentIndex(pState);

    if (mEnvIndex == cEnvHashLen || mCurrentScore >= kTargetScores[mEnvIndex])
        return cDontShoot;

    auto &dirs = kAllDirections[mEnvIndex][pState.getRound()];
    if (turn > dirs.size())
        return cDontShoot;

    mCurrentScore -= 1;
    return Action(turn - 1, (EMovement)dirs[turn - 1]);
"""


# Hit function content.
ANSWER_HIT = """
    mCurrentScore += 2;
"""


# Guess function content.
ANSWER_GUESS = """
    mGuesses = std::vector<ESpecies>(pState.getNumBirds(), SPECIES_UNKNOWN);
    if (mEnvIndex == cEnvHashLen)
        return mGuesses;

    auto &species = kAllSpecies[mEnvIndex][pState.getRound()];
    int L = std::min((int)pState.getNumBirds(), kTargetScores[mEnvIndex] - mCurrentScore);
    for (int i = 0; i < L; i++)
        mGuesses[i] = (ESpecies)species[i];

    return mGuesses;
"""


# Reveal function content.
ANSWER_REVEAL = """
    for (size_t i = 0; i < pSpecies.size(); i++) {
        if (pSpecies[i] != SPECIES_UNKNOWN)
            mCurrentScore += ((pSpecies[i] == mGuesses[i]) * 2) - 1;
    }
"""



def gen_bird_array(envs: List, name: Text, etype: Text):
    "Generate a static array for birds."

    upper = name.capitalize()
    result = "using Env%s = std::vector<int>[10];\n" % (upper)
    result += "Env%s kAll%s[%d] = {\n" % (upper, upper, len(envs))

    for i, e in enumerate(envs):
        result += " " * 4 + "{  // Environment %d.\n" % (i+1)
        for r in e["rounds"]:
            if r[name]:
                result += " " * 8 + "{ " + ", ".join(map(str, r[name])) + " },\n"
            else:
                result += " " * 8 + "{ 0 },\n"
        result += " " * 4 + "},\n"

    result += "};\n"
    return result


def answer_static(R: List, Scores: List, **kargs):
    "Static code for the final code."

    result = gen_bird_array(R, "directions", "EMovement") + "\n"
    result += gen_bird_array(R, "species", "ESpecies") + "\n"

    result += "int kTargetScores[%s] = { " % len(R)
    result += ", ".join(map(str, Scores)) + " };\n"

    return result
