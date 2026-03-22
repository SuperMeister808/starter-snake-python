
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from logger.emergency_logger import EmergencyLogger

import unittest
from unittest.mock import patch, MagicMock

from move import Move
from logger.emergency_logger import EmergencyLogger

# Tests that check_safe_moves correctly marks moves as safe or unsafe based on future simulation.
class TestGetSafeMoves(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.head = {}
        self.game_state = {}
        self.body = []
        self.neck = {}
        self.my_length = 0

        patch.object(EmergencyLogger.loger_queue, "put").start()
        self.addCleanup(patch.stopall)

    def test_multiple_safe_moves(self):
        # verifies that all moves remain safe when future simulation returns True
        with patch.object(self.bot, "is_move_safe", new={
            "left":  {"is_safe": True},
            "right": {"is_safe": True},
            "down":  {"is_safe": True},
            "up":    {"is_safe": True},
        }):
            with patch.object(self.bot.future_safety, "call_future_safety", return_value=True):
                self.bot.check_safe_moves(2, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

                for move, data in self.bot.is_move_safe.items():
                    self.assertTrue(data["is_safe"])

    def test_no_safe_move(self):
        # verifies that all moves are marked unsafe when future simulation returns False
        with patch.object(self.bot, "is_move_safe", new={
            "left":  {"is_safe": True},
            "right": {"is_safe": True},
            "down":  {"is_safe": True},
            "up":    {"is_safe": True},
        }):
            with patch.object(self.bot.future_safety, "call_future_safety", return_value=False):
                self.bot.check_safe_moves(2, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

                for move, data in self.bot.is_move_safe.items():
                    self.assertFalse(data["is_safe"])

    @patch("move.deepcopy")
    def test_exception_resets_is_move_safe(self, mock_deepcopy):
        # verifies that an exception resets is_move_safe to all safe with zero priority
        mock_deepcopy.side_effect = RuntimeError("side effect")

        self.bot.check_safe_moves(2, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

        expected = {
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
        }
        self.assertEqual(self.bot.is_move_safe, expected)

if __name__ == "__main__":

    unittest.main()