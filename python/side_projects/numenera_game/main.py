#!/usr/bin/env python3

from roll_a_die import Die
from pprint import pprint
from distutils.util import strtobool


def initial_setup() -> object:
    name = input("Please enter your name? : ")
    while True:
        try:
            isinstance(name, str)
        except (ValueError, TypeError) as e:
            print(f"Please type a name!:\nSee what went wrong:\n {e}")
            continue
        else:
            die_collection = Die.die_collection(owner=name)
            return die_collection


def die_choices(die_collection):
    die_options = {f"{i}": die for i, die in
                   enumerate(die_collection, 1)}

    return die_options


def toss_simulator():
    dices = initial_setup()
    dice_option = die_choices(dices)

    while True:
        pprint(dice_option)
        player_choice = input("\nPick your weapon of choice: ")
        try:
            dice_option[player_choice]
        except (KeyError, ValueError) as error:
            print(f"Please pick a valid option! User input -> {error} was "
                  f"not found.")
            continue

        else:
            die = dice_option.get(player_choice)
            print(f"{die.owner} rolls a:\n")
            print(die.roll())

            while True:
                try:
                    text = strtobool(input("Wish to roll again?: "))
                except ValueError:
                    print("Try again")
                    continue
                if text:
                    print(die.roll())
                elif not text:
                    break
                else:
                    continue

            while_exit = strtobool(input("Do you wish to quit (Y) or Do you "
                                       "want "
                                   "to change die (N)??: "))
            if while_exit:
                break
            continue


def main():
    toss_simulator()


if __name__ == "__main__":
    main()
