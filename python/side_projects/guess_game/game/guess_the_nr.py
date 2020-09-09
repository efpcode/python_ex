#!/usr/bin/env python3

from random import randint


def _test_userinput(data_input: int = None) -> int:
    """Function tries to check if 'data_input' parameter is passed
    correctly. Parameter only accepts input of int -type.

    Parameters
    ----------
    data_input : int
        The parameter called "data_input" should only accept int values.

    Returns
    -------
    int
        Function returns int only if 'data_input' parameters is passed
        correctly. Otherwise user is prompted to enter a digit.
    """
    while True:
        try:
            if not data_input:
                data_input = int(input("Please enter a digit :"))
        except (ValueError, TypeError) as input_error:
            print(f"User should enter a digit input "
                  f"results in the following error:\n {input_error}")
            continue
        else:
            return abs(data_input)


def _set_range(min_value: int = None, max_value: int = None) -> int:
    """
    Checks that parameters values passed as 'min_val' and 'max_val' are
    sensible and generates the secrete number.

    Parameters
    ----------
    min_value : int
        The 'min_val' sets the initial value for range.

    max_value : int
        The 'max_value' sets the stop value of range. Note that stop is
        included in the range of digit.

    Returns
    -------
    hidden_nr : int
        The 'hidden_nr' is the secrete number picked by the game.

    Raises
    ------
    ValueError if 'min_val' or 'max_val' are smaller than 0 and if min_val
    is greater than 'max_val'

    See Also
    --------
    random.randint : For more information on how 'hidden_nr' is generated.

    """
    while True:
        try:
            if not (min_value and max_value):
                min_value, max_value = [_test_userinput() for _ in range(2)]

            if (min_value or max_value) < 0:
                raise ValueError

            if max_value < min_value:
                raise ValueError

        except ValueError as error:
            print(f"Please enter a min and max value! Entered input "
                  f"resulted in:\n {type(error)} --> None range")
            min_value, max_value = [_test_userinput() for _ in range(2)]
            continue

        except Exception as all_errors:
            print(f"Something unexpected happened\n:{all_errors}")
            continue

        else:
            hidden_nr = randint(min_value, max_value)
            return hidden_nr


def _start_game() -> str:
    """The function is placeholder for text might be removed in later
    version of the code.
    """
    text = ("Welcome to this number guessing game! Please enter your wanted "
            "guessing range. Start by entering the minimum value first "
            "and then enter max value for the guessing range.")
    return f"***\n{text}\n***"


def guessing_game(
        min_val: int = None, max_val: int = None, lives: int = None) -> str:
    """The function is the main driver for the number guessing game,
    it contains all the process logic and outcomes. The function sets a secrete
    number and prompts user for input. Function ends if user guesses the
    correct value or if lives are depleted.

    Parameters
    ----------
    min_val : int
        The 'min_val' parameter set the lower boundary or initial value for
        a range of digits.
    max_val: int
        The 'max_val' parameter set the upper boundary or last value for
        a range of digits.

    lives: int
        The 'lives' parameter set the number of guess a player has before
        game over.

    Returns
    -------
    Outcomes : str
        The function evaluates user inputs and prompts 'correct' if user
        input was in fact the hidden number.

    """
    print(_start_game())
    if not lives:
        print("Before playing pick the number of lives you will have:\n")
        lives = _test_userinput()
    secrete_nr = _set_range(min_val, max_val)
    print(f"-- Start guessing --\n## Lives left: {lives} ##")
    while lives:
        guess = _test_userinput()

        if secrete_nr == guess:
            print("Correct!")
            return "Hurray"
        elif lives == 1:
            print(f"You have lost! No more lives left -> "
                  f"{lives - 1}\nThe correct answer was -> {secrete_nr}")
            return "You've run out of luck, buddy!"
        else:
            lives -= 1
            print("Try again!")
            print(f"Lives left: {lives}!")
