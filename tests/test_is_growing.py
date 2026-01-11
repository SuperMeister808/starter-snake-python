
import unittest

from unittest.mock import patch

from move import Move

class TestIsGrowing(unittest.TestCase):

    def check_safe_move(self, is_move_safe, excluded_move):

        for move , data in is_move_safe.items():

            if move != excluded_move:

                if data["is_safe"] == False:

                    return False
                
        return True
    
    def test_is_growing(self):

        game_state = {"you": {"id": "my", "head": {"x": 1, "y": 1} ,"body": [{"x": 1, "y": 1}, {"x": 1, "y": 2}, {"x": 1, "y": 3}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 3, "y": 1}, "body": [{"x": 3, "y": 1}, {"x": 2, "y": 1}], "length": 2}], "food": [{"x": 4, "y": 1}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_backward", return_value = "Patch not_backward") as patch_1:

            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_2:

                with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_3:

                    bot = Move()
                    
                    bot.choose_move(game_state)
                    
                    patch_1.assert_called_once()
                    patch_2.assert_called_once()
                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["right"]["is_safe"])

                    self.assertTrue(self.check_safe_move(bot.is_move_safe, "right"))

    def test_is_not_growing(self):

        game_state = {"you": {"id": "my", "head": {"x": 1, "y": 1} ,"body": [{"x": 1, "y": 1}, {"x": 1, "y": 2}, {"x": 1, "y": 3}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 3, "y": 1}, "body": [{"x": 3, "y": 1}, {"x": 2, "y": 1}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_backward", return_value = "Patch not_backward") as patch_1:

            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_2:

                with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_3:

                    bot = Move()
                    
                    bot.choose_move(game_state)
                    
                    patch_1.assert_called_once()
                    patch_2.assert_called_once()
                    patch_3.assert_called_once()
                    
                    self.assertTrue(self.check_safe_move(bot.is_move_safe, "None"))

if __name__ == "__main__":

    unittest.main()
