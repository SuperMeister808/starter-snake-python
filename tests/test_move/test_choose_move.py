
import unittest

from unittest.mock import patch , MagicMock , ANY , call

from move import Move

# Tests that choose_move correctly orchestrates the full pipeline and handles fallbacks.
class TestChooseMove(unittest.TestCase):

    bot = Move()
    def setUp(self):
        self.neck = {}
        self.head = {}
        self.body = []
        self.my_length = 0
        self.game_state = {"you": {"head": self.head, "body": self.body, "length": self.my_length}}
        self.EMERGENCY_MOVES = ["left", "right", "down", "up"]

        patch.object(self.bot, "reset_is_move_safe").start()
        patch.object(self.bot.future_safety, "log_data").start()
        patch.object(self.bot, "check_safe_moves").start()
        patch.object(self.bot, "check_priority_moves").start()
        patch.object(self.bot, "select_move", return_value={"move": "left"}).start()

        self.addCleanup(patch.stopall)

    def _kwargs(self):
        return dict(
            head=self.head, game_state=self.game_state,
            body=self.body, neck=self.neck, my_length=self.my_length
        )

    @patch.object(bot, "check_moves")
    @patch.object(bot.extract_data, "get_neck", return_value={})
    @patch.object(bot.extract_data, "edit_body", return_value=[])
    def test_no_fallback(self, mock_edit_body, mock_get_neck, mock_check_moves):
        # verifies the full pipeline runs correctly with no fallbacks
        result = self.bot.choose_move(self.game_state)

        self.assertEqual(result, {"move": "left"})
        self.bot.reset_is_move_safe.assert_called_once()
        self.bot.check_priority_moves.assert_called_once()
        self.bot.select_move.assert_called_once()
        self.bot.check_safe_moves.assert_called_once_with(ANY, **self._kwargs())
        mock_edit_body.assert_called_once_with(self.body)
        mock_get_neck.assert_called_once_with(body=self.body, game_state=self.game_state)
        mock_check_moves.assert_called_once_with(
            self.bot.is_move_safe, **self._kwargs()
        )

    @patch.object(bot.extract_data, "edit_body", side_effect=RuntimeError("side effect"))
    def test_fallback_extract_game_state(self, mock_edit_body):
        # verifies that RuntimeError is raised when game state extraction fails
        
        result = self.bot.choose_move(self.game_state)

        self.assertIn(result["move"], self.EMERGENCY_MOVES)
        self.bot.reset_is_move_safe.assert_called_once()
        expected_calls = [
            call('choose_move', {'game_state': {'you': {'head': {}, 'body': [], 'length': 0}}}),
        ]
        self.bot.future_safety.log_data.assert_has_calls(expected_calls)
        mock_edit_body.assert_called_once_with(self.body)

    @patch.object(bot, "check_moves", side_effect=RuntimeError("side effect"))
    @patch.object(bot.extract_data, "get_neck", side_effect=RuntimeError("side effect"))
    @patch.object(bot.extract_data, "edit_body", return_value=[])
    def test_fallback_get_neck(self, mock_edit_body, mock_get_neck, mock_check_moves):
        # verifies that an emergency move is returned when get_neck fails
        mock_get_neck.__name__ = "mock_get_neck"
        result = self.bot.choose_move(self.game_state)

        self.assertIn(result["move"], self.EMERGENCY_MOVES)
        self.bot.reset_is_move_safe.assert_called_once()
        mock_edit_body.assert_called_once_with(self.body)
        mock_get_neck.assert_called_once_with(body=self.body, game_state=self.game_state)
        mock_check_moves.assert_not_called()

    @patch.object(bot, "check_moves", side_effect=RuntimeError("side effect"))
    @patch.object(bot.extract_data, "get_neck", return_value={})
    @patch.object(bot.extract_data, "edit_body", return_value=[])
    def test_fallback_check_moves(self, mock_edit_body, mock_get_neck, mock_check_moves):
        # verifies that an emergency move is returned when check_moves fails
        mock_check_moves.__name__ = "mock_check_moves"
        result = self.bot.choose_move(self.game_state)

        self.assertIn(result["move"], self.EMERGENCY_MOVES)
        self.bot.reset_is_move_safe.assert_called_once()
        self.bot.check_safe_moves.assert_not_called()
        mock_edit_body.assert_called_once_with(self.body)
        mock_get_neck.assert_called_once_with(body=self.body, game_state=self.game_state)
        mock_check_moves.assert_called_once_with(
            self.bot.is_move_safe, **self._kwargs()
        )

if __name__ == "__main__":

    unittest.main()
