
import unittest
from unittest.mock import patch , MagicMock

from future_safety import FutureSafety
from move import Move

class TestCallFutureSafety(unittest.TestCase):
    
    def setUp(self):
        
        self.move = Move()
        self.future_safety = FutureSafety(self.move)

        self.patchers = [
            patch.object(self.future_safety, "log_data")
        ]
        self.mocks = {}
    
    def setup_patchers(self, extract_keywords_move):

        patcher_extract_keywords = self.create_patcher_extract_keywords(extract_keywords_move)
        self.patchers.append(patcher_extract_keywords)
    
    def create_patcher_extract_keywords(self, move):

        patcher = patch.object(self.future_safety.keywords, "extract_keywords", return_value=("game_state", "body", move, "head", "my_length", "neck"))
        return patcher
    
    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):
            mock = patcher.start()
            try:
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    self.mocks [i] = mock
                else:
                    raise

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def check_calls(self):
        
        for name , mock in self.mocks.items():

            try:
                mock.assert_called_once()
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    pass
                else:
                    raise
    
    def test_2_calls_move_up(self):

        pass

    def test_2_call_move_left(self):

        pass

    def test_1_call_move_up(self):

        pass

    def test_1_call_move_left(self):

        pass

