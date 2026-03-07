
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger

import queue

import threading

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", new=lambda where, exception, level, turn: (where, exception, level, turn)),
        ]

        self.start_patchers()
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:

            patcher.start()
    
    def stop_patchers(self):


        for patcher in self.patchers:

            patcher.stop()
    
    def test_coorect_queue(self):

        q = queue.Queue()
        q.put(("where", "exception", "game_state"))
        
        with patch.object(EmergencyLogger, "loger_queue", new=q):

            self.start_threading()
            self.join_threads()

            keys = ["where", "exception", "game_state"]
            for e in keys:
                assert any(any(e in str(value) for value in  (where, exception, game_state)) for where, exception, game_state in self.result)

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