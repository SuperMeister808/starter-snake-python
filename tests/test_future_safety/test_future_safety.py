
import unittest
from unittest.mock import patch , MagicMock

from future_safety import FutureSafety
from move import Move

class TestFutureSafety(unittest.TestCase):

    def setUp(self):

        self.patchers = []
        self.mocks = {}

        self.addCleanup(self.stop_patchers)
        
    def setup_patchers(self, new_opponents_positions):

        patcher_opponents_positions = self.create_patcher_opponents_positions(new_opponents_positions)
        self.patchers.append(patcher_opponents_positions)

        self.start_patchers()
    
    def create_patcher_opponents_positions(self, new):

        patcher = patch.object(Move, "opponents_positions", new=new)
        return patcher
    
    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):
            mock = patcher.start()
            try:
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                self.mocks [i] = mock

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            if isinstance(mock, MagicMock):
                mock.assert_called()
    
    def test_safe_move_left(self):

        pass

    def test_no_safe_move_at_second_level(self):

        pass

    def test_no_safe_move_left(self):

        pass