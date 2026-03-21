
import unittest
from unittest.mock import patch , ANY , MagicMock
from move import Move

class TestCalculateNotWallCollision(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.mock_extract_keywords = None
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.game_state = {"board": {"width": 11, "height": 11}}
        self.head = {}

        self.addCleanup(self.assert_calls_extract_keywords)
    
    def assert_calls_extract_keywords(self):

        if not isinstance(self.mock_extract_keywords, MagicMock):

            raise TypeError("Object: self.mock_extract_keywords is not a MagicMock()")
        
        self.mock_extract_keywords.assert_called_once_with(ANY, head=self.head, game_state=self.game_state)
    
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
    
    def test_not_wall_collision_right(self):
        
        head = {"x": 10, "y": 2}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as self.mock_extract_keywords:

            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, False, 0, True, 0, True, 0)

    
    def test_not_wall_collision_left(self):

        head = {"x": 0, "y": 2}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as self.mock_extract_keywords:

            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(False, 0, True, 0, True, 0, True, 0)


            
    
    def test_not_wall_collision_down(self):
        
        head = {"x": 2, "y": 0}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as self.mock_extract_keywords:

            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, True, 0, False, 0, True, 0)

    def test_not_wall_collision_up(self):

        head = {"x": 2, "y": 10}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as self.mock_extract_keywords:

            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, True, 0, True, 0, False, 0)

    #Edge-Case
    #tests >= and <= logic
    def test_not_wall_collision_negative_height(self):

        head = {"x": 2, "y": -1}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as self.mock_extract_keywords:

            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, True, 0, False, 0, True, 0)
    
    def test_not_wall_collision_corner(self):
        
        head = {"x": 10, "y": 10}
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as self.mock_extract_keywords:

            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            self.move_assertions(True, 0, False, 0, True, 0, False, 0)

if __name__ == "__main__":

    unittest.main()                                        