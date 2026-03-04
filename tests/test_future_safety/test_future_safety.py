
import unittest
from unittest.mock import patch , MagicMock

from future_safety import FutureSafety

class TestFutureSafety(unittest.TestCase):

    def setUp(self):

        self.patchers = [
            patch.object(FutureSafety, "log_data")
        ]
        self.mocks = {}

        self.start_patchers()
        self.addCleanup(self.stop_patchers)
        
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