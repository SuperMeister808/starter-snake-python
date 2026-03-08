
import unittest
from unittest.mock import patch

from move import Move

class TestCalculateFood(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        self.is_move_safe = {"left": {"priority": 0}, "right": {"priority": 0}, "up": {"priority": 0}, "down": {"priority": 0}}
    
    def test_food_move_left(self):

        game_state = {"board": {"food": [{"x": 2, "y": 2}]}}
        head = {"x": 3, "y": 2}

        self.bot.calculate_food(self.is_move_safe, head=head, game_state=game_state)

        self.assertEqual(self.is_move_safe["left"]["priority"], 1)
        self.assertEqual(self.is_move_safe["right"]["priority"], 0)
        self.assertEqual(self.is_move_safe["up"]["priority"], 0)
        self.assertEqual(self.is_move_safe["down"]["priority"], 0)

    def test_food_move_right(self):

        game_state = {"board": {"food": [{"x": 2, "y": 2}]}}
        head = {"x": 1, "y": 2}

        self.bot.calculate_food(self.is_move_safe, head=head, game_state=game_state)

        self.assertEqual(self.is_move_safe["left"]["priority"], 0)
        self.assertEqual(self.is_move_safe["right"]["priority"], 1)
        self.assertEqual(self.is_move_safe["up"]["priority"], 0)
        self.assertEqual(self.is_move_safe["down"]["priority"], 0)

    def test_food_move_up(self):

        pass

    def test_food_move_down(self):

        pass

    def test_food_on_multiple_moves(self):

        pass

    def test_food_out_of_range(self):

        pass

    def test_food_in_range_and_food_out_of_range(self):

        pass

if __name__ == "__main__":

    unittest.main()



