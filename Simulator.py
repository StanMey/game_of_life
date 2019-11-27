from World import *


class Simulator:
    """
    Game of Life simulator. Handles the evolution of a Game of Life ``World``.
    Read https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life for an introduction to Conway's Game of Life.
    """

    def __init__(self, rules, world=None):
        """
        Constructor for Game of Life simulator.

        :param world: (optional) environment used to simulate Game of Life.
        """
        self.generation = 0
        self.rule_set = rules
        if world == None:
            self.world = World(20)
        else:
            self.world = world

    def is_normal_game(self, rules):
        """
        Returns if the normal game is started (the String with the rule has no /A component)
        :param rules: The String with the rules of the game
        :return: Bool that says if the normal game is started
        """
        return len(rules.split("/")) == 2

    def get_fertility_set(self, fertile_numb):
        """
        Gives back the set of ages on which a cell is fertile
        :param fertile_numb: The number that is given after the /A in the rule string
        :return: A tuple which holds the ages on which a cell is fertile
        """
        min_numb = 2
        max_numb = fertile_numb - 2

        if max_numb < min_numb:
            result_tupl = (2, 3)
        else:
            result_tupl = tuple([x for x in range(min_numb, max_numb + 1)])

        return result_tupl

    def get_fertile_cells_amount(self, neighbours, fert_set):
        """
        Gets the total count of fertile neighbours of a particular cell
        :param neighbours: The list with the values of all the neighbours of this particular cell
        :param fert_set: A tuple which holds the ages on which a cell is fertile
        :return: The amount of fertile neighbours
        """
        fert_count = 0

        for neighbour in neighbours:
            if neighbour in fert_set:
                fert_count += 1

        return fert_count

    def get_ruleset(self, rules):
        """
        Gets a rule set in the form of a String and returns a set of rules
        :return: a set with all the amounts of neighbours on which a cell comes back to life
        """
        if self.is_normal_game(rules):
            split_rules = rules.split("/")
            birth_rule = list(map(int, split_rules[0].split("B")[1]))
            survive_rule = list(map(int, split_rules[1].split("S")[1]))

            # add the two rules together
            rule_set = birth_rule + survive_rule

            # sort the list and remove the duplicates
            rule_set = tuple(dict.fromkeys(sorted(rule_set)))
        else:
            split_rules = rules.split("/")
            birth_rule = tuple(map(int, split_rules[0].split("B")[1]))
            survive_rule = tuple(map(int, split_rules[1].split("S")[1]))
            fertile_rule = self.get_fertility_set(int(split_rules[2].split("A")[1]))
            # append all the rules into one tuple
            rule_set = (birth_rule, survive_rule, fertile_rule)

        return rule_set

    def next_state(self, normal_game, current_state, rules, neighbours):
        """
        Gives back the new value of a particular cell
        :param normal_game: if a normal game is started (bool)
        :param current_state: The value of the current cell
        :param rules: gets a set of rules on which defines the behaviour of the cell
        :param neighbours: gets an array of all the values of the neighbours
        :return: The new value of the cell
        """
        if normal_game:
            # playing a normal game
            nb_amount = sum(1 for x in neighbours if x > 0)
            if nb_amount in rules:
                # the cell gives birth/survives
                result = 1
            else:
                # the cell dies
                result = 0
        else:
            # not playing a normal game
            if current_state == 0:
                # current cell is dead
                fertile_neighbours = self.get_fertile_cells_amount(neighbours, rules[2])
                if fertile_neighbours in rules[0]:
                    # There are enough fertile neighbours to be born
                    max_life = max(rules[2]) + 2
                    result = max_life
                else:
                    # There aren't enough neighbours to be born
                    result = 0
            else:
                # current cell is alive
                alive_neigh = sum(1 for x in neighbours if x > 0)
                if alive_neigh in rules[1]:
                    # The cell survives
                    result = current_state
                else:
                    # The cell doesn't survive
                    result = current_state - 1

        return result

    def update(self) -> World:
        """
        Updates the state of the world to the next generation. Uses rules for evolution.
        :return: New state of the world.
        """
        self.generation += 1
        current_rules = self.get_ruleset(self.rule_set)
        normal_game = self.is_normal_game(self.rule_set)

        # make a new world
        new_world = World(110)

        # retrieve the next value and update every cell
        for x in range(0, self.get_world().height):
            for y in range(0, self.get_world().width):

                # get the values for the current state and current neighbours
                current_state = self.get_world().get(x, y)
                curr_neighbours = self.get_world().get_neighbours(x, y)

                # get new value and update the new world
                new_world.set(x, y, value=self.next_state(normal_game, current_state, current_rules, curr_neighbours))

        self.set_world(new_world)
        return self.world

    def get_generation(self):
        """
        Returns the value of the current generation of the simulated Game of Life.

        :return: generation of simulated Game of Life.
        """
        return self.generation

    def get_world(self):
        """
        Returns the current version of the ``World``.

        :return: current state of the world.
        """
        return self.world

    def set_world(self, world: World) -> None:
        """
        Changes the current world to the given value.

        :param world: new version of the world.

        """
        self.world = world
