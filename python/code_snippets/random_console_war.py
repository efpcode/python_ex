#!/usr/bin/env python

"""The script has random match generator for consoles. Two consoles
roll a die and battle it out.

Names of consoles where stolen from wikipedia.
If you missing a console just added it as a list item in 'consoles'.
"""
from time import sleep
from random import choices

consoles = [
    "Magnavox Odyssey",
    "Ping-O-Tronic",
    "Atari's Home Pong",
    "Atari 5200",
    "Epoch Cassette Vision",
    "Atari 7800",
    "Nintendo Entertainment System (Nes)",
    "Super Nintendo Entertainment System (Snes)",
    "Atari XEGS",
    "Nintendo 64",
    "Sega Master System",
    "Commodore 64 Games System",
    "PC Engine",
    "Neo-Geo",
    "TurboGrafx-16",
    "Super Famicon",
    "CD-i",
    "Sega CD",
    "Sega 32X",
    "Neo-Geo CD",
    "Amiga CD32",
    "Atari Jaguar",
    "Apple Bandai Pippin",
    "Sony PlayStation",
    "Nintendo 64DD",
    "Sega Dreamcast",
    "Nuon",
    "Sony PlayStation2",
    "Nintendo Game Cube",
    "Microsoft Xbox",
    "Microsoft Xbox 360",
    "Sony PlayStation 3",
    "Sony PlayStation 4",
    "Nintendo Wii",
    "Nintendo Wii U",
    "Microsoft Xbox One",
    "Nintendo Switch"]

# Random generator, k = number of samples.
roll_die_console1, roll_die_console2 = choices(range(1, 21), k=2)
# Console names
console1, console2= list(set(choices(consoles, k=10)))[:2]  # Tuple unpacking

# Prompting info to user.
print("""\n --- A console war has started between --- """)
print(f"{console1} Vs {console2}")

# Thriller maker (!?)
count = 3  # Starting value for countdown a.k.a. global variable.
print("\nConsoles are shaking dice")

# While-loop continues until expression is False.
while count > 0:
    print("T minus {}!".format(count))  # String formatting.
    count -= 1  # abbreviation <--> count = count - 1.
    sleep(1)   # Waits for 1s before repeating while loop.

print("\n### Roll of dice ###")
print(f"{console1} --> {roll_die_console1}, {console2} --> {roll_die_console2}")
print("\n*** The Outcome *** ")

# Some logic

if roll_die_console1 > roll_die_console2:
    print(f"{console1} is the victor!")
elif roll_die_console1 == roll_die_console2:
    print(f"The dice-battle was a draw!")
else:
    print(f"{console2} won!")
