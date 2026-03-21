
import unittest
from unittest.mock import patch , MagicMock

from logger.emergency_logger import EmergencyLogger
from logger.runtime_logger import RuntimeLogger

# Tests that emergency_log correctly logs messages with default and custom parameters.
class TestEmergencyLog(unittest.TestCase):

    def setUp(self):
        EmergencyLogger.setup_runtime_logger("TestLogger", "test.log", False)

        self.mock_create_message = patch.object(
            EmergencyLogger, "create_message",
            side_effect=lambda where, exception: f"{where}: {exception}"
        ).start()

        self.mock_log = patch.object(
            EmergencyLogger.runtime_logger, "log"
        ).start()

        self.addCleanup(patch.stopall)

    def test_default_level_and_turn(self):
        # verifies that level defaults to 40 (ERROR) and turn defaults to "unknown"
        EmergencyLogger.emergency_log("wherever", "Testing...")

        self.mock_log.assert_called_once_with(
            40, "wherever: Testing...", extra={"turn": "unknown"}
        )

    def test_customized_level_and_turn(self):
        # verifies that custom level and turn are passed through correctly
        EmergencyLogger.emergency_log("wherever", "Testing...", 20, 0)

        self.mock_log.assert_called_once_with(
            20, "wherever: Testing...", extra={"turn": 0}
        )

    @patch.object(EmergencyLogger, "create_message")
    def test_exception_raises_runtime_error(self, mock_create_message):
        # verifies that a RuntimeError is raised if create_message fails
        mock_create_message.side_effect = RuntimeError("side effect")

        with self.assertRaises(RuntimeError):
            EmergencyLogger.emergency_log("wherever", "Testing...", 20, 0)

    @patch.object(EmergencyLogger, "runtime_logger", new=None)
    def test_no_runtime_logger_raises_runtime_error(self):
        # verifies that a RuntimeError is raised if the logger is not initialized
        with self.assertRaises(RuntimeError):
            EmergencyLogger.emergency_log("wherever", "Testing...", 20, 0)

if __name__ == "__main__":

    unittest.main()