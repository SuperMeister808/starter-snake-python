
import unittest

from unittest.mock import patch

from move import Move

class TestIsGrowing(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.patchers = [
             patch.object(self.bot, "reset_is_move_safe"),
             patch.object(self.bot, "not_backward"),
             patch.object(self.bot, "not_itself_collision"),
             patch.object(self.bot, "not_wall_collision"),
             patch.object(self.bot, "calculate_food")      
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
    
    def check_safe_move(self, is_move_safe, excluded_move):

        for move , data in is_move_safe.items():

            if move != excluded_move:

                if data["is_safe"] == False:

                    return False
                
        return True
    
    def test_is_growing_right(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 1} ,"body": [{"x": 1, "y": 1}, {"x": 1, "y": 2}, {"x": 1, "y": 3}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 3, "y": 1}, "body": [{"x": 3, "y": 1}, {"x": 2, "y": 1}], "length": 2}], "food": [{"x": 4, "y": 1}]},
                      "turn": 1
                      }
        


                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertFalse(self.bot.is_move_safe["right"]["is_safe"])

                    self.assertTrue(self.check_safe_move(self.bot.is_move_safe, "right"))

    def test_is_growing_left(self):

                    game_state = {"you": {"id": "my", "head": {"x": 8, "y": 1} ,"body": [{"x": 8, "y": 1}, {"x": 8, "y": 2}, {"x": 8, "y": 3}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 6, "y": 1}, "body": [{"x": 6, "y": 1}, {"x": 7, "y": 1}], "length": 2}], "food": [{"x": 5, "y": 1}]},
                      "turn": 1
                      }
        


         
                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertFalse(self.bot.is_move_safe["left"]["is_safe"])

                    self.assertTrue(self.check_safe_move(self.bot.is_move_safe, "left"))

    def test_is_growing_up(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 1} ,"body": [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 1, "y": 3}, "body": [{"x": 1, "y": 3}, {"x": 1, "y": 2}], "length": 2}], "food": [{"x": 1, "y": 4}]},
                      "turn": 1
                      }
        



                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertFalse(self.bot.is_move_safe["up"]["is_safe"])

                    self.assertTrue(self.check_safe_move(self.bot.is_move_safe, "up"))

    def test_is_growing_down(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 3} ,"body": [{"x": 1, "y": 3}, {"x": 2, "y": 3}, {"x": 3, "y": 3}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 1, "y": 1}, "body": [{"x": 1, "y": 1}, {"x": 1, "y": 2}], "length": 2}], "food": [{"x": 1, "y": 0}]},
                      "turn": 1
                      }
        


                    
                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertFalse(self.bot.is_move_safe["down"]["is_safe"])

                    self.assertTrue(self.check_safe_move(self.bot.is_move_safe, "down"))
    
    def test_is_not_growing(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 1} ,"body": [{"x": 1, "y": 1}, {"x": 1, "y": 2}, {"x": 1, "y": 3}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 3, "y": 1}, "body": [{"x": 3, "y": 1}, {"x": 2, "y": 1}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        


        
                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertTrue(self.check_safe_move(self.bot.is_move_safe, "None"))

if __name__ == "__main__":

    unittest.main()
