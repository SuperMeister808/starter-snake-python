
import unittest
from unittest.mock import patch , MagicMock , call

from emergency_logger import EmergencyLogger

import queue

import threading

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        EmergencyLogger.setup_runtime_logger("TestLoger", "test.log", False)
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", new=MagicMock(name="emergency_log")),
            patch.object(EmergencyLogger, "flags", new={"is_running": False, "worker_thread": None}),
            patch.object(EmergencyLogger, "loger_queue", new=queue.Queue())
        ]
        self.mocks = {}
        
        #FILO
        self.addCleanup(self.stop_patchers)


    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):

            mock = patcher.start()
            try:
                self.mocks [mock.__wrapped__] = mock
            except AttributeError:
                try:
                    self.mocks [mock._mock_name] = mock
                except AttributeError:
                    if not isinstance(mock, MagicMock):
                        self.mocks [i] = mock
                    else:
                        raise

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            try:
                mock.assert_called()
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    pass
                else:
                    raise

    def check_no_calls(self):

        for name , mock in self.mocks.items():
            try:
                mock.assert_not_called()
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    pass
                else:
                    raise
    
    def start_thread(self):

        EmergencyLogger.flags ["is_running"] = True
        log_worker_thread = threading.Thread(target=EmergencyLogger.log_worker) 
        EmergencyLogger.flags ["worker_thread"] = log_worker_thread
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        log_worker_thread.start()

    def join_thread(self):

        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if isinstance(log_worker_thread, threading.Thread):
            log_worker_thread.join()
        
    def test_coorect_queue(self):

        self.start_patchers()
        self.start_thread()
        
        EmergencyLogger.loger_queue.put(("wherever", "exception", "turn", "level"))
        
        EmergencyLogger.loger_queue.put(("whereever2", "exception2", "turn2", "level2"))

        EmergencyLogger.flags ["is_running"] = False
        
        self.join_thread()

        self.assertTrue(EmergencyLogger.loger_queue.empty())
        expected_calls = [
            call("wherever", "exception", level="level", turn="turn"),
            call("whereever2", "exception2", level="level2", turn="turn2")
        ]

        EmergencyLogger.emergency_log.assert_has_calls(expected_calls)

        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        self.assertFalse(log_worker_thread.is_alive())

    def test_thread_dependency_to_flag_is_running(self):

        pass
    
    def test_queue_3_elements(self):

        pass

    def test_queue_2_elements(self):

        pass

    def test_empty_queue(self):

       pass

    def test_fallback(self):

        pass

    def test_flag_is_running_False(self):

        pass

if __name__ == "__main__":

    unittest.main()