
import unittest

from unittest.mock import patch , MagicMock

from move import Move

class TestNotItselfCollision(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.head = {"x": 2, "y": 2}
        self.body = []

    def assert_extract_keywords(self, mock):
        
        if not isinstance(mock, MagicMock):
            raise TypeError(f"Object: {mock} is not MagicMock()")
        
        mock.assert_called_once()

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

    def test_not_itself_collision_right(self):
        
        pass
    
    def test_not_itself_collision_left(self):
        
        pass
    
    def test_not_itself_collision_up(self):
        
        pass
    
    def test_not_itself_collision_down(self):
        
        pass
    
    def test_not_itself_collision_multiple_collisions(self):
        
        pass
    
    def test_body_parts_out_of_range(self):
        
        pass


if __name__ == "__main__":

    unittest.main()