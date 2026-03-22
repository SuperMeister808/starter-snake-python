
import unittest
from unittest.mock import patch , MagicMock

from move import Move

# Tests that calculate_opponents_positions correctly maps opponent body parts to unsafe and priority positions.
class TestCalculateOpponentsPositions(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        self.maxDiff = None
        self.my_length = 4

    def _call(self, game_state, is_growing=False):
        with patch.object(self.bot, "calculate_is_growing", return_value=is_growing) as mock:
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=self.my_length)
            return mock

    def test_head_is_safe_opponent_smaller(self):
        # verifies that head moves are priority only when opponent is smaller than you
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"id": "opponent", "length": 3, "head": {"x": 2, "y": 2},
             "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}
        ]}}
        mock = self._call(game_state)

        expected = {"opponent": {
            "unsafe":   [{"x": 2, "y": 2}, {"x": 2, "y": 3}],
            "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
        }}
        self.assertEqual(self.bot.opponents_positions, expected)
        mock.assert_called_once()

    def test_head_moves_unsafe_opponent_larger(self):
        # verifies that head moves are added to unsafe when opponent is larger than you
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"id": "opponent", "length": 5, "head": {"x": 2, "y": 2},
             "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}
        ]}}
        mock = self._call(game_state)

        expected = {"opponent": {
            "unsafe":   [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
            "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
        }}
        self.assertEqual(self.bot.opponents_positions, expected)
        mock.assert_called_once()

    def test_tail_unsafe_when_growing(self):
        # verifies that tail is added to unsafe positions when snake is growing
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"id": "opponent", "length": 3, "head": {"x": 2, "y": 2},
             "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}
        ]}}
        mock = self._call(game_state, is_growing=True)

        expected = {"opponent": {
            "unsafe":   [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}],
            "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
        }}
        self.assertEqual(self.bot.opponents_positions, expected)
        mock.assert_called_once()

    def test_multiple_snakes(self):
        # verifies that positions are calculated correctly for multiple opponents
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"id": "opponent_0", "length": 3, "head": {"x": 2, "y": 2},
             "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]},
            {"id": "opponent_1", "length": 5, "head": {"x": 2, "y": 2},
             "body": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 4, "y": 2}]},
        ]}}
        mock = self._call(game_state)

        expected = {
            "opponent_0": {
                "unsafe":   [{"x": 2, "y": 2}, {"x": 2, "y": 3}],
                "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
            },
            "opponent_1": {
                "unsafe":   [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
                "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
            },
        }
        self.assertEqual(self.bot.opponents_positions, expected)
        mock.assert_called()

    def test_no_snakes(self):
        # verifies that opponents_positions is empty when there are no snakes
        game_state = {"you": {"id": "you"}, "board": {"snakes": []}}
        mock = self._call(game_state)

        self.assertEqual(self.bot.opponents_positions, {})
        mock.assert_not_called()

    def test_missing_body_parts_between_head_and_tail(self):
        # verifies that only head is unsafe when body has no middle parts
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"head": {"x": 2, "y": 2}, "id": "opponent", "length": 3,
             "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}]}
        ]}}
        mock = self._call(game_state)

        expected = {"opponent": {
            "unsafe":   [{"x": 2, "y": 2}],
            "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
        }}
        self.assertEqual(self.bot.opponents_positions, expected)
        mock.assert_called_once()

    def test_snake_wrong_type(self):
        # verifies that non-dict snake entries are skipped
        game_state = {"you": {"id": "you"}, "board": {"snakes": ["opponent"]}}
        mock = self._call(game_state)

        self.assertEqual(self.bot.opponents_positions, {})
        mock.assert_not_called()

    def test_snake_missing_required_keys(self):
        # verifies that snakes missing required keys are skipped
        game_state = {"you": {"id": "you"}, "board": {"snakes": {"id": "opponent", "head": {"x": 2, "y": 2}, "length": 3}}}
        mock = self._call(game_state)

        self.assertEqual(self.bot.opponents_positions, {})
        mock.assert_not_called()

    def test_opponent_id_equals_you_id(self):
        # verifies that the player's own snake is skipped
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"id": "you", "head": {"x": 2, "y": 2}, "length": 3, "body": [{"x": 2, "y": 2}]}
        ]}}
        mock = self._call(game_state, is_growing=True)

        self.assertEqual(self.bot.opponents_positions, {})
        mock.assert_not_called()

    def test_only_head(self):
        # edge case — verifies that a snake with only a head is handled correctly
        game_state = {"you": {"id": "you"}, "board": {"snakes": [
            {"id": "opponent", "head": {"x": 2, "y": 2}, "length": 3, "body": [{"x": 2, "y": 2}]}
        ]}}
        mock = self._call(game_state, is_growing=True)

        expected = {"opponent": {
            "unsafe":   [{"x": 2, "y": 2}],
            "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}],
        }}
        self.assertEqual(self.bot.opponents_positions, expected)
        mock.assert_not_called()

if __name__ == "__main__":
    unittest.main()