# Protocol for getting all wanted data

At each execution, Kattis gives us a runtime between 0.00 and 16.00. With that
range we can encode about 10.5 bits of information.


## Overview of the algorithm

```py
# Assume that there is the same number of rounds for all environnements.
NUM_ROUNDS = 10


for i in range(number_of_env):

    # First, retrieve the number of birds for each round of the env.
    for j in range(0, NUM_ROUNDS, 2):
        get("number of birds of round j and j+1")

    # Retrieve the first directions of the birds from the first round. We do
    # that for knowing in which env we currently are.
    get("directions of first birds")

    # Get species of each bird.
    for k in range(0, NUM_ROUNDS * NUM_BIRDS_ENV, 4):
        get("species of birds k, k+1, k+2 and k+3")

    # Finally retrieve the directions of each bird.
    for k in range(0, NUM_ROUNDS * NUM_BIRDS_ENV, 3):
        get("directions of birds k, k+1 and k+2")
```


## Get the number of birds
