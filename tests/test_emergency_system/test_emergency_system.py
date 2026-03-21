
import unittest
from unittest.mock import patch , MagicMock

from logger.emergency_logger import EmergencyLogger
from emergency_system import EmergencySystem
from move import Move

import unittest
from unittest.mock import patch, MagicMock

from move import Move
from emergency_system import EmergencySystem
from logger.emergency_logger import EmergencyLogger

# Tests that emergency_system correctly calls functions and returns fallback moves on failure.
class TestEmergencySystem(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.emergency_system = EmergencySystem(self.bot)

        self.mock_loger_queue = patch.object(EmergencyLogger, "loger_queue").start()
        self.mock_loger_queue.put = MagicMock()

        self.addCleanup(patch.stopall)

    def test_correct_call(self):
        # verifies that the function is called with the correct arguments
        func = MagicMock()

        self.emergency_system.emergency_system(func, "Testing...", kwarg=True)

        func.assert_called_once_with("Testing...", kwarg=True)
        self.mock_loger_queue.put.assert_not_called()

    def test_exception(self):
        # verifies that an emergency move is returned when the function raises an exception
        func = MagicMock()
        func.__name__ = "test_func"
        exc = RuntimeError("side effect")
        func.side_effect = exc

        result = self.emergency_system.emergency_system(func, "Testing...", kwarg=True)

        self.mock_loger_queue.put.assert_called_once_with(
            (func.__name__, exc, self.bot.turn_counter, 40)
        )
        self.assertIn(result["move"], self.emergency_system.EMERGENCY_MOVES)
        self.assertEqual(result["id"], self.emergency_system.EMERGENCY_ID)

    @patch("random.choice")
    def test_hard_fallback(self, mock_choice):
        # verifies that "down" is returned as last resort if random.choice also fails
        func = MagicMock()
        func.__name__ = "test_func"
        exc = RuntimeError("side effect")
        func.side_effect = exc
        mock_choice.side_effect = exc

        result = self.emergency_system.emergency_system(func, "Testing...", kwarg=True)

        self.assertEqual(self.mock_loger_queue.put.call_count, 2)
        self.assertEqual(result["move"], "down")
        self.assertEqual(result["id"], self.emergency_system.EMERGENCY_ID)

if __name__ == "__main__":

    unittest.main()