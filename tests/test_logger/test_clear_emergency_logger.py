
import unittest
from unittest.mock import patch

from logger.emergency_logger import EmergencyLogger
from logger.runtime_logger import RuntimeLogger

# Tests that clear_emergency_logger resets flags and closes file handlers.
class TestClearEmergencyLogger(unittest.TestCase):

    @patch.object(EmergencyLogger, "flags", new={})
    @patch.object(EmergencyLogger, "runtime_logger", new="runtime_logger")
    @patch.object(RuntimeLogger, "close_file_handlers")
    def test_clear_emergency_logger(self, mock_close_file_handlers):

        EmergencyLogger.clear_emergency_logger()

        self.assertEqual(EmergencyLogger.flags, {"is_running": False, "worker_thread": None})
        mock_close_file_handlers.assert_called_once_with(EmergencyLogger.runtime_logger)

if __name__ == "__main__":

    unittest.main()


