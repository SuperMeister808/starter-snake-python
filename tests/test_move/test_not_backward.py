
import unittest
from unittest.mock import patch , MagicMock
from move import Move

class TestNotBackward(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.head = {}
        self.neck = {}
    
    def assert_extract_keywords(self, mock):
        
        if not isinstance(mock, MagicMock):
            raise TypeError(f"Object: {mock} is not MagicMock()")
        
        mock.assert_called_once_with()

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
    
    def test_neck_over_head(self):
        
        head = {"x": 2, "y": 2}
        neck = {"x": 2, "y": 3}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, neck)) as mock_extract_keywords:
            self.bot.not_backward(self.is_move_safe, head=self.head, neck=self.neck)
            self.move_assertions(True, 0, True, 0, True, 0, False, 0)

            self.assert_extract_keywords(mock_extract_keywords)
    
    def test_neck_under_head(self):
        
        head = {"x": 2, "y": 2}
        neck = {"x": 2, "y": 1}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, neck)) as mock_extract_keywords:
            self.bot.not_backward(self.is_move_safe, head=self.head, neck=self.neck)
            self.move_assertions(True, 0, True, 0, False, 0, True, 0)

            self.assert_extract_keywords(mock_extract_keywords)
    
    
    def test_neck_next_to_head_left(self):
        
        head = {"x": 2, "y": 2}
        neck = {"x": 1, "y": 2}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, neck)) as mock_extract_keywords:
            self.bot.not_backward(self.is_move_safe, head=self.head, neck=self.neck)
            self.move_assertions(False, 0, True, 0, True, 0, True, 0)

            self.assert_extract_keywords(mock_extract_keywords)
    
    def test_neck_next_to_head_right(self):
        
        head = {"x": 2, "y": 2}
        neck = {"x": 3, "y": 2}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, neck)) as mock_extract_keywords:
            self.bot.not_backward(self.is_move_safe, head=self.head, neck=self.neck)
            self.move_assertions(True, 0, False, 0, True, 0, True, 0)

            self.assert_extract_keywords(mock_extract_keywords)

if __name__ == "__main__":

    unittest.main()