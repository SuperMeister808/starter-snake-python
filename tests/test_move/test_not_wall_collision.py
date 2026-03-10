
import unittest
from unittest.mock import patch , ANY
from move import Move

class TestNotWallCollision(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.game_state = {"board": {"width": 11, "height": 11}}
    
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
    
    def test_not_wall_collision_width(self):
        
        head = {"x": 10, "y": 2}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as mock_extract_keywords:

            self.bot.not_wall_collision(self.is_move_safe, head=head, game_state=self.game_state)
            self.move_assertions(True, 0, False, 0, True, 0, True, 0)
    
    def test_not_wall_collision_heigth(self):
        
        pass
    
    def test_not_wall_collision_corner(self):
        
        pass

if __name__ == "__main__":

    unittest.main()                                        