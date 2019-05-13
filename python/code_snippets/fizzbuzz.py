# Write a program that prints the numbers from 1 to 100.
# But for multiples of three print "Fizz" instead of the number
# and for the multiples of five print "Buzz".
# For numbers that are multiples of both three and five print "FizzBuzz".

from sys import argv
from decimal import Decimal, DecimalException

def fizzbuzz_game():
    endpoint = user_input()

    # Catches None Value inhert from func call test_user_input
    if not endpoint:
        return
    else:
        values = list(map(game_logic, range(1, endpoint)))
        for i in values:
            print(i)


def game_logic(num):
    if not num % 15:
        return "FizzBuzz"
    elif not num % 3:
        return "Fizz"
    elif not num % 5:
        return "Buzz"
    else:
        return num


def user_input():
    """
    """
    endpoint = input("\n>>> Enter the endpoint value: ")
    endpoint = test_user_input(endpoint)
    return endpoint


def test_user_input(endpoint):
    """
    """
    try:
        end = int(Decimal(endpoint))
    except (DecimalException, TypeError, Exception) as error:
        print(f"\n>>> The invaild input:{endpoint} -> {error} "
              "\n>>> Let's try again!\n")
        fizzbuzz_game()
    else:
        return end


def main():
    print(f"Welcome to {argv[0]}")
    fizzbuzz_game()

if __name__ == "__main__":
    try:
        if argv[1] == "run":
            main()
    except IndexError as error:
        print(
            "To execute script:\n 'python -m {}' run".format(argv[0].replace('.py','')))
