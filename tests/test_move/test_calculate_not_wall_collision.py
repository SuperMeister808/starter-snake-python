
import unittest
from unittest.mock import patch , ANY , MagicMock
from move import Move

# Tests that calculate_not_wall_collision correctly marks moves that would hit a wall as unsafe.
class TestCalculateNotWallCollision(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.head = {}
        self.game_state = {"board": {"width": 11, "height": 11}}
        self.is_move_safe = {
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
        }

    def _call(self, head):
        # patches extract_keywords to return controlled head and game_state values
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, self.game_state)) as mock:
            self.bot.calculate_not_wall_collision(self.is_move_safe, head=self.head, game_state=self.game_state)
            mock.assert_called_once_with(ANY, head=self.head, game_state=self.game_state)

    def _assert_safe(self, left=True, right=True, up=True, down=True):
        self.assertEqual(self.is_move_safe["left"]["is_safe"],  left)
        self.assertEqual(self.is_move_safe["right"]["is_safe"], right)
        self.assertEqual(self.is_move_safe["up"]["is_safe"],    up)
        self.assertEqual(self.is_move_safe["down"]["is_safe"],  down)

    def test_collision_right_wall(self):
        # verifies that right is marked unsafe when head is at the right wall
        self._call({"x": 10, "y": 2})
        self._assert_safe(right=False)

    def test_collision_left_wall(self):
        # verifies that left is marked unsafe when head is at the left wall
        self._call({"x": 0, "y": 2})
        self._assert_safe(left=False)

    def test_collision_down_wall(self):
        # verifies that down is marked unsafe when head is at the bottom wall
        self._call({"x": 2, "y": 0})
        self._assert_safe(down=False)

    def test_collision_up_wall(self):
        # verifies that up is marked unsafe when head is at the top wall
        self._call({"x": 2, "y": 10})
        self._assert_safe(up=False)

    def test_collision_negative_height(self):
        # edge case — verifies >= and <= logic when head is below zero
        self._call({"x": 2, "y": -1})
        self._assert_safe(down=False)

    def test_collision_corner(self):
        # verifies that two directions are marked unsafe when head is in a corner
        self._call({"x": 10, "y": 10})
        self._assert_safe(right=False, up=False)

if __name__ == "__main__":

    unittest.main()                                        