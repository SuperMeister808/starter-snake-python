
import unittest
from unittest.mock import patch
from move import Move

class TestNoEnemyCollision(unittest.TestCase):

    def test_priority_left(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],"length": 3}, 
                      "board": {"snakes": {"id": "opponent", "head": {"x": 1, "y": 2}, "body": [{"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": 1, "y": 4}]}}
                      }
        
        bot = Move()
        
        with patch("move.not_backward", return_value = "Patch not_backward") as patch_1:

            with patch("move.not_wall_collision", return_value = "patch not_wall_collision") as patch2:

                with patch("move.not_itself_collision", return_value = "patch not_itself_collision") as patch3:

                    self.assert_any_call(patch_1)
                    self.assert_any_call(patch2)
                    self.assert_any_call(patch3)
                    
                    result = bot.choose_move(game_state)

                    expectation = {"move": "left"}

                    self.assertEqual(result, expectation)