
import unittest
from unittest.mock import patch , MagicMock

from future.future_safety import FutureSafety
from move import Move

# Tests that call_future_safety correctly simulates future turns and returns safe move status.
class TestCallFutureSafety(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.future_safety = FutureSafety(self.bot)

        patch.object(self.bot.extract_data, "call_get_body", return_value="new_body").start()
        patch.object(self.bot.extract_data, "get_neck", return_value="new_neck").start()

        self.addCleanup(patch.stopall)

    def _setup(self, move, safe_move_result):
        # sets up extract_keywords and future_safety mocks for each test
        patch.object(
            self.future_safety.keywords, "extract_keywords",
            return_value=("game_state", "body", move, {"x": 2, "y": 2}, "my_length", "neck")
        ).start()
        patch.object(
            self.future_safety, "future_safety",
            return_value=(safe_move_result, "node_ids")
        ).start()

    def _call(self, calls):
        return self.future_safety.call_future_safety(
            calls,
            game_state="game_state", body="body", move="move",
            head="head", my_length="my_length", neck="neck"
        )

    def test_2_calls_move_up_safe(self):
        # verifies that True is returned when future simulation finds safe moves
        self._setup("up", True)
        self.assertTrue(self._call(2))

    def test_2_calls_move_left_unsafe(self):
        # verifies that False is returned when future simulation finds no safe moves
        self._setup("left", False)
        self.assertFalse(self._call(2))

    def test_1_call_move_up_unsafe(self):
        # verifies that False is returned with 1 call when no safe moves exist
        self._setup("up", False)
        self.assertFalse(self._call(1))

    def test_1_call_move_left_safe(self):
        # verifies that True is returned with 1 call when safe moves exist
        self._setup("left", True)
        self.assertTrue(self._call(1))

if __name__ == "__main__":

    unittest.main()

