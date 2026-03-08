
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestCheckMoves(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        
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
                try:
                    self.mocks [mock.name] = mock
                except AttributeError:
                    self.mocks [mock._mock_name] = mock 

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def check_calls_calculate_opponents_positions(self, game_state, my_length):

        for name, mock in self.mocks.items():
            if name == "mock_calculate_opponents_positions":
                mock.assert_called_with(game_state=game_state, my_length=my_length)
            else:
                continue
    
    def check_calls_checks(self, is_move_safe, head, game_state, body, neck):

        for name, mock in self.mocks.items():

            if name == "mock_calculate_opponents_positions":
                continue
            mock.assert_called_with(is_move_safe, head=head, game_state=game_state, body=body, neck=neck)
    
    def test_correct_check_moves(self):

        pass

    def fallback_calculate_opponents_position(self):

        pass

    def fallback_checks(self):

        pass

if __name__ == "__main__":
    unittest.main()