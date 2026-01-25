
import unittest

from unittest.mock import patch

from move import Move

class TestChooseMove(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.patchers = [
             patch.object(self.bot, "reset_is_move_safe"),
             patch.object(self.bot, "not_enemy_collision"),
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
    
    def test_priority_left(self):

  
                game_state = "Not_important"


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(game_state)

                    expected = ["left"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_right(self):


  
                game_state = "Not_important"


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(game_state)

                    expected = ["right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_up(self):


  
                game_state = "Not_important"


                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                          
                    result = self.bot.choose_move(game_state)

                    expected = ["up"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_down(self):


  
                game_state = "Not_important"


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                                
                    result = self.bot.choose_move(game_state)

                    expected = ["down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_right_and_left(self):


  
                game_state = "Not_important"


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(game_state)

                    expected = ["left", "right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_up_and_down(self):
           

      
                game_state = "Not_important"


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:

                    result = self.bot.choose_move(game_state)

                    expected = ["up", "down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_unsafe_move(self):
         

               
                game_state = "Not important"



                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:

                    result = self.bot.choose_move(game_state)

                    expected = ["up", "down", "right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_and_unsafe(self):


               
                game_state = "Not important"


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                
                    result = self.bot.choose_move(game_state)

                    expected = ["down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_ever_move_unsafe(self):
                            

  
                game_state = {"turn": 1}


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": False, "priority": 0}}) as is_move_safe:
                                
                    result = self.bot.choose_move(game_state)

                    expected = ["down"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

    def test_multiple_priorities(self):
         

  
                game_state = {"turn": 1}


                                
                with patch.object(self.bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 2}, "up": {"is_safe": True, "priority": 1}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                                
                    result = self.bot.choose_move(game_state)

                    expected = ["down", "right"]
                            
                    self.check_calls()
                            
                    self.assertIn(result["move"], expected)

if __name__ == "__main__":

    unittest.main()

