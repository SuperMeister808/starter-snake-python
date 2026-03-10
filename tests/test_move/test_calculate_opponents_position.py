
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestCalculateOpponentsPositions(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.mocks = {}
        self.patchers = [
            patch.object(self.bot.future_safety, "log_data", name="mock_log_data"),
            patch.object(self.bot, "reset_opponents_positions", name="mock_reset_opponents_positions")
        ]

        self.start_patchers()
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()
    
    def general_call_assertion(self):

        for name , mock in self.mocks.items():
            if isinstance(mock, MagicMock):
                mock.assert_called()
    
    def test_extract_positions_one_snake(self):

        pass

    def test_extract_positions_one_snake_is_growing(self):

        pass

    def test_extract_positions_multiple_snakes(self):

        pass

    def test_extract_positions_no_snakes(self):

        pass

    def test_missing_body_parts_between_head_and_tail(self):

        pass

    def test_snake_has_wrong_type(self):

        pass
    
    #Edge-Case
    def test_only_head(self):

        pass