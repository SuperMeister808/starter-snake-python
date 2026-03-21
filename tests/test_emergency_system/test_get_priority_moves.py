
import unittest
from unittest.mock import patch , MagicMock

from logger.emergency_logger import EmergencyLogger
from move import Move

import unittest
from unittest.mock import patch, MagicMock

from move import Move
from logger.emergency_logger import EmergencyLogger

# Tests that check_priority_moves correctly identifies the highest priority moves.
class TestGetPriorityMoves(unittest.TestCase):

    def setUp(self):
        self.bot = Move()

        self.mock_loger_queue = patch.object(EmergencyLogger, "loger_queue").start()
        self.mock_loger_queue.put = MagicMock()

        self.addCleanup(patch.stopall)

    def test_one_priority_move(self):
        # verifies that only the highest priority move is selected
        new_is_move_safe = {
            "left":  {"priority": 0},
            "right": {"priority": 2},
            "up":    {"priority": 0},
            "down":  {"priority": 1},
        }

        with patch.object(self.bot, "is_move_safe", new=new_is_move_safe):
            self.bot.check_priority_moves()

            self.mock_loger_queue.put.assert_not_called()
            self.assertEqual(self.bot.priority_moves, ["right"])

    def test_multiple_priority_moves(self):
        # verifies that all moves tied for highest priority are selected
        new_is_move_safe = {
            "left":  {"priority": 1},
            "right": {"priority": 0},
            "up":    {"priority": 1},
            "down":  {"priority": 1},
        }

        with patch.object(self.bot, "is_move_safe", new=new_is_move_safe):
            self.bot.check_priority_moves()

            self.mock_loger_queue.put.assert_not_called()
            self.assertEqual(self.bot.priority_moves, ["left", "up", "down"])

    def test_exception(self):
        # verifies that an exception resets priority_moves and logs the error
        with patch.object(self.bot, "is_move_safe") as mock_is_move_safe:
            exc = RuntimeError("side effect")
            mock_is_move_safe.items = MagicMock(side_effect=exc)

            self.bot.check_priority_moves()

            mock_is_move_safe.items.assert_called_once()
            self.mock_loger_queue.put.assert_called_once_with(
                ("check_priority_moves", exc, self.bot.turn_counter, 40)
            )
            self.assertEqual(self.bot.priority_moves, [])

if __name__ == "__main__":

    unittest.main()