
import unittest

from unittest.mock import patch

from move import Move

# Tests that calculate_is_growing correctly detects adjacent food.
class TestIsGrowing(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.head = {"x": 2, "y": 2}

    def _call(self, game_state):
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, game_state)) as mock:
            result = self.bot.calculate_is_growing(head=self.head, game_state=game_state)
            mock.assert_called_once()
            return result

    def test_is_growing(self):
        # verifies that True is returned when food is adjacent to the head
        game_state = {"board": {"food": [{"x": 2, "y": 3}]}}
        self.assertTrue(self._call(game_state))

    def test_is_growing_multiple_food(self):
        # verifies that True is returned when multiple food items are adjacent
        game_state = {"board": {"food": [{"x": 1, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 1}, {"x": 2, "y": 3}]}}
        self.assertTrue(self._call(game_state))

    def test_is_not_growing_no_food(self):
        # verifies that False is returned when there is no food
        game_state = {"board": {"food": []}}
        self.assertFalse(self._call(game_state))

    def test_is_not_growing_food_out_of_range(self):
        # verifies that False is returned when food is not adjacent to the head
        game_state = {"board": {"food": [{"x": 4, "y": 4}, {"x": 0, "y": 0}, {"x": 0, "y": 4}, {"x": 4, "y": 0}]}}
        self.assertFalse(self._call(game_state))

if __name__ == "__main__":

   unittest.main()
