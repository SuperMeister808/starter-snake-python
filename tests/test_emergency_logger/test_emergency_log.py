
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger
from runtime_logger import RuntimeLogger

class TestEmergencyLog(unittest.TestCase):

    def setUp(self):
        
        EmergencyLogger.setup_runtime_logger("TestLogger", "test.log", False)
        
        self.mocks = {}
        self.patchers = [
            patch.object(EmergencyLogger, "create_message", return_value=lambda cls, where, exception: (where, exception)),
            patch.object(EmergencyLogger.runtime_logger, "log", return_value=lambda level, message, extra: (level, message, extra))
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

        self.start_patchers()

        where_expected = "anywhere"
        exception_expected = "Testing..."

        log = EmergencyLogger.emergency_log(where_expected, exception_expected)

        level , message , extra = log
        turn = extra ["turn"]
        where_result , exception_result = message

        default_level = 40
        default_turn = "unknown"

        self.assertEqual(level, default_level)
        self.assertEqual(turn, default_turn)
        self.assertEqual(where_result, where_expected)
        self.assertEqual(exception_result, exception_expected)

    def test_customized_message(self):

        pass

    def test_exception(self):

        pass

    def test_no_runtime_logger(self):

        pass

if __name__ == "__main__":

    unittest.main()