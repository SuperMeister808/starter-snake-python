
import unittest
from unittest.mock import patch , MagicMock , call

from emergency_logger import EmergencyLogger

import queue

import threading

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        EmergencyLogger.setup_runtime_logger("TestLoger", "test.log", False)
        
        self.where = "wherever"
        self.exception = "exception"
        self.turn = "turn"
        self.level = "level"
        self.where_2 = "wherever2"
        self.exception_2 = "exception2"
        self.turn_2 = "turn2"
        self.level_2 = "level_2"
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", new=MagicMock(wraps=EmergencyLogger.emergency_log)),
            patch.object(EmergencyLogger, "flags", new={"is_running": False, "worker_thread": None}),
            patch.object(EmergencyLogger, "loger_queue", new=queue.Queue()),
            patch.object(EmergencyLogger.runtime_logger, "log"),
            patch.object(EmergencyLogger, "create_message", side_effect=lambda where, exception: (where, exception))
        ]
        self.mocks = {}
        
        #FILO
        self.addCleanup(self.stop_patchers)
        self.addCleanup(self.teardown)


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
        if isinstance(log_worker_thread, threading.Thread):
            EmergencyLogger.flags ["worker_thread"] = log_worker_thread
            log_worker_thread = EmergencyLogger.flags ["worker_thread"]
            log_worker_thread.start()
        else:
            raise RuntimeError("Kein thread Objekt referenziert!")

    def join_thread(self, timeout):

        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if isinstance(log_worker_thread, threading.Thread):
            log_worker_thread.join(timeout)
        else:
            raise RuntimeError("Kein thread Objekt referenziert!")

    def teardown(self):

        EmergencyLogger.flags ["is_running"] = False
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if isinstance(log_worker_thread, threading.Thread):
            log_worker_thread.join(timeout=2)
        else:
            raise RuntimeError("Kein Thread Objekt referenziert!")

    def test_coorect_queue(self):

        self.start_patchers()
        self.start_thread()
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if not isinstance(log_worker_thread, threading.Thread):
            raise RuntimeError("Kein thread Objekt referenziert!")
        
       
        
        EmergencyLogger.loger_queue.put((self.where, self.exception, self.turn, self.level))
        EmergencyLogger.loger_queue.put((self.where_2, self.exception_2, self.turn_2, self.level_2))

        EmergencyLogger.flags ["is_running"] = False
        self.join_thread(2)

        self.assertFalse(log_worker_thread.is_alive())

        self.assertTrue(EmergencyLogger.loger_queue.empty())
        expected_calls_emergency_log = [
            call(self.where, self.exception, level=self.level, turn=self.turn),
            call(self.where_2, self.exception_2, level=self.level_2, turn=self.turn_2)
        ]
        EmergencyLogger.emergency_log.assert_has_calls(expected_calls_emergency_log)
        expected_calls_log = [
            call(self.level, (self.where, self.exception), extra={"turn": self.turn}),
            call(self.level_2, (self.where_2, self.exception_2), extra={"turn": self.turn_2})
        ]
        EmergencyLogger.runtime_logger.log.assert_has_calls(expected_calls_log)



    def test_thread_dependency_to_flag_is_running(self):

        self.start_patchers()
        self.start_thread()
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if not isinstance(log_worker_thread, threading.Thread):
            raise RuntimeError("Kein thread Objekt referenziert!")

        EmergencyLogger.loger_queue.put((self.where, self.exception, self.turn, self.level))
        EmergencyLogger.loger_queue.put((self.where_2, self.exception_2, self.turn_2, self.level_2))

        self.join_thread(2)
        self.assertTrue(log_worker_thread.is_alive())

        self.assertTrue(EmergencyLogger.loger_queue.empty())
        expected_calls_emergency_log = [
            call(self.where, self.exception, level=self.level, turn=self.turn),
            call(self.where_2, self.exception_2, level=self.level_2, turn=self.turn_2)
        ]
        EmergencyLogger.emergency_log.assert_has_calls(expected_calls_emergency_log)
        expected_calls_log = [
            call(self.level, (self.where, self.exception), extra={"turn": self.turn}),
            call(self.level_2, (self.where_2, self.exception_2), extra={"turn": self.turn_2})
        ]
        EmergencyLogger.runtime_logger.log.assert_has_calls(expected_calls_log)
   
        EmergencyLogger.flags ["is_running"] = False
        self.join_thread(2)
        self.assertFalse(log_worker_thread.is_alive())
    
    def test_queue_3_elements(self):

        self.start_patchers()
        self.start_thread()
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if not isinstance(log_worker_thread, threading.Thread):
            raise RuntimeError("Kein thread Objekt referenziert!")
        
        EmergencyLogger.loger_queue.put((self.where, self.exception, self.turn))
        EmergencyLogger.loger_queue.put((self.where_2, self.exception_2, self.turn_2))

        EmergencyLogger.flags ["is_running"] = False
        self.join_thread(2)

        self.assertFalse(log_worker_thread.is_alive())

        self.assertTrue(EmergencyLogger.loger_queue.empty())
        expected_calls_emergency_log = [
            call(self.where, self.exception, turn=self.turn),
            call(self.where_2, self.exception_2, turn=self.turn_2)
        ]
        EmergencyLogger.emergency_log.assert_has_calls(expected_calls_emergency_log)
        expected_calls_log = [
            call(40, (self.where, self.exception), extra={"turn": self.turn}),
            call(40, (self.where_2, self.exception_2), extra={"turn": self.turn_2})
        ]
        EmergencyLogger.runtime_logger.log.assert_has_calls(expected_calls_log)

    def test_queue_2_elements(self):

        self.start_patchers()
        self.start_thread()
        log_worker_thread = EmergencyLogger.flags ["worker_thread"]
        if not isinstance(log_worker_thread, threading.Thread):
            raise RuntimeError("Kein thread Objekt referenziert!")
        
        EmergencyLogger.loger_queue.put((self.where, self.exception))
        EmergencyLogger.loger_queue.put((self.where_2, self.exception_2))

        EmergencyLogger.flags ["is_running"] = False
        self.join_thread(2)

        self.assertFalse(log_worker_thread.is_alive())

        self.assertTrue(EmergencyLogger.loger_queue.empty())
        expected_calls_emergency_log = [
            call(self.where, self.exception),
            call(self.where_2, self.exception_2)
        ]
        EmergencyLogger.emergency_log.assert_has_calls(expected_calls_emergency_log)
        expected_calls_log = [
            call(40, (self.where, self.exception), extra={"turn": "unknown"}),
            call(40, (self.where_2, self.exception_2), extra={"turn": "unknown"})
        ]
        EmergencyLogger.runtime_logger.log.assert_has_calls(expected_calls_log)

    def test_empty_queue(self):

       pass

    def test_fallback(self):

        pass

    def test_flag_is_running_False(self):

        pass

if __name__ == "__main__":

    unittest.main()