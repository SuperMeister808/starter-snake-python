
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from emergency_logger import EmergencyLogger

class TestGetSafeMoves(unittest.TestCase):
    
    def setUp(self):
        
        self.patchers = [
            patch.object(EmergencyLogger, "loger_queue")
        ]

        mocks = {}

        for patcher in self.patchers:

            mock = patcher.start()
            mocks ["mock_loger_queue"] = mock

        self.mock_loger_queue = mocks ["mock_loger_queue"]
        self.mock_loger_queue.put = MagicMock()
        
        self.addCleanup(self.stop_patcher)

    def stop_patcher(self):

        for patcher in self.patchers:

            patcher.stop()
    

    def test_correct_is_move_safe(self):

        bot = Move()
        
        with patch.object(bot, "is_move_safe", new={"left": {"is_safe": False, "priority": 3}, "right": {"is_safe": True, "priority": 2}, "up": {"is_safe": False, "priority": 1}, "down": {"is_safe": True, "priority": 0}}):

           game_state = {"testing...": "testing..."}
           result = bot.get_safe_moves(game_state)

           self.mock_loger_queue.put.assert_not_called()
           
           expected = {"right": 2, "down": 0}
           self.assertEqual(result, expected)

    def test_exception_is_move_safe(self):

        bot = Move()

        with patch.object(bot, "is_move_safe") as mock_is_move_safe:
            
            mock_is_move_safe.items = MagicMock()
            exc = RuntimeError("side effect")
            mock_is_move_safe.items.side_effect = exc

            game_state = {"testing...": "testing..."}
            result = bot.get_safe_moves(game_state)

            self.mock_loger_queue.put.assert_called_once_with(("safe_moves", "side effect", game_state))
            expection = {"left": 0, "right": 0, "up": 0, "down": 0}
            self.assertEqual(result, expection)

if __name__ == "__main__":

    unittest.main()