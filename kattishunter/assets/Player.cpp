#include "Player.hpp"
#include <cstdlib>
#include <iostream>


namespace ducks
{

/*{STATIC_CODE}*/

/*{STATIC_CODE_ENVHASH}*/

/*{STATIC_CODE_SKIP}*/

Player::Player()
{
}

Action Player::shoot(const GameState &pState, const Deadline &pDue)
{
    /*{SHOOT_SKIP}*/

    /*{SHOOT}*/

    return cDontShoot;
}

std::vector<ESpecies> Player::guess(const GameState &pState, const Deadline &pDue)
{
    std::vector<ESpecies> lGuesses(pState.getNumBirds(), SPECIES_UNKNOWN);

    /*{GUESS_SKIP}*/

    /*{GUESS}*/

    return lGuesses;
}

void Player::hit(const GameState &pState, int pBird, const Deadline &pDue)
{
    /*{HIT}*/
}

void Player::reveal(const GameState &pState, const std::vector<ESpecies> &pSpecies, const Deadline &pDue)
{
    /*{REVEAL_SKIP}*/

    /*{REVEAL}*/
}


} /*namespace ducks*/
