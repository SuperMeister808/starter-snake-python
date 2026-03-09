
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
        
        self.game_state = {"board": {"width": 11, "heigth": 11}}
        self.head = {}
    
    def test_not_wall_collision_width(self):
        
        pass
    
    def test_not_wall_collision_heigth(self):
        
        pass
    
    def test_not_wall_collision_corner(self):
        
        pass

if __name__ == "__main__":

    unittest.main()                                        