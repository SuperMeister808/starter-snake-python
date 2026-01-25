
import unittest
from unittest.mock import patch
from move import Move

class TestNotWallCollision(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        
        self.patchers = [
               patch.object(self.bot, "reset_is_move_safe"),
               patch.object(self.bot, "not_enemy_collision"),
               patch.object(self.bot, "not_itself_collision"),
               patch.object(self.bot, "calculate_food"),
               patch.object(self.bot, "not_backward")
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
    
    def test_not_left(self):

                        game_state = {"you": {"id": "my", "head": {"x": 0, "y": 2} ,"body": [{"x": 0, "y": 2}, {"x": 0, "y": 3}, {"x": 0, "y": 4}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        

                    


                        self.bot.choose_move(game_state)
                    
                        self.check_calls()
                    
                        is_safe_left = self.bot.is_move_safe["left"]["is_safe"]
                    
                        self.assertFalse(is_safe_left)

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "left"))

    def test_not_right(self):

                        game_state = {"you": {"id": "my", "head": {"x": 10, "y": 2} ,"body": [{"x": 10, "y": 2}, {"x": 10, "y": 3}, {"x": 10, "y": 4}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        

                    


                        self.bot.choose_move(game_state)
                    
                        self.check_calls()
                    
                        is_safe_right = self.bot.is_move_safe["right"]["is_safe"]
                    
                        self.assertFalse(is_safe_right)

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "right"))
    
    def test_not_up(self):

                        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 10} ,"body": [{"x": 2, "y": 10}, {"x": 2, "y": 9}, {"x": 2, "y": 8}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        



                        self.bot.choose_move(game_state)
                    
                        self.check_calls()
                    
                        is_safe_up = self.bot.is_move_safe["up"]["is_safe"]

                        self.assertFalse(is_safe_up)

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "up"))

    def test_not_down(self):

                        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 0} ,"body": [{"x": 2, "y": 0}, {"x": 3, "y": 0}, {"x": 4, "y": 0}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        



                        self.bot.choose_move(game_state)

                        self.check_calls()
                    
                        is_safe_down = self.bot.is_move_safe["down"]["is_safe"]

                        self.assertFalse(is_safe_down)

                        self.assertTrue(self.check_safe_moves(self.bot.is_move_safe, "down"))
    
    def test_not_up_and_right(self):

                        game_state = {"you": {"id": "my", "head": {"x": 10, "y": 10} ,"body": [{"x": 10, "y": 10}, {"x": 9, "y": 10}, {"x": 8, "y": 10}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        




                        self.bot.choose_move(game_state)
                    
                        self.check_calls()
                    
                        is_safe_up = self.bot.is_move_safe["up"]["is_safe"]

                        is_safe_right = self.bot.is_move_safe["right"]["is_safe"]

                        self.assertFalse(is_safe_up)

                        self.assertFalse(is_safe_right)

                        self.assertTrue(self.bot.is_move_safe["down"]["is_safe"])

                        self.assertTrue(self.bot.is_move_safe["left"]["is_safe"])

    def test_not_down_and_left(self):

                        game_state = {"you": {"id": "my", "head": {"x": 0, "y": 0} ,"body": [{"x": 1, "y": 0}, {"x": 2, "y": 0}, {"x": 3, "y": 0}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        




                        self.bot.choose_move(game_state)
                    
                        self.check_calls()
                    
                        is_safe_down = self.bot.is_move_safe["down"]["is_safe"]

                        is_safe_left = self.bot.is_move_safe["left"]["is_safe"]

                        self.assertFalse(is_safe_down)

                        self.assertFalse(is_safe_left)

                        self.assertTrue(self.bot.is_move_safe["up"]["is_safe"])

                        self.assertTrue(self.bot.is_move_safe["right"]["is_safe"])

if __name__ == "__main__":

    unittest.main()                                        