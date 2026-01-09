
import unittest
from unittest.mock import patch
from move import Move

class TestNoEnemyCollision(unittest.TestCase):

    def test_priority_left(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],"length": 3}, 
                      "board": {"snakes": {"id": "opponent", "head": {"x": 1, "y": 2}, "body": [{"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": 1, "y": 4}]}}
                      }
        
        bot = Move()
        
        with patch.object(Move, "not_backward", return_value = "Patch not_backward") as patch_1:

            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_2:

                with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_3:

                    result = bot.choose_move(game_state)
                    
                    patch_1.assert_called_once()
                    patch_2.assert_called_once()
                    patch_3.assert_called_once()

                    expectation = {"move": "left"}

                    self.assertEqual(result, expectation)

if __name__ == "__main__":

    unittest.main()