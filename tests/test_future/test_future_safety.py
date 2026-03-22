
import unittest
from unittest.mock import patch , MagicMock

from future.future_safety import FutureSafety
from future.future_safety_tree import FutureSafetyTree
from move import Move
from keywords import Keywords

# Tests that future_safety correctly simulates moves and tracks safe paths.
class TestFutureSafety(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.future_safety = FutureSafety(self.bot)

        self.head = {}
        self.game_state = {}
        self.body = []
        self.neck = {}
        self.my_length = 0
        self.child_id = 0

        patch.object(Move, "calculate_moves").start()
        patch.object(self.future_safety, "create_future_safety_tree", return_value="root id").start()
        patch.object(self.future_safety, "reset_safe_moves").start()
        patch.object(self.future_safety, "extract_data_from_tree", return_value=(self.head, self.body, self.neck, self.my_length)).start()
        patch.object(self.future_safety.future_safety_tree, "add_node", side_effect=self._fake_add_node).start()
        patch.object(self.future_safety, "get_move", return_value=self.head).start()
        patch.object(self.future_safety, "create_data_from_head", return_value=(self.body, self.neck, self.my_length)).start()
        patch.object(self.future_safety.move, "calculate_is_growing", return_value=False).start()

        self.addCleanup(patch.stopall)

    def _fake_add_node(self, *args, **kwargs):
        # returns incrementing ids to simulate tree node creation
        child_id = self.child_id
        self.child_id += 1
        return child_id

    def _call(self):
        return self.future_safety.future_safety(
            head=self.head, game_state=self.game_state,
            body=self.body, neck=self.neck, my_length=self.my_length
        )

    def test_safe_move_left(self):
        # verifies that safe_move_left is True and node ids are tracked when moves are safe
        with patch.object(self.future_safety, "safe_moves", new={
            "left":  {"is_safe": True},
            "right": {"is_safe": True},
            "up":    {"is_safe": True},
            "down":  {"is_safe": True},
        }):
            safe_move_left, node_ids = self._call()

            self.assertTrue(safe_move_left)
            self.assertEqual(node_ids, [0, 1, 2, 3])

    def test_no_safe_move_left(self):
        # verifies that safe_move_left is False and node ids are empty when no moves are safe
        with patch.object(self.future_safety, "safe_moves", new={
            "left":  {"is_safe": False},
            "right": {"is_safe": False},
            "up":    {"is_safe": False},
            "down":  {"is_safe": False},
        }):
            safe_move_left, node_ids = self._call()

            self.assertFalse(safe_move_left)
            self.assertEqual(node_ids, [])

if __name__ == "__main__":

    unittest.main()