
import unittest

from unittest.mock import patch

from move import Move

class TestChooseMove(unittest.TestCase):

    def test_priority_left(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = {"move": "left"}

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertEqual(result, expected)

    def test_priority_right(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = {"move": "left"}

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertEqual(result, expected)

if __name__ == "__main__":

    unittest.main()

