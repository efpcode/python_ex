#!/usr/bin/env python3
import argparse
from .game.guess_the_nr import guessing_game


def set_args():
    """"""
    # Setting cmd-line arguments.
    game_inputs = argparse.ArgumentParser(
        description="The list of arguments available in the game guesser "
                    "game.")

    game_inputs.add_argument("MinimumValue", metavar='min_val', type=int,
                             help="sets the starting value for guessing "
                                  "range.", default=None)
    game_inputs.add_argument("MaximumValue", metavar='max_val', type=int,
                             help="sets the stop value for guessing range.",
                             default=None)
    game_inputs.add_argument("Lives", metavar='lives', type=int, nargs='?',
                             help=" optional argument that sets the number "
                                  "of lives the user has before hitting a "
                                  "game over.", default=5)

    # Instantiate parameters passed.
    parameters = game_inputs.parse_args()
    print(parameters)

    # Unpacking parameters from instance.
    min_val = parameters.MinimumValue
    max_val = parameters.MaximumValue
    lives = parameters.Lives
    return min_val, max_val, lives


def main():
    min_val, max_val, lives = set_args()
    guessing_game(min_val=min_val, max_val=max_val, lives=lives)


if __name__ == "__main__":
    main()
