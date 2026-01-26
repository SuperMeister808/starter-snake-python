
import unittest
from unittest.mock import patch

from move import Move

class TestCalculateFood(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.patchers = [
             patch.object(self.bot, "reset_is_move_safe"),
             patch.object(self.bot, "not_backward"),
             patch.object(self.bot, "not_itself_collision"),
             patch.object(self.bot, "not_wall_collision")    
        ]

        self.mocks = {}

        for patcher in self.patchers:
             
            mock = patcher.start()
            self.mocks[mock._mock_name] = mock

        self.addCleanup(self.stop_patches)

    def stop_patches(self):
         
        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):
         
        for name, mock in self.mocks.items():
             
            mock.assert_called_once()

    
    def test_safe_food(self):

        game_state = {
            "you": {"head": {"x": 2, "y": 2}},
            "board": {"food": [{"x": 3, "y": 2}], "snakes": []}
        }

        self.bot.choose_move(game_state)

        self.assertEqual(self.bot.is_move_safe["right"]["priority"], 1)

        for move, data in self.bot.is_move_safe.items():
            
            self.assertTrue(data["is_safe"])

    def test_unsafe_food(self):

        game_state = {
            "you": {"head": {"x": 2, "y": 2}, "id": "you", "length": 1, "body": [{"x": 2, "y": 2}]},
            "board": {"food": [{"x": 3, "y": 2}], "snakes": [{"id": "opponent", "head": {"x": 3, "y": 1}, "body": [{"x": 3, "y": 1}, {"x": 4, "y":1}], "length": 2}]}
        }

        self.bot.choose_move(game_state)

        self.assertFalse(self.bot.is_move_safe["right"]["is_safe"])
        #snake area + food area
        self.assertEqual(self.bot.is_move_safe["right"]["priority"], 2)

        for move, data in self.bot.is_move_safe.items():

            if move != "right" and move != "down":
            
                self.assertTrue(data["is_safe"])

    def test_multiple_food_items(self):

        game_state = {
            "you": {"head": {"x": 2, "y": 2}, "id": "you", "length": 1, "body": [{"x": 2, "y": 2}]},
            "board": {"food": [{"x": 3, "y": 2}, {"x": 1, "y": 2}], "snakes": [{"id": "opponent", "head": {"x": 3, "y": 1}, "body": [{"x": 3, "y": 1}, {"x": 4, "y":1}], "length": 2}]}
        }

        self.bot.choose_move(game_state)

        self.assertEqual(self.bot.is_move_safe["left"]["priority"], 1)
        self.assertEqual(self.bot.is_move_safe["right"]["priority"], 1)

        self.assertFalse(self.bot.is_move_safe["right"]["is_safe"])
        for move, data in self.bot.is_move_safe.items():

            if move != "right" and move != "down":

                self.assertTrue(data["is_safe"])

if __name__ == "__main__":

    unittest.main()



