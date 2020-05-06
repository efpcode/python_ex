from random import randint
from time import sleep


class Die:
    """
    Object that represents any type of die or dice.

    Attributes
    ----------
    nr_faces : int
        The number of sides or faces a singular die has.
    owner : str
        The owner of the owner of the die i.e. the one the die belongs to.

    Methods
    -------
    roll()
        Represents the a toss of a die.
    shake()
        Add some needed tension to a roll of the die.
    roll_again()
        Performance a new roll with die.

    gamble(cost_effort="1", effort=20)
        Staticmethod called 'gamble', lowers the difficulty of a given task or
        action from game master. Returns new value for effort.

    d10_die(sides="10", owner="d10")
        A classmethod that returns a new Die object for die with 10 sides or
        faces and owner.

    die_collection(owner='all_dice')
        A classmethod that generates a set of types of dice in one go.

    See Also
    --------
    Die.d04_die: to instantiate 4 faced die or sided die.
    Die.d06_die: to instantiate 6 faced die or sided die.
    Die.d10_die: to instantiate 10 sided or faced die.
    Die.d12_die: to instantiate 12 faced die or sided die.
    Die.d20_die: to instantiate 20 faced or sided die.
    Die.die_collection: to instantiate all dice in Die class.
    """
    nr_faces: int
    owner: str

    def __init__(self, nr_faces=None, owner=None):
        """
        Constructor class

        Parameters
        ----------
        nr_faces : int
            The 'nr_faces' parameter references the number of sides of
            the die.
        owner : str
            The 'owner' parameter is the owner of the player who
            tossing the die e.g. in tabletop RPG this can be set to 'GM' for
            Game Master.

        Returns
        -------
        None : None
            Constructor class shouldn't return anything. However added a
            message to flag that die was created.

        See Also
        --------
        Die.d04_die: to instantiate 4 faced die or sided die.
        Die.d06_die: to instantiate 6 faced die or sided die.
        Die.d10_die: to instantiate 10 sided or faced die.
        Die.d12_die: to instantiate 12 faced die or sided die.
        Die.d20_die: to instantiate 20 faced or sided die.
        """
        self.nr_faces = nr_faces
        self.owner = owner

        try:
            assert (isinstance(self.nr_faces, int))
            assert (isinstance(self.owner, str))

        except AssertionError:
            message = f"Value error nr_faces: {self.nr_faces} must be int. " \
                      f"\nValue error owner: {self.owner} must " \
                      f"be str."
            raise ValueError(message)

    def __repr__(self) -> str:
        """
       The die class represented with it's value.

        Returns
        -------
        str : str or None
            The Die objects and the value of its attributes.
        """
        return f"{self.__class__.__name__}(nr_faces= {self.nr_faces}, " \
               f"owner= '{self.owner}')"

    def roll(self) -> int:
        """
        The methods returns random int, simulating a roll die.

        Returns
        -------
        int : int
            Returns random integers based on the number of faces or sides of
            the die.

        See Also
        --------
        random.randint : to see randomization function.

        """
        return randint(1, self.nr_faces)

    def shake(self) -> str:
        """
        The shake method simulates a owner shaking the die before a toss.

        Returns
        -------
        str
            A message of a tossing scenario of a die.

        See Also
        --------
        random.randint : for randomization algorithm.
        time.sleep : for hold or pause of execution of code.
        """
        message = "Shake.. shake ... .... shake!\n"
        interval = randint(1, 3)
        print(f"Player: {self.owner} is shaking the die")
        for i in range(0, interval):
            print(message)
            sleep(interval)
        return f"Player Tosses Die!\nAnd die rolls and stops at:"

    def roll_again(self) -> int:
        """
        Performance a new roll of the die.
        Returns
        -------
        int : int
            Returns the int generated from by the call to roll method in Die
            class.

        See Also
        --------
        Die.roll : for more information about method call.
        """
        message = f"Player: {self.owner} tosses again!"
        print(message)
        return Die.roll(self)

    # Effort calculator

    @staticmethod
    def gamble(cost_effort: int = 1, effort: int = 20) -> int:
        """
        The method is a risk and reward calculator, the owner or player
        can lower the difficulty of a task by spending a resource called
        'effort' in Numenera.

        Parameters
        ----------
        cost_effort : int
            The amount of the resource a user is willing to spend.
            Integer passed must be > 0

        effort : int
            The current value of the resource called 'effort' in Numnera.
            Integer passed must be > 0

        Returns
        -------
        effort : int
            The new calculated value after spending the resource called
            'effort'.

        Raises
        ------
        AssertionError
            If parameters 'cost_effort' or 'effort' is < 0 and if sum
            of parameters is < 0. Return value for 'effort' is set to 0.

        ValueError, TypeError
            If parameter is not a integer.
        """
        condition = "".join(
            (str(cost_effort), str(effort)))
        try:
            assert(condition.count("-") == 0)
            assert(effort - cost_effort >= 0)
            isinstance(int(condition.replace("-", "")), int)
        except (ValueError, TypeError) as e:
            print(f"Type of 'cost_effort' and 'effort' must be int:\n "
                  f"\ntype({cost_effort}) -> {type(cost_effort)}"
                  f"\ntype({effort}) -> {type(effort)}")
            raise ValueError(e)

        except AssertionError:
            effort: int = 0
            message3 = f"Player cannot use effort, since its " \
                       f"depleted!\nCurrent value of effort left {effort}."
            print(message3)
            return effort

        message = f"Player applies effort to toss!"
        effort -= cost_effort
        message2 = f"Players effort reduce to {effort}"
        print(message, message2)
        return effort

    # Dice Factory

    @classmethod
    def d20_die(cls, sides=20, owner="d20") -> object:
        return cls(nr_faces=sides, owner=owner)

    @classmethod
    def d10_die(cls, sides=10, owner="d10") -> object:
        return cls(nr_faces=sides, owner=owner)

    @classmethod
    def d06_die(cls, sides=6, owner="d06") -> object:
        return cls(nr_faces=sides, owner=owner)

    @classmethod
    def d12_die(cls, sides=12, owner="d12") -> object:
        return cls(nr_faces=sides, owner=owner)

    @classmethod
    def d08_die(cls, sides=8, owner="d08") -> object:
        return cls(nr_faces=sides, owner=owner)

    @classmethod
    def d04_die(cls, sides=4, owner="d04") -> object:
        return cls(nr_faces=sides, owner=owner)

    # Multiple dice factory.
    @classmethod
    def die_collection(cls, owner: str = "all_dice") -> object:
        """
        The classmethod creates all the dice available in Die class.

        Parameters
        ----------
        owner : str
        The 'owner' is reference the owner of the die. The one who is
        performing a toss with the die.

        Returns
        -------
        all_dice : list(Die)
            The 'all_dice' is list object, where list items are a specific
            die. The range of dice created are from 4 sided or 4 faced to 20
            sided or 20 faced die.
        """
        die_type = [4, 6, 8, 12, 20]
        all_dice = [cls(nr_faces=side, owner=owner) for side in die_type]
        return all_dice


def simulation_of_game():
    """
    A function that simulates a game scenario. This function is a hold-on
    function and should be deleted from code base after testing has been done.
    Returns
    -------
    str
        A scenario played out.

    """
    name = input("Enter a owner: ")
    gm_intro = (
        f"Welcome to {name}, this is a brand new game! You're a character \n"
        f"you in a RPG game and there's a creature looking at you! "
        f"The creatures approaches fast!\n"
        f"Take action!"
    )
    gm_dice = Die.d10_die(owner="Game Master")
    monster_points = gm_dice.roll()
    monster_points *= 2
    player_dice = Die.d20_die(owner=name)
    print(gm_intro)

    while monster_points > 0:
        super_point = 0
        print("Monster roars!")
        print("You swing your blade!")
        user_choice = input("Put effort into roll of die?: ")
        if user_choice == "yes":
            super_point = player_dice.gamble(3) / 3

        player_dice.shake()
        die_toss = player_dice.roll()
        print(f"Player rolled: {die_toss}")
        attack_points: int = round((die_toss / 3) + super_point)
        print(f"And attacks with: {attack_points}")
        monster_points -= attack_points

    else:
        print("Monster cries out and blood flows!")
