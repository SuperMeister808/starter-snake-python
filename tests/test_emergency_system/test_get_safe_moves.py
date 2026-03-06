
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from emergency_logger import EmergencyLogger

class TestGetSafeMoves(unittest.TestCase):
    
    bot = Move()

    def setUp(self):
        
        self.patchers = [
            patch.object(self.bot, "is_move_safe", new={"left": {"is_safe": True}, "right": {"is_safe": True}, "down": {"is_safe": True}, "up": {"is_safe": True}})
        ]

        self.mock_loger_queue = patch.object(EmergencyLogger, "logger_queue")
        self.patchers.append(self.mock_loger_queue)
        self.mock_loger_queue.put = MagicMock()

        self.mocks = {}
        
        self.addCleanup(self.stop_patcher)

    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):

            mock = patcher.start()
            try:
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    self.mocks [i] = mock
                else:
                    raise
    
    def stop_patcher(self):

        for patcher in self.patchers:

            patcher.stop()
    
    @classmethod
    @patch.object(bot.future_safety, "call_future_safety")
    def test_multiple_safe_moves(cls, mock_call_future_safety):

        mock_call_future_safety.return_value = True
        result = cls.bot.check_safe_moves(2, )

        cls.assertTrue(cls, result)

    def test_one_safe_move(self):

        pass

    def test_exception_is_move_safe(self):

        bot = Move()

        with patch.object(bot, "is_move_safe") as mock_is_move_safe:
            
            mock_is_move_safe.items = MagicMock()
            exc = RuntimeError("side effect")
            mock_is_move_safe.items.side_effect = exc

            game_state = {"testing...": "testing..."}
            result = bot.get_safe_moves(game_state)

            self.mock_loger_queue.put.assert_called_once_with(("safe_moves", "side effect", game_state))
            mock_is_move_safe.items.assert_called_once()
            expection = {"left": 0, "right": 0, "up": 0, "down": 0}
            self.assertEqual(result, expection)

if __name__ == "__main__":

    unittest.main()