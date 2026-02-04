
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger
from print_collector import PrintCollector

from queue import Queue

class TestClearEmergencyLogger(unittest.TestCase):

    
    def test_written_data(self):

        q = Queue()
        q.put("where", "exception", "game_state")
        
        print_collector = PrintCollector()
        print_collector.collect_message("text1")

        with (
            patch.object(EmergencyLogger, "loger_queue", new=q),
            patch.object(EmergencyLogger, "flags", new={"testing...": "Testing..."}),
            patch.object(EmergencyLogger, "print_collector", new=print_collector)
        ):
            EmergencyLogger.clear_emergency_logger()

            self.assertTrue(EmergencyLogger.loger_queue.empty())
            self.assertEqual(EmergencyLogger.flags, {"is_running": False, "worker_thread": None})
            messages = EmergencyLogger.print_collector.messages
            self.assertEqual(len(messages), 0)

    def test_already_cleared(self):

        q = Queue()
        
        print_collector = PrintCollector()

        with (
            patch.object(EmergencyLogger, "loger_queue", new=q),
            patch.object(EmergencyLogger, "flags", new={"is_running": False, "worker_thread": None}),
            patch.object(EmergencyLogger, "print_collector", new=print_collector)
        ):
            EmergencyLogger.clear_emergency_logger()

            self.assertTrue(EmergencyLogger.loger_queue.empty())
            self.assertEqual(EmergencyLogger.flags, {"is_running": False, "worker_thread": None})
            messages = EmergencyLogger.print_collector.messages
            self.assertEqual(len(messages), 0)

if __name__ == "__main__":

    unittest.main()