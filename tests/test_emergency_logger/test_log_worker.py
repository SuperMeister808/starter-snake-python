
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger

import queue

import threading

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        self.worker_thread = None
        self.flags = {"is_running": False, "worker_thread": None}

        self.result = []
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", new=self.fake_log),
            patch.object(EmergencyLogger, "flags", new=self.flags),
        ]

        self.start_patchers()
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:

            patcher.start()
    
    def stop_patchers(self):


        for patcher in self.patchers:

            patcher.stop()
    
    def start_threading(self):

        self.flags["is_running"] = True

        self.worker_thread = threading.Thread(target=EmergencyLogger.start_log_worker)
        self.flags["worker_thread"] = self.worker_thread

        self.worker_thread.start()
        

    def join_threads(self):

        self.flags["is_running"] = False
        self.worker_thread.join()

    
    def fake_log(self, where, exception, game_state):

        self.result.append((where, exception, game_state))
    
    def test_coorect_queue(self):

        q = queue.Queue()
        q.put(("where", "exception", "game_state"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            keys = ["where", "exception", "game_state"]
            for e in keys:
                assert any(any(e in str(value) for value in  (where, exception, game_state)) for where, exception, game_state in self.result)

    def test_correct_queue_multiple_elements(self):

        q = queue.Queue()
        q.put(("where", "exception", "game_state"))
        q.put(("test_correct_queue_multiple_elements", "Testing...", "turn: 1"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            keys = ["where", "exception", "game_state", "test_correct_queue_multiple_elements", "Testing...", "turn: 1"]
            for e in keys:
                assert any(any(e in str(value) for value in  (where, exception, game_state)) for where, exception, game_state in self.result)

    def test_less_values(self):

        EmergencyLogger.print_collector.clear_messages()
        
        q = queue.Queue()
        q.put(("where", "exception"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = "Not enough values:"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)

            EmergencyLogger.print_collector.clear_messages()


    def test_less_values_multiple_elements(self):

        EmergencyLogger.print_collector.clear_messages()
        
        q = queue.Queue()
        q.put(("where", "exception"))
        q.put(("where", "exception", "game_state"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = "Not enough values:"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)

            keys = ["where", "exception", "game_state"]
            for e in keys:
                assert any(any(e in str(value) for value in  (where, exception, game_state)) for where, exception, game_state in self.result)
            
            EmergencyLogger.print_collector.clear_messages()

    def test_too_many_values(self):

        EmergencyLogger.print_collector.clear_messages()
        
        q = queue.Queue()
        q.put(("where", "exception", "game_state", "extra"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = f"Too many values"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)
            
            EmergencyLogger.print_collector.clear_messages()

    def test_too_many_values_multiple_elements(self):

        EmergencyLogger.print_collector.clear_messages()
        
        q = queue.Queue()
        q.put(("where", "exception", "game_state"))
        q.put(("where", "exception", "game_state", "extra"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = f"Too many values"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)
            
            keys = ["where", "exception", "game_state"]
            for e in keys:
                assert any(any(e in str(value) for value in  (where, exception, game_state)) for where, exception, game_state in self.result)
            
            EmergencyLogger.print_collector.clear_messages()


    def test_wrong_data_type(self):

        EmergencyLogger.print_collector.clear_messages()
        
        q = queue.Queue()
        q.put("where, exception, game_state")
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = "Item is not a tuple or a list!"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)
            
            EmergencyLogger.print_collector.clear_messages()

    def test_wrong_data_type_multiple_values(self):

        EmergencyLogger.print_collector.clear_messages()
        
        q = queue.Queue()
        q.put(("where", "exception", "game_state"))
        q.put("where, exception, game_state")
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = "Item is not a tuple or a list!"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)
            
            keys = ["where", "exception", "game_state"]
            for e in keys:
                assert any(any(e in str(value) for value in  (where, exception, game_state)) for where, exception, game_state in self.result)
            
            EmergencyLogger.print_collector.clear_messages()

    def test_empty_queue(self):

        q = queue.Queue()

        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            expected = "logger queue is empty"
            
            assert any(expected in message for message in EmergencyLogger.print_collector.messages)
            
            EmergencyLogger.print_collector.clear_messages()

if __name__ == "__main__":

    unittest.main()