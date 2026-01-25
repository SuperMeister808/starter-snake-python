
import unittest
from unittest.mock import patch
from move import Move

class TestNotBackward(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        
        self.patchers = [
               patch.object(self.bot, "reset_is_move_safe"),
               patch.object(self.bot, "not_enemy_collision"),
               patch.object(self.bot, "not_wall_collision"),
               patch.object(self.bot, "not_itself_collision"),
               patch.object(self.bot, "calculate_food"),
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
        

                        self.bot.choose_move(game_state)
        
                        self.check_calls()
                    
                        self.assertFalse(self.bot.is_move_safe["down"]["is_safe"])

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "down"))

    def test_not_left(self):

                        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 1, "y": 2}, {"x": 0, "y": 2}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }

                        self.bot.choose_move(game_state)

                        self.check_calls()
                    
                        self.assertFalse(self.bot.is_move_safe["left"]["is_safe"])

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "left"))

    def test_not_right(self):

                        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 4, "y": 2}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        


                        self.bot.choose_move(game_state)
        
                        self.check_calls()
                    
                        self.assertFalse(self.bot.is_move_safe["right"]["is_safe"])

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "right"))

    def test_not_up(self):

                        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 2} ,"body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],"length": 3}, 
                      "board": {"snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        

        


                        self.bot.choose_move(game_state)
        
                        self.check_calls()
                    
                        self.assertFalse(self.bot.is_move_safe["up"]["is_safe"])

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "up"))

if __name__ == "__main__":

    unittest.main()