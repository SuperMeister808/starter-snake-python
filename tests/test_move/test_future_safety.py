
import unittest
from unittest.mock import patch

from move import Move

class TestFutureSafety(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.addCleanup(self.stop_patchers)

    def setup_patchers(self, patcher_check_moves_return_value, patcher_is_move_safe_new):

        self.patchers = [self.create_patcher_check_moves(patcher_check_moves_return_value),
                         self.create_patcher_is_move_safe(patcher_is_move_safe_new)]
        
        self.start_patchers()

    def start_patchers(self):

        self.mocks = {}
        for patcher in self.patchers:
            
            mock = patcher.start()
            self.mocks[mock._name] = mock

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def check_calls(self):

        for name, mock in self.mocks.items():
            try:
                mock.assert_called()
            except AttributeError as e:
                pass
    
    def create_patcher_check_moves(self, return_value):

        patcher = patch.object(self.bot, "check_moves", return_value=return_value)
        return patcher
    
    def create_patcher_is_move_safe(self, new):

        patcher = patch.object(self.bot, "is_move_safe", new=new)
        return patcher
    
    def test_emergency_id(self):

        pass

    def test_is_safe_move_left(self):

        pass

    def test_no_safe_moves_left(self):

        pass

if __name__ == "__main__":
    unittest.main()

        




        

        