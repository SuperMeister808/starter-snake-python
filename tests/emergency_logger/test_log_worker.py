
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger

import queue

class TestLogWorker(unittest.TestCase):

    def setUp(self):
        
        self.patchers = [
            patch.object(EmergencyLogger, "emergency_log", lambda where, exception, game_state: f"{where}, {exception}, {game_state}"),
        ]

        self.mocks = {}
        
        for  patcher in self.patchers:

            mock = patcher.start()

            self.mocks [mock._mock_name] = mock

        self.addCleanup(self.stop_patchers)

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for name, mock in self.mocks.items():

            mock.assert_called_once()
    
    def test_coorect_queue(self):

        q = queue.Queue()
        q.put(("where", "exception", "game_state"))
        
        log_worker = EmergencyLogger.log_worker
        
        with patch.object(EmergencyLogger.loger_queue, q):
            with patch.object(EmergencyLogger.log_worker, lambda _: )

        EmergencyLogger.is_running = True
        EmergencyLogger.log_worker()

        if EmergencyLogger.loger_queue

    def test_correct_queuemultiple_elements(self):

        pass

    def test_less_values(self):

        pass

    def test_less_values_multiple_elements(self):

        pass

    def test_too_many_values(self):

        pass

    def test_too_many_values_multiple_elements(self):

        pass

    def test_wrong_data_type(self):

        pass

    def test_wrong_data_type_multiple_values(self):

        pass

    def test_empty_queue(self):

        pass