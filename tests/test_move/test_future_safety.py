
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from future_safety import FutureSafety

class TestFutureSafety(unittest.TestCase):

    move = Move()
    future_safety = FutureSafety(move)
    def setUp(self):
        self.head = {"x": 2, "y": 2}
        self.game_state = {}
        self.body = [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]
        self.neck = {"x": 2, "y": 3}
        self.my_length = 3
        
        self.patchers = [
            patch.object(self.future_safety, "extract_keywords", return_value=(self.head, self.game_state, self.body, self.neck, self.my_length)),
            patch.object(self.future_safety, "log_data"),
            patch.object(self.future_safety, "reset_safe_moves"),
            patch.object(self.future_safety.move, "check_moves")
        ]
        self.mocks = {}

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

    @patch.object(future_safety, "safe_moves", new={"left": {"is_safe": False}, "right": {"is_safe": False}, "up": {"is_safe": True}, "down": {"is_safe": False}})
    def test_one_safe_move_left(self):

        self.future_safety.future_safety()

    def test_multiple_safe_moves_left(self):

        pass

    def test_node_ids_is_not_default(self):

        pass
        

if __name__ == "__main__":
    unittest.main()

        




        

        