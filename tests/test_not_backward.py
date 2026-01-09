
import unittest
from unittest.mock import patch
from move import Move

class TestNotBackward(unittest.TestCase):

    def test_not_down(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)

                    is_safe = bot.is_move_safe["up"]["is_safe"]
        
                    self.assertFalse(is_safe)

    def test_not_left(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 1, "y": 2}, {"x": 0, "y": 2}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)

                    is_safe = bot.is_move_safe["left"]["is_safe"]
        
                    self.assertFalse(is_safe)

if __name__ == "__main__":

    unittest.main()