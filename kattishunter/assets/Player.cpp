#include "Player.hpp"
#include <cstdlib>
#include <iostream>


namespace ducks
{

/*{STATIC_CODE}*/

Player::Player()
{
}

Action Player::shoot(const GameState &pState, const Deadline &pDue)
{
    /*{SHOOT_BEFORE}*/
    /*{SHOOT}*/


    // This line choose not to shoot
    return cDontShoot;

    //This line would predict that bird 0 will move right and shoot at it
    //return Action(0, MOVE_RIGHT);
}

std::vector<ESpecies> Player::guess(const GameState &pState, const Deadline &pDue)
{
    /*{GUESS}*/

    std::vector<ESpecies> lGuesses(pState.getNumBirds(), SPECIES_UNKNOWN);
    return lGuesses;
}

void Player::hit(const GameState &pState, int pBird, const Deadline &pDue)
{
    /*
     * If you hit the bird you are trying to shoot, you will be notified through this function.
     */
    std::cerr << "HIT BIRD!!!" << std::endl;
}

void Player::reveal(const GameState &pState, const std::vector<ESpecies> &pSpecies, const Deadline &pDue)
{
    /*{REVEAL}*/
}


} /*namespace ducks*/
