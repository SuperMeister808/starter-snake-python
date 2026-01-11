
import unittest

from unittest.mock import patch

from move import Move

class TestNotItselfCollision(unittest.TestCase):

    def check_safe_moves(self, is_move_safe, excluded_move):

        for move , data in is_move_safe.items():

            if move != excluded_move:

                if data["is_safe"] == False:

                    return False
                
        return True
    
    def test_not_down(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 1}, {"x": 2, "y": 0}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["down"]["is_safe"])

                    self.assertTrue(self.check_safe_moves(bot.is_move_safe, "down"))

    def test_not_left(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 1, "y": 2}, {"x": 0, "y": 2}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["left"]["is_safe"])

                    self.assertTrue(self.check_safe_moves(bot.is_move_safe, "left"))

    def test_not_right(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 4, "y": 2}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["right"]["is_safe"])

                    self.assertTrue(self.check_safe_moves(bot.is_move_safe, "right"))

    def test_not_up(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["up"]["is_safe"])

                    self.assertTrue(self.check_safe_moves(bot.is_move_safe, "up"))

    def test_not_right_and_down(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 1}, {"x": 3, "y": 1}, {"x": 3, "y": 2}],"length": 4}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["right"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["down"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["left"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["up"]["is_safe"])

    def test_not_left_and_up(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 1, "y": 3}, {"x": 1, "y": 2}],"length": 4}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["left"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["up"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["right"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["down"]["is_safe"])

    def test_not_up_and_right_and_down(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 3}, {"x": 3, "y": 2}, {"x": 3, "y": 1}, {"x": 2, "y": 1}],"length": 6}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["right"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["up"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["down"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["left"]["is_safe"])

    def test_not_up_and_left_and_down(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 1, "y": 3}, {"x": 1, "y": 2}, {"x": 1, "y": 1}, {"x": 2, "y": 1}],"length": 6}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["left"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["up"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["down"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["right"]["is_safe"])

    def test_no_safe_move(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 1, "y": 3}, {"x": 1, "y": 2}, {"x": 1, "y": 1}, {"x": 2, "y": 1}],"length": 6}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        
        with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

            with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:
        
                    bot = Move()

                    bot.choose_move(game_state)
        
                    patch_1.assert_called_once()

                    patch_2.assert_called_once()

                    patch_3.assert_called_once()
                    
                    self.assertFalse(bot.is_move_safe["left"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["up"]["is_safe"])

                    self.assertFalse(bot.is_move_safe["down"]["is_safe"])

                    self.assertTrue(bot.is_move_safe["right"]["is_safe"])


if __name__ == "__main__":

    unittest.main()