
import unittest
from unittest.mock import patch , MagicMock

from logger.emergency_logger import EmergencyLogger
from move import Move

class TestGetPriorityMoves(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        
        self.patchers = [
            patch.object(EmergencyLogger, "loger_queue")
        ]

        mocks = {}
        
        for patcher in self.patchers:

            mock = patcher.start()
            mocks ["mock_loger_queue"] = mock

        self.mock_loger_queue = mocks ["mock_loger_queue"]
        self.mock_loger_queue.put = MagicMock()

        self.addCleanup(self.stop_patchers)
    
    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()
    
    def test_one_priority_move(self):

        new_is_move_safe = {"left": {"priority": 0}, "right": {"priority": 2}, "up": {"priority": 0}, "down": {"priority": 1}}

        with patch.object(self.bot, "is_move_safe", new=new_is_move_safe):
        
            self.bot.check_priority_moves()

            self.mock_loger_queue.put.assert_not_called()

            expected = ["right"]
            self.assertEqual(self.bot.priority_moves, expected)

    def test_multiple_priority_moves(self):

        new_is_move_safe = {"left": {"priority": 1}, "right": {"priority": 0}, "up": {"priority": 1}, "down": {"priority": 1}}

        with patch.object(self.bot, "is_move_safe", new=new_is_move_safe):
            
            self.bot.check_priority_moves()

            self.mock_loger_queue.put.assert_not_called()

            expected = ["left", "up", "down"]
            self.assertEqual(self.bot.priority_moves, expected)

    def test_exception(self):

        with patch.object(self.bot, "is_move_safe") as mock_is_move_safe:
            exc = RuntimeError("side effect")
            mock_is_move_safe.items = MagicMock()
            mock_is_move_safe.items.side_effect = exc

            self.bot.check_priority_moves()

            mock_is_move_safe.items.assert_called_once()
            self.mock_loger_queue.put.assert_called_once_with(("check_priority_moves", exc, self.bot.turn_counter, 40))

            expected = []
            self.assertEqual(self.bot.priority_moves, expected)

if __name__ == "__main__":

    unittest.main()