
import unittest
from unittest.mock import patch
from move import Move

class TestNotWallCollision(unittest.TestCase):

    def test_not_left(self):

        game_state = {"you": {"id": "my", "head": {"x": 0, "y": 2} ,"body": [{"x": 0, "y": 2}, {"x": 0, "y": 3}, {"x": 0, "y": 4}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        
        with patch.object(Move, "not_backward", return_value="Mocked") as not_backward:

            with patch.object(Move, "not_itself_collision", return_value="Mocked") as not_itself:

                with patch.object(Move, "not_enemy_collision", return_value="Mocked") as not_enemy:
                    
                    bot = Move()

                    bot.choose_move(game_state)
                    
                    not_backward.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()
                    
                    is_safe = bot.is_move_safe["left"]["is_safe"]
                    
                    self.assertFalse(is_safe)

    def test_not_up(self):

        game_state = {"you": {"id": "my", "head": {"x": 2, "y": 10} ,"body": [{"x": 2, "y": 10}, {"x": 2, "y": 9}, {"x": 2, "y": 8}],"length": 3}, 
                      "board": {"height": 11, "width": 11, "snakes": [], "food": [{"x": 10, "y": 10}]},
                      "turn": 1}
        
        with patch.object(Move, "not_backward", return_value="Mocked") as not_backward:

            with patch.object(Move, "not_itself_collision", return_value="Mocked") as not_itself:

                with patch.object(Move, "not_enemy_collision", return_value="Mocked") as not_enemy:

                    bot = Move()

                    bot.choose_move(game_state)
                    
                    not_backward.assert_called_once()

                    not_itself.assert_called_once()

                    not_enemy.assert_called_once()
                    
                    is_safe = bot.is_move_safe["up"]["is_safe"]

                    self.assertFalse(is_safe)

if __name__ == "__main__":

    unittest.main()

                                        