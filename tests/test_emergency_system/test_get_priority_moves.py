
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger
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

        game_state = {"testing...": "testing..."}
        safe_moves = {"left": 2, "right": 1, "up": 0, "down": 2}

        result = self.bot.get_priority_moves(game_state, safe_moves)

        self.mock_loger_queue.put.assert_not_called()

        expected = ["left", "down"]
        self.assertEqual(result, expected)

    def test_exception(self):

        game_state = {"testing...": "testing..."}
        
        safe_moves = MagicMock()
        safe_moves.items = MagicMock()
        exc = RuntimeError("side effect")
        safe_moves.items.side_effect = exc

        result = self.bot.get_priority_moves(game_state, safe_moves)

        safe_moves.items.assert_called_once()
        self.mock_loger_queue.put.assert_called_once_with(("priority", "side effect", game_state))

        expected = []
        self.assertEqual(result, expected)


if __name__ == "__main__":

    unittest.main()