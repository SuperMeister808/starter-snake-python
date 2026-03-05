
import unittest
from unittest.mock import patch , MagicMock

from future_safety import FutureSafety
from future_safety_tree import FutureSafetyTree
from move import Move
from keywords import Keywords

class TestFutureSafety(unittest.TestCase):

    def setUp(self):

        self.bot = Move()
        self.future_safety = FutureSafety(self.bot)

        self.head = "head"
        self.game_state = "game_state"
        self.body = "body"
        self.neck = "neck"
        self.my_length = "my_length"
        
        self.child_id = 0
        self.patchers = [
            patch.object(self.future_safety, "log_data"),
            patch.object(Move, "check_moves"),
            patch.object(Keywords, "extract_keywords", return_value=("head", "game_state", "body", "neck", "my_length")),
            patch.object(self.future_safety, "create_future_safety_tree", return_value="root id"),
            patch.object(self.future_safety, "reset_safe_moves"),
            patch.object(self.future_safety, "extract_data_from_tree", return_value=("head", "body", "neck", "my_length")),
            patch.object(self.future_safety, "get_move", return_value="move possition"),
            patch.object(self.future_safety.future_safety_tree, "add_node", side_effect=self.fake_add_node),
            patch.object(Move, "call_get_body", return_value=("head", "body")),
            patch.object(Move, "get_neck", return_value=("body"))
        ]
        self.mocks = {}

        self.addCleanup(self.stop_patchers)
        
    def fake_add_node(self, *args, **kwargs):

        child_id = self.child_id
        self.child_id += 1

        return child_id
    
    def setup_patchers(self, new_safe_moves):

        patcher_safe_moves = self.create_patcher_safe_moves(new_safe_moves)
        self.patchers.append(patcher_safe_moves)

        self.start_patchers()
    
    def create_patcher_safe_moves(self, new):

        patcher = patch.object(self.future_safety, "safe_moves", new=new)
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

        safe_moves = {"left": {"is_safe": True}, "right": {"is_safe": True}, "up": {"is_safe": True}, "down": {"is_safe": True}}
        self.setup_patchers(safe_moves)


        safe_move_left , node_ids = self.future_safety.future_safety(head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)
        self.check_calls()

        self.assertTrue(safe_move_left)
        self.assertEqual(node_ids, [0, 1, 2, 3])

    def test_no_safe_move_left(self):
        
        pass

if __name__ == "__main__":

    unittest.main()