
import unittest
from unittest.mock import patch , MagicMock

from future_safety import FutureSafety
from future_safety_tree import FutureSafetyTree
from move import Move

class TestFutureSafety(unittest.TestCase):

    def setUp(self):

        self.bot = Move()
        self.future_safety = FutureSafety(self.bot)
        
        self.patchers = [
            patch.object(FutureSafety, "log_data"),
            patch.object(Move, "check_moves"),
            patch.object(FutureSafety, "extract_keywords", return_value=("head", "game_state", "body", "neck", "my_length")),
            patch.object(FutureSafety, "create_future_safety_tree", return_value="root id"),
            patch.object(FutureSafety, "reset_safe_moves"),
            patch.object(FutureSafety, "extract_data_from_tree", return_value=("head", "body", "neck", "my_length")),
            patch.object(FutureSafety, "get_move", return_value="move possition"),
            patch.object(FutureSafetyTree, "add_node", return_value="child id")
        ]
        self.mocks = {}

        self.addCleanup(self.stop_patchers)
        
    def setup_patchers(self, new_safe_moves):

        patcher_opponents_positions = self.create_patcher_opponents_positions(new_safe_moves)
        self.patchers.append(patcher_opponents_positions)

        self.start_patchers()
    
    def create_patcher_check_moves(self, new):

        patcher = patch.object(FutureSafety, "safe_moves", new=new)
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
            try:
                mock.assert_called()
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    pass
                else:
                    raise
    
    def test_safe_move_left(self):

        safe_moves = {"left": True, "right": True, "up": True, "down": True}
        self.setup_patchers(safe_moves)

        head = "head"
        game_state = "game_state"
        
        self.future_safety.future_safety()


    def test_no_safe_move_at_second_level(self):

        pass

    def test_no_safe_move_left(self):
        

        pass