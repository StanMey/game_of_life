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

    def get_ruleset(self, rules):
        """

        :return:
        """
        split_rules = rules.split("/")
        birth_rule = list(map(int, split_rules[0].split("B")[1]))
        survive_rule = list(map(int, split_rules[1].split("S")[1]))

        rule_set = birth_rule + survive_rule
        rule_set = tuple(dict.fromkeys(sorted(rule_set)))
        return rule_set

    def next_state(self, rules, neighbours):
        """
        :param rules:
        :param neighbours: gets an array of all the values of the neighbours
        :return: whether a cell lives or dies
        """
        nb_amount = sum(neighbours)
        if nb_amount in rules:
            return 1
        else:
            return 0

    def update(self) -> World:
        """
        Updates the state of the world to the next generation. Uses rules for evolution.

        :return: New state of the world.
        """
        self.generation += 1
        current_rules = self.get_ruleset(self.rule_set)

        # make a new world
        new_world = World(110)

        # TODO: Do something to evolve the generation
        for x in range(0, self.get_world().height):
            for y in range(0, self.get_world().width):
                new_world.set(x, y, value=self.next_state(current_rules, self.get_world().get_neighbours(x, y)))

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
