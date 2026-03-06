
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

class TestEmergencyLog(unittest.TestCase):

    def setUp(self):
        
        self.mocks = {}
        self.patchers = [
            patch.object(EmergencyLogger, "create_message", return_value=lambda cls, where, exception: (where, exception)),
            patch.object(EmergencyLogger, "log", return_value=lambda level, message, extra: (level, message, extra))
        ]

        self.addCleanup(self.stop_patchers)
    
    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):
            mock = patcher.start()
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

    def test_default_message(self):

        pass

    def test_customized_message(self):

        pass

    def test_exception(self):

        pass

    def test_no_runtime_logger(self):

        pass