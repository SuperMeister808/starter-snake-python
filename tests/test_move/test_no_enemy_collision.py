
import unittest
from unittest.mock import patch , MagicMock , ANY
from move import Move

class TestNoEnemyCollision(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.is_move_safe =  {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        self.head = {"x": 2, "y": 2}
        self.game_state = {"you": {"id": "Super Meister"}}
        self.patchers = [
            patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, self.game_state), name="mock_extract_keywords")
        ]
        self.mocks = {}

        self.start_patchers()
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):
        
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def general_call_assertion(self):
        
        for name, mock in self.mocks.items():
            if isinstance(mock, MagicMock):
              mock.assert_called()

    def assert_call_extract_keywords(self):
        
        mock_extract_keywords = self.mocks.get("mock_extract_keywords", "unknown")
        if not isinstance(mock_extract_keywords, MagicMock):
            raise TypeError("Object: mock_extract_keywords is not a MagicMock()")
        
        mock_extract_keywords.assert_called_once_with(ANY, head=self.head, game_state=self.game_state)
    
    def extract_moves(self):
        
        left = self.is_move_safe.get("left", "unknown")
        right = self.is_move_safe.get("right", "unknown")
        down = self.is_move_safe.get("down", "unknwon")
        up = self.is_move_safe.get("up", "unknwon")

        return left , right , down , up
    
    def move_assertions(self, left_safe, left_priority, right_safe, right_priority, down_safe, down_priority, up_safe, up_priority):
        
        left , right , down , up = self.extract_moves()
        self.assertEqual(left.get("is_safe", "unknown"), left_safe)
        self.assertEqual(right.get("is_safe", "unknown"), right_safe)
        self.assertEqual(down.get("is_safe", "unknown"), down_safe)
        self.assertEqual(up.get("is_safe", "unknown"), up_safe)
        self.assertEqual(left.get("priority", "unknown"), left_priority)
        self.assertEqual(right.get("priority", "unknown"), right_priority)
        self.assertEqual(down.get("priority", "unknown"), down_priority)
        self.assertEqual(up.get("priority", "unknown"), up_priority)

    def test_unsafe_moves(self):
        
        new_opponents_positions = {"...": {"unsafe": [{"x": 3, "y": 2}, {"x": 1, "y": 2}], "priority": []}}
        with patch.object(self.bot, "opponents_positions", new=new_opponents_positions):
            self.bot.not_enemy_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(False, 0, False, 0, True, 0, True, 0)

            self.assert_call_extract_keywords()

    
    def test_priority_moves(self):
        
        new_opponents_positions = {"...": {"unsafe": [], "priority": [{"x": 2, "y": 3}, {"x": 3, "y": 2}]}}
        with patch.object(self.bot, "opponents_positions", new=new_opponents_positions):
            self.bot.not_enemy_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, True, 2, True, 0, True, 2)

            self.assert_call_extract_keywords()
    
    def test_unsafe_moves_and_priority_moves(self):
        
        new_opponents_positions = {"...": {"unsafe": [{"x": 1, "y": 2}, {"x": 2, "y": 3}], "priority": [{"x": 2, "y": 3}, {"x": 3, "y": 2}]}}
        with patch.object(self.bot, "opponents_positions", new=new_opponents_positions):
            self.bot.not_enemy_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(False, 0, True, 2, True, 0, False, 2)

            self.assert_call_extract_keywords()
    
    def test_no_unsafe_and_no_priority_moves(self):
        
        new_opponents_positions = {"...": {"unsafe": [], "priority": []}}
        with patch.object(self.bot, "opponents_positions", new=new_opponents_positions):
            self.bot.not_enemy_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, True, 0, True, 0, True, 0)

            self.assert_call_extract_keywords()
    
    
    def test_spread_entries_over_multiple_snakes(self):
        
        new_opponents_positions = {"...": {"unsafe": [{"x": 2, "y": 3}], "priority": [{"x": 3, "y": 2}]}, "opponent": {"unsafe": [{"x": 1, "y": 2}], "priority": [{"x": 2, "y": 1}]}}
        with patch.object(self.bot, "opponents_positions", new=new_opponents_positions):
            self.bot.not_enemy_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(False, 0, True, 2, True, 2, False, 0)

            self.assert_call_extract_keywords()
    
if __name__ == "__main__":

    unittest.main()