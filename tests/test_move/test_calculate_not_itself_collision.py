
import unittest

from unittest.mock import patch , MagicMock , ANY

from move import Move

# Tests that calculate_not_itself_collision correctly marks moves that collide with the snake's own body as unsafe.
class TestCalculateNotItselfCollision(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.head = {"x": 2, "y": 2}
        self.body = []
        self.is_move_safe = {
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
        }

    def _call(self, body):
        # patches extract_keywords to return controlled head and body values
        with patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, body)) as mock:
            self.bot.calculate_not_itself_collision(self.is_move_safe, head=self.head, body=self.body)
            mock.assert_called_once_with(ANY, head=self.head, body=self.body)

    def _assert_safe(self, left=True, right=True, up=True, down=True):
        self.assertEqual(self.is_move_safe["left"]["is_safe"],  left)
        self.assertEqual(self.is_move_safe["right"]["is_safe"], right)
        self.assertEqual(self.is_move_safe["up"]["is_safe"],    up)
        self.assertEqual(self.is_move_safe["down"]["is_safe"],  down)

    def test_head_is_not_iterated(self):
        # verifies that the head (body[0]) is skipped and no moves are marked unsafe
        self._call([{"x": 3, "y": 2}])
        self._assert_safe()

    def test_collision_right(self):
        # verifies that right is marked unsafe when body part is to the right
        self._call([self.head, {"x": 3, "y": 2}])
        self._assert_safe(right=False)

    def test_collision_left(self):
        # verifies that left is marked unsafe when body part is to the left
        self._call([self.head, {"x": 1, "y": 2}])
        self._assert_safe(left=False)

    def test_collision_up(self):
        # verifies that up is marked unsafe when body part is above
        self._call([self.head, {"x": 2, "y": 3}])
        self._assert_safe(up=False)

    def test_collision_down(self):
        # verifies that down is marked unsafe when body part is below
        self._call([self.head, {"x": 2, "y": 1}])
        self._assert_safe(down=False)

    def test_multiple_collisions(self):
        # verifies that multiple body parts mark multiple directions as unsafe
        self._call([self.head, {"x": 2, "y": 1}, {"x": 1, "y": 2}, {"x": 2, "y": 3}])
        self._assert_safe(left=False, up=False, down=False)

    def test_body_parts_out_of_range(self):
        # verifies that body parts not adjacent to the head do not affect safe moves
        self._call([self.head, {"x": 2, "y": 1}, {"x": 3, "y": 1}, {"x": 3, "y": 2}])
        self._assert_safe(right=False, down=False)

if __name__ == "__main__":

    unittest.main()