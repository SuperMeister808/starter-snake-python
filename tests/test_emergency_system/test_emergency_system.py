
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger
from move import Move

class TestEmergencySystem(unittest.TestCase):

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

        self.addCleanup(self.stop_patchers)

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def test_correct_call(self):

        bot = Move()
        
        func = MagicMock()
        game_state = {"testing...": "testing..."}
        arg = "Testing..."

        bot.emergency_system(game_state, func, arg, kwarg=True)

        func.assert_called_once_with(arg, kwarg=True)

        self.mock_loger_queue.put.assert_not_called()

    def test_exception_reset_is_move_safe(self):

        bot = Move()

        game_state = {"testing...": "testing..."}
        func = MagicMock()
        func.__name__ = "reset_is_move_safe"
        exc = RuntimeError("side effect")
        func.side_effect = exc
        arg = "Testing..."
        kwarg = True

        with patch.object(bot, "is_move_safe", new={}):
        
            bot.emergency_system(game_state, func, arg, kwarg=kwarg)

            func.assert_called_once_with(arg, kwarg=kwarg)
            self.mock_loger_queue.put.assert_called_once_with((func.__name__, exc, game_state))

            self.assertEqual(bot.is_move_safe, {"left": {"is_safe": True, "priority": 0}, 
                                "right": {"is_safe": True, "priority": 0},
                                 "up": {"is_safe": True, "priority": 0},
                                 "down": {"is_safe": True, "priority": 0}})

    @patch("move.random.choice")
    def test_exception(self, mock_choice):

        bot = Move()
        
        game_state = {"testing...": "testing..."}
        func = MagicMock()
        func.__name__ = "test_func"
        exc = RuntimeError("side effect")
        func.side_effect = exc
        arg = "Testing..."
        kwarg = True

        mock_choice.return_value = "left"
        
        result = bot.emergency_system(game_state, func, arg, kwarg=kwarg)
        
        func.assert_called_once_with(arg, kwarg=kwarg)
        self.mock_loger_queue.put.assert_called_once_with((func.__name__, exc, game_state))
        mock_choice.assert_called_once_with(["left", "right", "up", "down"])
        self.assertEqual(result, {"move": "left"})


if __name__ == "__main__":

    unittest.main()