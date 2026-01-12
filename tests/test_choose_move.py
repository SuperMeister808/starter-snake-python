
import unittest

from unittest.mock import patch

from move import Move

class TestChooseMove(unittest.TestCase):

    def test_priority_left(self):

        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
  
                game_state = "Not_important"

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = bot.choose_move(game_state)

                    expected = ["left"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_right(self):

        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
  
                game_state = "Not_important"

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = bot.choose_move(game_state)

                    expected = ["right"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_up(self):

        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
  
                game_state = "Not_important"

                bot = Move()
                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                          
                    result = bot.choose_move(game_state)

                    expected = ["up"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_down(self):

        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
  
                game_state = "Not_important"

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                                
                    result = bot.choose_move(game_state)

                    expected = ["down"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_right_and_left(self):

       with patch.object(Move, "reset_is_move_safe") as reset, \
            patch.object(Move, "not_backward") as not_backward, \
            patch.object(Move, "not_wall_collision") as not_wall, \
            patch.object(Move, "not_itself_collision") as not_itself, \
            patch.object(Move, "not_enemy_collision") as not_enemy:
  
                game_state = "Not_important"

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:
                                
                    result = bot.choose_move(game_state)

                    expected = ["left", "right"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_up_and_down(self):
           
        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
      
                game_state = "Not_important"

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:

                    result = bot.choose_move(game_state)

                    expected = ["up", "down"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_unsafe_move(self):
         
        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
               
                game_state = "Not important"

                bot = Move()

                with patch.object(bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as is_move_safe:

                    result = bot.choose_move(game_state)

                    expected = ["up", "down", "right"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_priority_and_unsafe(self):

        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
               
                game_state = "Not important"

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as is_move_safe:
                
                    result = bot.choose_move(game_state)

                    expected = ["down"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

    def test_ever_move_unsafe(self):
                            
        with patch.object(Move, "reset_is_move_safe") as reset, \
             patch.object(Move, "not_backward") as not_backward, \
             patch.object(Move, "not_wall_collision") as not_wall, \
             patch.object(Move, "not_itself_collision") as not_itself, \
             patch.object(Move, "not_enemy_collision") as not_enemy:
  
                game_state = {"turn": 1}

                bot = Move()
                                
                with patch.object(bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": False, "priority": 0}}) as is_move_safe:
                                
                    result = bot.choose_move(game_state)

                    expected = ["down"]
                            
                    reset.assert_called_once()

                    not_backward.assert_called_once()
                                
                    not_wall.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()

                    reset.assert_called_once()
                            
                    self.assertIn(result["move"], expected)

if __name__ == "__main__":

    unittest.main()

