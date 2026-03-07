
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

import queue

import threading

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        EmergencyLogger.setup_runtime_logger("TestLoger", "test.log", False)
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", new=lambda where, exception, level, turn: (where, exception, level, turn)),
            patch.object(EmergencyLogger.loger_queue, "get", new=MagicMock(wraps=EmergencyLogger.loger_queue.get)),
            patch.object(EmergencyLogger.loger_queue, "task_done", new=MagicMock(wraps=EmergencyLogger.loger_queue.task_done))
        ]
        self.mocks = {}

        self.start_patchers()
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:

            patcher.start()
    
    def stop_patchers(self):


        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            try:
                mock.assert_called_once()
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    pass
                else:
                    raise
    
    @patch.object(EmergencyLogger, "loger_queue", new=queue.Queue())
    @patch.object(EmergencyLogger, "flags", new={"is_running": True, "worker_thread": None})
    def test_coorect_queue(self):

        EmergencyLogger.loger_queue.put(("wherever", "exception", "turn", "level"))
        EmergencyLogger.log_worker()



    def test_queue_3_elements(self):

        pass

    def test_queue_2_elements(self):

        pass

    def test_empty_queue(self):

        q = queue.Queue()

        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = "logger queue is empty"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)
            
            EmergencyLogger.print_collector.clear_messages()

    def test_fallback(self):

        pass

    def test_flag_is_running_False(self):

        pass

if __name__ == "__main__":

    unittest.main()