
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

class TestGetPriorityMoves(unittest.TestCase):

    def setUp(self):
        
        self.patchers = [
            patch.object(EmergencyLogger, "loger_queue")
        ]

        mocks = {}
        
        for patcher in self.patchers:

            mock = patcher.start()
            mocks ["mock_loger_queue"] = mock

        self.mock_loger_queue = mocks ["mock_loger_queue"]
        self.mock_loger_queue.put = MagicMock()

        self.addCleanup(self.stop_patchers)
    
    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()
    
    def test_one_priority_move(self):

        pass

    def test_multiple_priority_moves(self):

        pass

    def test_exception(self):

        pass

if __name__ == "__main__":

    unittest.main()