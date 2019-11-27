import unittest
from unittest import TestCase
from Simulator import *


class TestSimulator(TestCase):
    """
    Tests for ``Simulator`` implementation.
    """
    def setUp(self):
        self.sim = Simulator("B3/S23")

    def test_update(self):
        """
        Tests that the update functions returns an object of World type.
        """
        self.assertIsInstance(self.sim.update(), World)

    def test_get_generation(self):
        """
        Tests whether get_generation returns the correct value:
            - Generation should be 0 when Simulator just created;
            - Generation should be 2 after 2 updates.
        """
        self.assertIs(self.sim.generation, self.sim.get_generation())
        self.assertEqual(self.sim.get_generation(), 0)
        self.sim.update()
        self.sim.update()
        self.assertEqual(self.sim.get_generation(), 2)

    def test_get_world(self):
        """
        Tests whether the object passed when get_world() is called is of World type, and has the required dimensions.
        When no argument passed to construction of Simulator, world is square shaped with size 20.
        """
        self.assertIs(self.sim.world, self.sim.get_world())
        self.assertEqual(self.sim.get_world().width, 20)
        self.assertEqual(self.sim.get_world().height, 20)

    def test_set_world(self):
        """
        Tests functionality of set_world function.
        """
        world = World(10)
        self.sim.set_world(world)
        self.assertIsInstance(self.sim.get_world(), World)
        self.assertIs(self.sim.get_world(), world)

    def test_get_fertility_set(self):
        """
        Tests the returns of the fertility set
        """
        self.assertEqual(self.sim.get_fertility_set(2), (2, 3))
        self.assertEqual(self.sim.get_fertility_set(3), (2, 3))
        self.assertEqual(self.sim.get_fertility_set(4), (2,))
        self.assertEqual(self.sim.get_fertility_set(6), (2, 3, 4))
        self.assertEqual(self.sim.get_fertility_set(9), (2, 3, 4, 5, 6, 7))

    def test_get_fertile_cells_amount(self):
        """
        Tests the function that returns the amount of fertile neighbours
        """
        self.assertEqual(self.sim.get_fertile_cells_amount([0, 1, 0, 0, 1, 0, 0, 0], (2, 3)), 0)
        self.assertEqual(self.sim.get_fertile_cells_amount([0, 4, 0, 4, 1, 6, 0, 5], (4, 5)), 3)
        self.assertEqual(self.sim.get_fertile_cells_amount([0, 1, 0, 7, 1, 2, 0, 0], (2, )), 1)
        self.assertEqual(self.sim.get_fertile_cells_amount([3, 1, 4, 0, 6, 0, 7, 9], (2, 3, 4, 5)), 2)
        self.assertEqual(self.sim.get_fertile_cells_amount([2, 3, 5, 6, 4, 7, 9, 5], (2, 3, 4, 5, 6)), 6)

    def test_is_normal_game(self):
        """
        Tests whether a normal game is started or not:
            - The rule_set has an '/A' included within the string
            - The rule_set doesn't have an 'A' included within the string
        """
        # The /A isn't included
        self.assertEqual(self.sim.is_normal_game("B358/S237"), True)
        self.assertEqual(self.sim.is_normal_game("B8/S23"), True)
        self.assertEqual(self.sim.is_normal_game("B38/S37"), True)

        # The /A is included
        self.assertEqual(self.sim.is_normal_game("B358/S237/A"), False)
        self.assertEqual(self.sim.is_normal_game("B3/S2/A8"), False)
        self.assertEqual(self.sim.is_normal_game("B58/S37/A7"), False)

    def test_get_ruleset(self):
        """
        Tests whether the ruleset gets handled correctly:
            - with a normal game the function will return a set of birth and survival numbers
            - with a not normal game the function will return a set of sets with it's respective information
        """
        # There is a normal game
        self.assertEqual(self.sim.get_ruleset("B358/S237"), (2, 3, 5, 7, 8))
        self.assertEqual(self.sim.get_ruleset("B67/S12"), (1, 2, 6, 7))
        self.assertEqual(self.sim.get_ruleset("B3/S23"), (2, 3))
        self.assertEqual(self.sim.get_ruleset("B2345/S456"), (2, 3, 4, 5, 6))

        # Not a normal game
        self.assertEqual(self.sim.get_ruleset("B358/S237/A6"), ((3, 5, 8), (2, 3, 7), (2, 3, 4)))
        self.assertEqual(self.sim.get_ruleset("B35/S37/A7"), ((3, 5), (3, 7), (2, 3, 4, 5)))
        self.assertEqual(self.sim.get_ruleset("B45/S67/A8"), ((4, 5), (6, 7), (2, 3, 4, 5, 6)))
        self.assertEqual(self.sim.get_ruleset("B2/S3/A5"), ((2,), (3,), (2, 3)))

    def test_next_state(self):
        """
        Tests whether a cell gets correctly evolved based on the rules:
            Normal game
            - The cell survives based on the rules of birth and survival
            - The cell dies based on the rules of birth and survival
            Not normal game
            - The cell comes back to life if enough neighbours are fertile
            - The cell survives and holds its value if the survival condition is met
            - The cell who dies loses something of its value
        """
        # NORMAL GAME
        # the cell survives or lives
        self.assertEqual(self.sim.next_state(True, 1, (2, 3, 5, 7, 8), [0, 1, 0, 0, 1, 0, 0, 0]), 1)
        self.assertEqual(self.sim.next_state(True, 0, (2, 3, 5, 7), [0, 1, 0, 0, 1, 0, 1, 0]), 1)
        self.assertEqual(self.sim.next_state(True, 0, (7, 8), [1, 1, 1, 1, 1, 1, 1, 0]), 1)
        self.assertEqual(self.sim.next_state(True, 1, (1, 8), [0, 1, 0, 0, 0, 0, 0, 0]), 1)
        # the cell dies
        self.assertEqual(self.sim.next_state(True, 1, (2, 3, 5, 7, 8), [0, 0, 0, 0, 0, 0, 0, 0]), 0)
        self.assertEqual(self.sim.next_state(True, 0, (2, 3, 5, 7), [0, 1, 0, 1, 0, 1, 0, 1]), 0)
        self.assertEqual(self.sim.next_state(True, 1, (7, 8), [0, 1, 0, 1, 0, 0, 0, 0]), 0)
        self.assertEqual(self.sim.next_state(True, 0, (1, 8), [0, 0, 0, 0, 0, 0, 0, 0]), 0)


        # NOT NORMAL GAME
        # The cell comes back to life
        self.assertEqual(self.sim.next_state(False, 0, ((3, 5, 8), (2, 3, 7), (2, 3, 4)), [0, 3, 0, 4, 1, 3, 0, 0]), 6)
        self.assertEqual(self.sim.next_state(False, 0, ((3, 5, 8), (2, 3, 7), (2, 3, 4)), [2, 3, 0, 4, 1, 3, 0, 4]), 6)
        self.assertEqual(self.sim.next_state(False, 0, ((3, 4, 5), (2, 3, 7), (2, 3, 4, 5)), [0, 3, 0, 4, 1, 3, 0, 0]), 7)

        # the cell survives
        self.assertEqual(self.sim.next_state(False, 6, ((3, 4, 5), (2, 3, 6, 7), (2, 3, 4)), [0, 3, 1, 4, 1, 3, 2, 0]), 6)
        self.assertEqual(self.sim.next_state(False, 4, ((3, 4, 5), (2, 3, 7), (2, 3, 4)), [0, 3, 0, 0, 1, 3, 0, 0]), 4)
        self.assertEqual(self.sim.next_state(False, 2, ((3, 4, 5), (2, 3, 7), (2, 3, 4)), [5, 3, 2, 4, 1, 3, 0, 4]), 2)

        # the cell dies (remove one lifepoint)
        self.assertEqual(self.sim.next_state(False, 3, ((3, 4, 5), (2, 3, 6), (2, 3, 4)), [5, 3, 2, 4, 1, 3, 0, 4]), 2)
        self.assertEqual(self.sim.next_state(False, 5, ((3, 4, 5), (2, 3, 7), (2, 3, 4)), [0, 3, 5, 0, 1, 3, 0, 0]), 4)
        self.assertEqual(self.sim.next_state(False, 4, ((3, 4, 5), (2, 3, 7), (2, 3, 4)), [5, 3, 2, 4, 1, 3, 5, 4]), 3)


if __name__ == '__main__':
    unittest.main()
