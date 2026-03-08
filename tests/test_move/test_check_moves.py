
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestCheckMoves(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.is_move_safe = {}
        self.head = {}
        self.game_state = {}
        self.body = []
        self.neck = {}
        self.my_length = 0
        
        self.patchers = [
            patch.object(self.bot, "calculate_opponents_positions", name="mock_calculate_opponents_positions"),
            patch.object(self.bot, "not_backward", name="mock_not_backward"),
            patch.object(self.bot, "not_wall_collision", name="mock_not_wall_collision"),
            patch.object(self.bot, "not_itself_collision", name="mock_not_itself_collision"),
            patch.object(self.bot, "not_enemy_collision", name="mock_not_enemy_collision"),
            patch.object(self.bot, "calculate_food", name="mock_calculate_food")
        ]
        self.mocks = {}

        self.addCleanup(self.stop_patchers)

    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock 

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def assert_calls_calculate_opponents_positions(self, game_state, my_length):

        for name, mock in self.mocks.items():
            if name == "mock_calculate_opponents_positions":
                mock.assert_called_with(game_state=game_state, my_length=my_length)
            else:
                continue
    
    def assert_calls_check_moves(self, is_move_safe, head, game_state, body, neck):

        for name, mock in self.mocks.items():

            if name == "mock_calculate_opponents_positions":
                continue
            mock.assert_called_with(is_move_safe, head=head, game_state=game_state, body=body, neck=neck)
    
    def test_correct_check_moves(self):

        self.start_patchers()

        self.bot.check_moves(self.is_move_safe, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

        self.assert_calls_calculate_opponents_positions(self.game_state, self.my_length)
        self.assert_calls_check_moves(self.is_move_safe, self.head, self.game_state, self.body, self.neck)

    @patch.object(bot, "calculate_opponents_positions", side_effect=RuntimeError("side effect"))
    def test_fallback_calculate_opponents_position(self, mock_calculate_oppoenets_positions):

        with self.assertRaises(RuntimeError):
            self.bot.check_moves(self.is_move_safe, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

        mock_calculate_oppoenets_positions.assert_called_with(game_state=self.game_state, my_length=self.my_length)

    @patch.object(bot, "calculate_opponents_positions")
    @patch.object(bot, "not_backward", side_effect=RuntimeError("side effect"))
    def test_fallback_checks(self, mock_not_backward, mock_calculate_opponents_positions):

        with self.assertRaises(RuntimeError):
            self.bot.check_moves(self.is_move_safe, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

        mock_calculate_opponents_positions.assert_called_with(game_state=self.game_state, my_length=self.my_length)
        mock_not_backward.assert_called_with(self.is_move_safe, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck)


if __name__ == "__main__":
    unittest.main()