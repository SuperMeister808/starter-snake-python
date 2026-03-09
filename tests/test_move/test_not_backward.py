
import unittest
from unittest.mock import patch
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
    
    def test_neck_over_head(self):
        
        pass
    
    def test_neck_under_head(self):
        
        pass
    
    def test_neck_next_to_head_left(self):
        
        pass
    
    def test_neck_next_to_head_right(self):
        
        pass

if __name__ == "__main__":

    unittest.main()