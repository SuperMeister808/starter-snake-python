
import unittest
from unittest.mock import patch
from move import Move

class TestNoEnemyCollision(unittest.TestCase):

    def check_none_priority(self, is_move_safe, excluded_move):

        for move , data in is_move_safe.items():

            if move != excluded_move:

                if data["priority"] == 1:

                    return False
                
        return True
    
    def test_priority_left(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 0, "y": 2}, "body": [{"x": 0, "y": 2}, {"x": 0, "y": 3}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        bot = Move()
        
        with patch.object(Move, "not_backward", return_value = "Patch not_backward") as patch_1:

            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_2:

                with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_3:

                    bot.choose_move(game_state)
                    
                    patch_1.assert_called_once()
                    patch_2.assert_called_once()
                    patch_3.assert_called_once()
                    
                    self.assertEqual(bot.is_move_safe["left"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(bot.is_move_safe, "left"))

    def test_priority_right(self):

        game_state = {"you": {"id": "my", "head": {"x": 0, "y": 2} ,"body": [{"x": 0, "y": 2}, {"x": 0, "y": 3}, {"x": 0, "y": 4}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        bot = Move()
        
        with patch.object(Move, "not_backward", return_value = "Patch not_backward") as patch_1:

            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_2:

                with patch.object(Move, "not_itself_collision", return_value = "patch not_itself_collision") as patch_3:

                    bot.choose_move(game_state)
                    
                    patch_1.assert_called_once()
                    patch_2.assert_called_once()
                    patch_3.assert_called_once()
                    
                    self.assertEqual(bot.is_move_safe["right"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(bot.is_move_safe, "right"))
    
    def test_priority_up(self):

        game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}, {"x": 3, "y": 2}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 1, "y": 4}, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}], "length": 2}], "food": [{"x": 10, "y": 10}]},
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

                    self.assertEqual(bot.is_move_safe["up"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(bot.is_move_safe, "up"))

    def test_priority_down(self):

        game_state = {"you": {"id": "my", "head": {"x": 1, "y": 4} ,"body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 1, "y": 2}, "body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}], "length": 2}], "food": [{"x": 10, "y": 10}]},
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

                    self.assertEqual(bot.is_move_safe["down"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(bot.is_move_safe, "down"))

    def test_multiple_snakes(self):

        game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}, {"x": 3, "y": 2}],"length": 3}, 
                      "board": {"snakes": [{"id": "not_important", "head": {"x": 8, "y": 8}, "body": [{"x": 8, "y": 8}, {"x": 9, "y": 8}], "length": 2}, {"id": "opponent", "head": {"x": 1, "y": 4}, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}], "length": 2}], "food": [{"x": 10, "y": 10}]},
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

                    self.assertEqual(bot.is_move_safe["up"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(bot.is_move_safe, "up"))

    def test_no_priority(self):

        game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}, {"x": 3, "y": 2}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 8, "y": 8}, "body": [{"x": 8, "y": 8}, {"x": 9, "y": 8}], "length": 2}], "food": [{"x": 10, "y": 10}]},
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

                    self.assertTrue(self.check_none_priority(bot.is_move_safe, "None"))
    
if __name__ == "__main__":

    unittest.main()