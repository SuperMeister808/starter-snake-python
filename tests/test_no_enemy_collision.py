
import unittest
from unittest.mock import patch
from move import Move

class TestNoEnemyCollision(unittest.TestCase):

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
        
                    
        


                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertEqual(self.bot.is_move_safe["left"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(self.bot.is_move_safe, "left"))

    def test_priority_right(self):

                    game_state = {"you": {"id": "my", "head": {"x": 0, "y": 2} ,"body": [{"x": 0, "y": 2}, {"x": 0, "y": 3}, {"x": 0, "y": 4}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        

        


                    self.bot.choose_move(game_state)
                    
                    self.check_calls()
                    
                    self.assertEqual(self.bot.is_move_safe["right"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(self.bot.is_move_safe, "right"))
    
    def test_priority_up(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}, {"x": 3, "y": 2}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 1, "y": 4}, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        


                   
                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()

                    self.assertEqual(self.bot.is_move_safe["up"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(self.bot.is_move_safe, "up"))

    def test_priority_down(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 4} ,"body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 1, "y": 2}, "body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        


                  
                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()

                    self.assertEqual(self.bot.is_move_safe["down"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(self.bot.is_move_safe, "down"))

    def test_multiple_snakes(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}, {"x": 3, "y": 2}],"length": 3}, 
                      "board": {"snakes": [{"id": "not_important", "head": {"x": 8, "y": 8}, "body": [{"x": 8, "y": 8}, {"x": 9, "y": 8}], "length": 2}, {"id": "opponent", "head": {"x": 1, "y": 4}, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        


                  
                    
                    self.bot.choose_move(game_state)

                    self.check_calls()

                    self.assertEqual(self.bot.is_move_safe["up"]["priority"], 1)

                    self.assertTrue(self.check_none_priority(self.bot.is_move_safe, "up"))

    def test_no_priority(self):

                    game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 2, "y": 2}, {"x": 3, "y": 2}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 8, "y": 8}, "body": [{"x": 8, "y": 8}, {"x": 9, "y": 8}], "length": 2}], "food": [{"x": 10, "y": 10}]},
                      "turn": 1
                      }
        


                   
                    
                    self.bot.choose_move(game_state)
                    
                    self.check_calls()

                    self.assertTrue(self.check_none_priority(self.bot.is_move_safe, "None"))

    def test_unsafe_moves(self):
            
            game_state = {"you": {"id": "my", "head": {"x": 1, "y": 2} ,"body": [{"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": 1, "y": 4}],"length": 3}, 
                      "board": {"snakes": [{"id": "opponent", "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 3, "y": 2}], "length": 2}], "food": []},
                      "turn": 1
                      }
            
            self.bot.choose_move(self.bot)
            
            self.assertFalse(self)
    
if __name__ == "__main__":

    unittest.main()