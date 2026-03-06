
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger

class TestEmergencyLog(unittest.TestCase):

    def setUp(self):
        
        self.patchers = [
            patch.object(EmergencyLogger, "create_message", return_value=lambda cls, where, exception: (where, exception)),
            patch.object(EmergencyLogger, "log", return_value=lambda level, message, extra: (level, message, extra))
        ]
    
    def test_default_message(self):

        pass

    def test_customized_message(self):

        pass

    def test_exception(self):

        pass

    def test_no_runtime_logger(self):

        pass