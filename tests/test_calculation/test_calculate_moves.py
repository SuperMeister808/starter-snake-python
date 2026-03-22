
import unittest
from unittest.mock import patch , MagicMock

from move import Move

# Tests that check_moves correctly calls all calculation methods in order.
class TestCheckMoves(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.is_move_safe = {}
        self.head = {}
        self.game_state = {}
        self.body = []
        self.neck = {}
        self.my_length = 0

        self.mock_calculate_opponents_positions = patch.object(self.bot, "calculate_opponents_positions").start()
        self.mock_not_backward = patch.object(self.bot, "calculate_not_backward").start()
        patch.object(self.bot, "calculate_not_wall_collision").start()
        patch.object(self.bot, "calculate_not_itself_collision").start()
        patch.object(self.bot, "calculate_not_enemy_collision").start()
        patch.object(self.bot, "calculate_food").start()

        self.addCleanup(patch.stopall)

    def _expected_call(self):
        return dict(
            head=self.head, game_state=self.game_state,
            body=self.body, neck=self.neck, my_length=self.my_length
        )

    def test_correct_check_moves(self):
        # verifies that all calculation methods are called with the correct arguments
        self.bot.calculate_moves(self.is_move_safe, **self._expected_call())

        self.mock_calculate_opponents_positions.assert_called_with(self.is_move_safe, **self._expected_call())
        self.mock_not_backward.assert_called_with(self.is_move_safe, **self._expected_call())

    def test_runtime_error(self):
        # verifies that a RuntimeError in calculate_opponents_positions stops the pipeline
        self.mock_calculate_opponents_positions.side_effect = RuntimeError("side effect")

        with self.assertRaises(RuntimeError):
            self.bot.calculate_moves(self.is_move_safe, **self._expected_call())

        self.mock_calculate_opponents_positions.assert_called_with(self.is_move_safe, **self._expected_call())
        self.mock_not_backward.assert_not_called()

if __name__ == "__main__":
    unittest.main()