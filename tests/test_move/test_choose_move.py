
import unittest

from unittest.mock import patch

from move import Move

class TestChooseMove(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.game_state = {"you": {"head": {}, "body": {}}}
        
        self.patchers = [
             patch.object(self.bot, "reset_is_move_safe"),
             patch.object(self.bot, "not_enemy_collision"),
             patch.object(self.bot, "not_backward"),
             patch.object(self.bot, "not_itself_collision"),
             patch.object(self.bot, "not_wall_collision"),
             patch.object(self.bot, "calculate_food"),
             patch.object(self.bot, "call_future_safety"),
             patch.object(self.bot, "get_neck", return_value={})      
        ]

        self.mocks = {}

        for i, patcher in enumerate(self.patchers):
             
            mock = patcher.start()
            self.mocks[i] = mock

        self.addCleanup(self.stop_patches)

    def stop_patches(self):
         
        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self, exclude_call_future_safety=False):
         
        for name, mock in self.mocks.items():
             
            if exclude_call_future_safety == True:
                if name == 6:
                    mock.assert_not_called()
                else:
                    mock.assert_called()    
            else:
                mock.assert_called()
    
    def test_priority_left(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["left"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_right(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_up(self):
       
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                          
                    result = self.bot.choose_move(self.game_state)

                    expected = ["up"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_down(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_right_and_left(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["left", "right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_up_and_down(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:

                    result = self.bot.choose_move(self.game_state)

                    expected = ["up", "down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_unsafe_move(self):



                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:

                    result = self.bot.choose_move(self.game_state)

                    expected = ["up", "down", "right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_and_unsafe(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_every_move_unsafe(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": False, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["down"]
                            
                    self.check_calls(exclude_call_future_safety=True)
                            
                    self.assertIn(result["move"], expected)

    def test_multiple_priorities(self):


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 2}, "up": {"is_safe": True, "priority": 1}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                                
                    result = self.bot.choose_move(self.game_state)

                    expected = ["down", "right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_unsafe_with_priority(self):


                                
        with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": False, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 1}}) as is_move_safe:
                                
                result = self.bot.choose_move(self.game_state)

                expected = ["down"]
                            
                self.check_calls()
                            
                self.assertIn(result["move"], expected)


if __name__ == "__main__":

    unittest.main()

