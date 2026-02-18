
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
    
    def get_moves(self, head):

        left_move = {"x": head["x"] - 1, "y": head["y"]}
        right_move = {"x": head["x"] + 1, "y": head["y"]}
        down_move = {"x": head["x"], "y": head["y"] - 1}
        up_move = {"x": head["x"], "y": head["y"] + 1}

        return left_move , right_move , down_move , up_move
    
    def compare_lists(self, list0, list1):

        for e in list0:
            if e in list1:
                continue
            else:
                return False
            
        return True
    
    def test_emergency_id(self):

        return_value = {"id": "Emergency!"}
        patcher_check_moves = self.create_patcher_check_moves(return_value)
        patcher_is_move_safe = self.create_patcher_is_move_safe(MagicMock())
        patcher_is_move_safe.items = MagicMock()
        
        self.patchers.append(patcher_check_moves)
        self.patchers.append(patcher_is_move_safe)
        self.start_patchers()


        result_bool , result_list = self.bot.future_safety(self.head, self.game_state, self.body, self.neck)

        self.assertFalse(result_bool)
        self.assertEqual(result_list, [])

    def test_is_safe_move_left(self):

        patcher_check_moves = self.create_patcher_check_moves(None)
        patcher_is_move_safe = self.create_patcher_is_move_safe({"left": {"is_safe": True}, "right": {"is_safe": False}, "up": {"is_safe": False}, "down": {"is_safe": False}})
        self.patchers.append(patcher_check_moves)
        self.patchers.append(patcher_is_move_safe)

        self.start_patchers()

        result_bool , result_list = self.bot.future_safety(self.head, self.game_state, self.body, self.neck)
        
        self.assertTrue(result_bool)
        
        move_left , move_right , move_down , move_up = self.get_moves(self.head)
        expected_current_relevant_positions = [move_left, move_right, move_down, move_up]
        expected_relevant_positions = []
        for e in expected_current_relevant_positions:
            move_left , move_right , move_down , move_up = self.get_moves(e)
            possible_moves = [move_left, move_right, move_down, move_up]
            expected_relevant_positions.extend(possible_moves)
        self.compare_lists(result_list, expected_relevant_positions)



    def test_no_safe_moves_left(self):

        patcher_check_moves = self.create_patcher_check_moves(None)
        patcher_is_move_safe = self.create_patcher_is_move_safe({"left": {"is_safe": False}, "right": {"is_safe": False}, "up": {"is_safe": False}, "down": {"is_safe": False}})
        self.patchers.append(patcher_check_moves)
        self.patchers.append(patcher_is_move_safe)

        self.start_patchers()

        result_bool , result_list = self.bot.future_safety(self.head, self.game_state, self.body, self.neck)
        
        self.assertFalse(result_bool)
        self.assertEqual(result_list, [])

if __name__ == "__main__":
    unittest.main()

        




        

        