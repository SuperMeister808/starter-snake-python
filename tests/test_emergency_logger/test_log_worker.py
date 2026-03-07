
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

import queue

import threading

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        EmergencyLogger.setup_runtime_logger("TestLoger", "test.log", False)
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", new=MagicMock(name="emergency_log")),
            patch.object(EmergencyLogger.loger_queue, "get", new=MagicMock(wraps=EmergencyLogger.loger_queue.get, name="get")),
            patch.object(EmergencyLogger.loger_queue, "task_done", new=MagicMock(wraps=EmergencyLogger.loger_queue.task_done, name="taks_done"))
        ]
        self.mocks = {}

        self.start_patchers()
        
        #FILO
        self.addCleanup(self.stop_patchers)
        self.addCleanup(self.join_thread)

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

        log_worker_thread = threading.Thread(target=EmergencyLogger.log_worker) 
        EmergencyLogger.flags ["worker_thread"] = log_worker_thread
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        log_worker_thread.start()

    def join_thread(self):

        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if isinstance(log_worker_thread, threading.Thread):
            log_worker_thread.join()
        
    def test_coorect_queue(self):

        self.start_thread()
        
        EmergencyLogger.loger_queue.put(("wherever", "exception", "turn", "level"))
        self.check_calls()
        mock_emergency_log = self.mocks ["emergency_log"]
        mock_emergency_log.assert_called_once_with(("wherever", "exception", "turn", "level"))

        EmergencyLogger.loger_queue.put(("whereever2", "exception2", "turn2", "level2"))
        self.check_calls()
        mock_emergency_log = self.mocks ["emergency_log"]
        mock_emergency_log.assert_called_with(("whereever2", "exception2", "turn2", "level2"))

        EmergencyLogger.flags ["is_running"] = False

        EmergencyLogger.loger_queue.put(("whereever3", "exception3", "turn3", "level3"))
        self.check_no_calls()
        mock_emergency_log = self.mocks ["emergency_log"]
        mock_emergency_log.assert_not_called()

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