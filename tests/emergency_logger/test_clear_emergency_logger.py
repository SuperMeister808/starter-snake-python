
import unittest
from unittest.mock import patch

from emergency_logger import EmergencyLogger

from queue import Queue

class TestClearEmergencyLogger(unittest.TestCase):

    
    def test_clear_data(self):

        q = Queue()
        q.put("where", "exception", "game_state")
        
        with (
            patch.object(EmergencyLogger, "loger_queue", new=q),

        ):
        

    def test_already_cleared(self):

        pass