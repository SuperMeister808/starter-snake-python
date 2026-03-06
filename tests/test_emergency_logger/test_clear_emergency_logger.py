
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger
from runtime_logger import RuntimeLogger

class TestClearEmergencyLogger(unittest.TestCase):

    @patch.object(EmergencyLogger, "flags", new={})
    @patch.object(EmergencyLogger, "runtime_logger", new="runtime_logger")
    @patch.object(RuntimeLogger, "close_file_handlers")
    @patch.object(EmergencyLogger.print_collector, "clear_messages")
    def test_clear_emergency_logger(self, mock_print_collector_clear_messages, mock_close_file_handlers):

        EmergencyLogger.clear_emergency_logger()

        self.assertEqual(EmergencyLogger.flags, {"is_running": False, "worker_thread": None})
        mock_close_file_handlers.assert_called_once_with(EmergencyLogger.runtime_logger)
        mock_print_collector_clear_messages.assert_called_once()

if __name__ == "__main__":

    unittest.main()


