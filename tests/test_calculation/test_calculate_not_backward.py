
import unittest
from unittest.mock import patch , MagicMock
from move import Move

# Tests that calculate_not_backward correctly marks the backward move as unsafe.
class TestNotBackward(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.head = {}
        self.neck = {}
        self.is_move_safe = {
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
        }

    def _call(self, head, neck):
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(head, neck)) as mock:
            self.bot.calculate_not_backward(self.is_move_safe, head=self.head, neck=self.neck)
            mock.assert_called_once_with(["head", "neck"], head={}, neck={})

    def _assert_safe(self, left=True, right=True, up=True, down=True):
        self.assertEqual(self.is_move_safe["left"]["is_safe"],  left)
        self.assertEqual(self.is_move_safe["right"]["is_safe"], right)
        self.assertEqual(self.is_move_safe["up"]["is_safe"],    up)
        self.assertEqual(self.is_move_safe["down"]["is_safe"],  down)

    def test_neck_above_head(self):
        # verifies that up is marked unsafe when neck is above the head
        self._call({"x": 2, "y": 2}, {"x": 2, "y": 3})
        self._assert_safe(up=False)

    def test_neck_below_head(self):
        # verifies that down is marked unsafe when neck is below the head
        self._call({"x": 2, "y": 2}, {"x": 2, "y": 1})
        self._assert_safe(down=False)

    def test_neck_left_of_head(self):
        # verifies that left is marked unsafe when neck is to the left of the head
        self._call({"x": 2, "y": 2}, {"x": 1, "y": 2})
        self._assert_safe(left=False)

    def test_neck_right_of_head(self):
        # verifies that right is marked unsafe when neck is to the right of the head
        self._call({"x": 2, "y": 2}, {"x": 3, "y": 2})
        self._assert_safe(right=False)

if __name__ == "__main__":

    unittest.main()