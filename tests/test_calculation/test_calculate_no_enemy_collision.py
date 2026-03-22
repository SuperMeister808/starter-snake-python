
import unittest
from unittest.mock import patch , MagicMock , ANY
from move import Move

# Tests that calculate_not_enemy_collision correctly marks unsafe moves and assigns priority.
class TestNoEnemyCollision(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.head = {"x": 2, "y": 2}
        self.game_state = {"you": {"id": "Super Meister"}}
        self.my_length = 0
        self.is_move_safe = {
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
        }

        patch.object(self.bot.keywords, "extract_keywords",
                     return_value=(self.head, self.game_state, self.my_length)).start()

        self.addCleanup(patch.stopall)

    def _call(self, opponents_positions):
        with patch.object(self.bot, "opponents_positions", new=opponents_positions):
            self.bot.calculate_not_enemy_collision(
                self.is_move_safe, head=self.head,
                game_state=self.game_state, my_length=self.my_length
            )
            self.bot.keywords.extract_keywords.assert_called_once_with(
                ANY, head=self.head, game_state=self.game_state, my_length=self.my_length
            )

    def _assert_moves(self, left_safe=True, left_priority=0, right_safe=True, right_priority=0,
                      down_safe=True, down_priority=0, up_safe=True, up_priority=0):
        self.assertEqual(self.is_move_safe["left"]["is_safe"],    left_safe)
        self.assertEqual(self.is_move_safe["left"]["priority"],   left_priority)
        self.assertEqual(self.is_move_safe["right"]["is_safe"],   right_safe)
        self.assertEqual(self.is_move_safe["right"]["priority"],  right_priority)
        self.assertEqual(self.is_move_safe["down"]["is_safe"],    down_safe)
        self.assertEqual(self.is_move_safe["down"]["priority"],   down_priority)
        self.assertEqual(self.is_move_safe["up"]["is_safe"],      up_safe)
        self.assertEqual(self.is_move_safe["up"]["priority"],     up_priority)

    def test_unsafe_moves(self):
        # verifies that moves overlapping unsafe positions are marked unsafe
        self._call({"...": {"unsafe": [{"x": 3, "y": 2}, {"x": 1, "y": 2}], "priority": []}})
        self._assert_moves(left_safe=False, right_safe=False)

    def test_priority_moves(self):
        # verifies that moves overlapping priority positions receive priority + 2
        self._call({"...": {"unsafe": [], "priority": [{"x": 2, "y": 3}, {"x": 3, "y": 2}]}})
        self._assert_moves(right_priority=2, up_priority=2)

    def test_unsafe_and_priority_moves(self):
        # verifies that unsafe and priority positions are applied simultaneously
        self._call({"...": {"unsafe": [{"x": 1, "y": 2}, {"x": 2, "y": 3}], "priority": [{"x": 2, "y": 3}, {"x": 3, "y": 2}]}})
        self._assert_moves(left_safe=False, right_priority=2, up_safe=False, up_priority=2)

    def test_no_unsafe_and_no_priority_moves(self):
        # verifies that all moves remain safe when opponents have no unsafe or priority positions
        self._call({"...": {"unsafe": [], "priority": []}})
        self._assert_moves()

    def test_multiple_snakes(self):
        # verifies that positions from multiple opponents are all applied
        self._call({
            "...":      {"unsafe": [{"x": 2, "y": 3}], "priority": [{"x": 3, "y": 2}]},
            "opponent": {"unsafe": [{"x": 1, "y": 2}], "priority": [{"x": 2, "y": 1}]},
        })
        self._assert_moves(left_safe=False, right_priority=2, down_priority=2, up_safe=False)

    def test_doubled_entry(self):
        # edge case — verifies that duplicate priority entries stack correctly
        self._call({"...": {"unsafe": [], "priority": [{"x": 1, "y": 2}, {"x": 1, "y": 2}]}})
        self._assert_moves(left_priority=2)
    
if __name__ == "__main__":

    unittest.main()