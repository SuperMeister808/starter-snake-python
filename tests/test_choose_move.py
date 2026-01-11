
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

                            expected = ["left"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_priority_right(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["right"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_priority_up(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["up"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_priority_down(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 2}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["down"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_priority_right_and_left(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["left", "right"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_priority_up_and_down(self):

        game_state = "Not_important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": True, "priority": 1}, "right": {"is_safe": True, "priority": 1}, "up": {"is_safe": True, "priority": 2}, "down": {"is_safe": True, "priority": 2}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["up", "down"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_unsafe_move(self):

        game_state = "Not important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["up", "down", "right"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_priority_and_unsafe(self):

        game_state = "Not important"

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 1}, "down": {"is_safe": True, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            result = bot.choose_move(game_state)

                            expected = ["up"]

                            patch_1.assert_called_once()

                            patch_2.assert_called_once()

                            patch_3.assert_called_once()

                            patch_4.assert_called_once()
                            
                            self.assertIn(result["move"], expected)

    def test_ever_move_unsafe(self):

        game_state = {"turn": 1}

        bot = Move()
                        
        with patch.object(bot, "is_move_safe", {"left": {"is_safe": False, "priority": 0}, "right": {"is_safe": False, "priority": 0}, "up": {"is_safe": False, "priority": 0}, "down": {"is_safe": False, "priority": 0}}) as patch_5:
                            
            with patch.object(Move, "not_wall_collision", return_value = "patch not_wall_collision") as patch_1:

                with patch.object(Move, "not_backward", return_value = "patch not_itself_collision") as patch_2:

                    with patch.object(Move, "not_enemy_collision", return_value = "Patch not_enemy_collision") as patch_3:

                        with patch.object(Move, "not_itself_collision", return_value="Patch not_itself_collision") as patch_4:
                                
                            #no return_value because return is None
                            with patch("builtins.print") as patch_6:
                            
                                result = bot.choose_move(game_state)

                                expected = ["down"]

                                patch_1.assert_called_once()

                                patch_2.assert_called_once()

                                patch_3.assert_called_once()

                                patch_4.assert_called_once()

                                patch_6.assert_called_once()
                            
                                self.assertIn(result["move"], expected)

if __name__ == "__main__":

    unittest.main()

