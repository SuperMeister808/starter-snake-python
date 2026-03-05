
import unittest
from unittest.mock import patch , MagicMock

from future_safety import FutureSafety
from move import Move

class TestCallFutureSafety(unittest.TestCase):
    
    def setUp(self):
        
        self.move = Move()
        self.future_safety = FutureSafety(self.move)

        self.game_state = "game_state"
        self.body = "body"
        self.move = "move"
        self.head = "head"
        self.my_length = "my_length"
        self.neck = "neck"

        self.patchers = [
            patch.object(self.future_safety, "log_data"),
            patch.object(Move, "call_get_body", return_value="new_body"),
            patch.object(Move, "get_neck", return_value="new_neck"),
            patch.object(self.future_safety, "future_safety")
        ]
        self.mocks = {}

        self.addCleanup(self.stop_patchers)
    
    def setup_patchers(self, extract_keywords_move, future_safety_return_value):

        patcher_extract_keywords = self.create_patcher_extract_keywords(extract_keywords_move)
        self.patchers.append(patcher_extract_keywords)

        patcher_future_safety = self.create_patcher_future_safety(future_safety_return_value)
        self.patchers.append(patcher_future_safety)

        self.start_patchers()
    
    def create_patcher_extract_keywords(self, move):

        patcher = patch.object(self.future_safety.keywords, "extract_keywords", return_value=("game_state", "body", move, {"x": 2, "y": 2}, "my_length", "neck"))
        return patcher
    
    def create_patcher_future_safety(self, return_value):

        patcher = patch.object(self.future_safety, "future_safety", return_value=(return_value, "node_ids"))
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
                mock.assert_called()
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    pass
                else:
                    raise
    
    def test_2_calls_move_up(self):

        self.setup_patchers("up", True)
        result = self.future_safety.call_future_safety(2, game_state=self.game_state, body=self.body, move=self.move, head=self.head, my_length=self.my_length, neck=self.neck)
        self.check_calls()

        self.assertTrue(result)

    def test_2_call_move_left(self):

        self.setup_patchers("left", False)
        result = self.future_safety.call_future_safety(2, game_state=self.game_state, body=self.body, move=self.move, head=self.head, my_length=self.my_length, neck=self.neck)
        self.check_calls()

        self.assertFalse(result)

    def test_1_call_move_up(self):

        self.setup_patchers("up", False)
        result = self.future_safety.call_future_safety(1, game_state=self.game_state, body=self.body, move=self.move, head=self.head, my_length=self.my_length, neck=self.neck)
        self.check_calls()

        self.assertFalse(result)

    def test_1_call_move_left(self):

        pass

if __name__ == "__main__":

    unittest.main()

