
import unittest
from unittest.mock import patch

from move import Move

# Tests that calculate_food correctly increases priority for moves leading to food.
class TestCalculateFood(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.is_move_safe = {
            "left":  {"priority": 0},
            "right": {"priority": 0},
            "up":    {"priority": 0},
            "down":  {"priority": 0},
        }
        # food at (2, 2) used across most tests
        self.food_at_2_2 = {"board": {"food": [{"x": 2, "y": 2}]}}

    def _call(self, head, game_state):
        self.bot.calculate_food(self.is_move_safe, head=head, game_state=game_state)

    def _assert_priorities(self, left=0, right=0, up=0, down=0):
        self.assertEqual(self.is_move_safe["left"]["priority"],  left)
        self.assertEqual(self.is_move_safe["right"]["priority"], right)
        self.assertEqual(self.is_move_safe["up"]["priority"],    up)
        self.assertEqual(self.is_move_safe["down"]["priority"],  down)

    def test_food_move_left(self):
        # verifies that left priority increases when food is to the left
        self._call({"x": 3, "y": 2}, self.food_at_2_2)
        self._assert_priorities(left=1)

    def test_food_move_right(self):
        # verifies that right priority increases when food is to the right
        self._call({"x": 1, "y": 2}, self.food_at_2_2)
        self._assert_priorities(right=1)

    def test_food_move_up(self):
        # verifies that up priority increases when food is above
        self._call({"x": 2, "y": 1}, self.food_at_2_2)
        self._assert_priorities(up=1)

    def test_food_move_down(self):
        # verifies that down priority increases when food is below
        self._call({"x": 2, "y": 3}, self.food_at_2_2)
        self._assert_priorities(down=1)

    def test_food_on_multiple_moves(self):
        # verifies that multiple food items increase priority on multiple directions
        self._call({"x": 2, "y": 3}, {"board": {"food": [{"x": 2, "y": 2}, {"x": 3, "y": 3}]}})
        self._assert_priorities(right=1, down=1)

    def test_food_out_of_range(self):
        # verifies that food not adjacent to the head does not increase any priority
        self._call({"x": 2, "y": 2}, {"board": {"food": [{"x": 4, "y": 4}]}})
        self._assert_priorities()

    def test_food_in_range_and_out_of_range(self):
        # verifies that only adjacent food increases priority
        self._call({"x": 2, "y": 2}, {"board": {"food": [{"x": 4, "y": 4}, {"x": 2, "y": 3}]}})
        self._assert_priorities(up=1)

if __name__ == "__main__":

    unittest.main()



