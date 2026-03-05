
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger
from emergency_system import EmergencySystem
from move import Move

class TestEmergencySystem(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        self.emergency_system = EmergencySystem(self.bot)
        
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
        
        func = MagicMock()
        arg = "Testing..."

        self.emergency_system.emergency_system(func, arg, kwarg=True)

        func.assert_called_once_with(arg, kwarg=True)

        self.mock_loger_queue.put.assert_not_called()

    def test_exception(self):

        func = MagicMock()
        func.__name__ = "test_func"
        exc = RuntimeError("side effect")
        func.side_effect = exc
        arg = "Testing..."
        kwarg = True
        
        emergency_moves = ["left", "right", "down", "up"]
        result = self.emergency_system.emergency_system(func, arg, kwarg=kwarg)
        
        func.assert_called_once_with(arg, kwarg=kwarg)
        self.mock_loger_queue.put.assert_called_once_with((func.__name__, exc, self.bot.turn_counter, 40))
        
        result_move = result["move"]
        result_id = result ["id"]
        self.assertIn(result_move, emergency_moves)
        self.assertEqual(result_id, "Emergency!")

if __name__ == "__main__":

    unittest.main()