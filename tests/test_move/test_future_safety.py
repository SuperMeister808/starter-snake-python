
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestFutureSafety(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
        self.patchers = []

        self.head = {"x": 2, "y": 2}
        self.game_state = "Testing..."
        self.body = "Testing..."
        self.neck = "Testing..."

        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        self.mocks = {}
        for patcher in self.patchers:
            
            mock = patcher.start()
            try:                
                self.mocks[mock._mock_name] = mock
            except AttributeError as e:
                key = str(mock)
                self.mocks[key] = mock

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

        return_value = {"id": "Emergency!"}
        patcher_check_moves = self.create_patcher_check_moves(return_value)
        patcher_is_move_safe = self.create_patcher_is_move_safe(MagicMock())
        patcher_is_move_safe.items = MagicMock()
        
        self.patchers.append(patcher_check_moves)
        self.patchers.append(patcher_is_move_safe)
        self.start_patchers()

        relevant_position = []
        result_bool , result_list = self.bot.future_safety(self.head, self.game_state, self.body, self.neck, relevant_position=relevant_position)

        self.assertFalse(result_bool)
        self.assertEqual(result_list, [])

    def test_is_safe_move_left(self):

        pass

    def test_no_safe_moves_left(self):

        pass

if __name__ == "__main__":
    unittest.main()

        




        

        