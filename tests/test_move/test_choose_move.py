
import unittest

from unittest.mock import patch , MagicMock , ANY

from move import Move

class TestChooseMove(unittest.TestCase):

    bot = Move()
    neck = {}
    head = {}
    body = []
    my_length = 0
    game_state = {"you": {"head": head, "body": body, "length": my_length}}
    def setUp(self):
        
        #Needed to be patched individualy
            #patch.object(self.bot, "edit_body", return_value="body"),
            #patch.object(self.bot, "get_neck", return_value="neck"),
            #patch.object(self.bot, "check_moves"),
        
        self.patchers = [
            patch.object(self.bot, "reset_is_move_safe", name="reset_is_move_safe"),
            patch.object(self.bot.future_safety, "log_data", name="log_data"),
            patch.object(self.bot, "check_safe_moves", name="check_safe_moves"),
            patch.object(self.bot, "check_priority_moves", name="check_priority_moves"),
            patch.object(self.bot, "random_choice", return_value={"move": "left"}, name="random_choice")
        ]
        self.mocks = {}

        self.start_patchers()
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def general_call_assertion(self):

        for name , mock in self.mocks.items():
            if isinstance(mock, MagicMock):
                mock.assert_called()

    def assert_calls_no_args(self):

        
        mock_reset_is_move_safe = self.mocks.get("reset_is_move_safe", "unknown") 
        mock_check_priority_moves = self.mocks.get("check_priority_moves", "unknown") 
        mock_random_choice = self.mocks.get("random_choice", "unknown") 
        asserted_mocks = {"mock_reset_is_move_safe": mock_reset_is_move_safe, 
                              "mock_check_priority_moves": mock_check_priority_moves,
                              "mock_random_choice": mock_random_choice}


        for name, mock in asserted_mocks.items():
            if not isinstance(mock, MagicMock):
                raise TypeError(f"Objekt: {name} ist kein MagicMock")
            mock.assert_called()

    def assert_calls_log_data(self, call_count, head, body, neck, my_length):

        try:
            mock_log_data = self.mocks ["log_data"]
        except KeyError:
            raise KeyError("mock_log_data nicht vorhanden")
        if not isinstance(mock_log_data, MagicMock):
            raise TypeError("Objekt nicht als MagicMock vorhanden")
        self.assertEqual(mock_log_data.call_count, call_count)
        #asserts only the last log_data call of choose_move
        mock_log_data.assert_called_with("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})

    def assert_calls_check_safe_moves(self, head, game_state, body, neck, my_length):

        try:
            mock_check_safe_moves = self.mocks ["check_safe_moves"]
        except KeyError:
            raise KeyError("mock_check_safe_moves nicht vorhanden")
        if not isinstance(mock_check_safe_moves, MagicMock):
            raise TypeError("Objekt: mock_check_safe_moves nicht als MagicMock vorhanden")
        
        mock_check_safe_moves.assert_called_once_with(ANY, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)
    
    @patch.object(bot, "check_moves")
    @patch.object(bot, "get_neck", return_value=neck)
    @patch.object(bot, "edit_body", return_value=body)
    def test_no_fallback(self, mock_edit_body, mock_get_neck, mock_check_moves):

        result = self.bot.choose_move(self.game_state)
        self.assertEqual(result, {"move": "left"})

        self.assert_calls_no_args()
        self.assert_calls_log_data(5, self.head, self.body, self.neck, self.my_length)
        self.assert_calls_check_safe_moves(self.head, self.game_state, self.body, self.neck, self.my_length)

        mock_edit_body.assert_called_once_with(self.body)
        mock_get_neck.assert_called_once_with(body=self.body, game_state=self.game_state)
        mock_check_moves.assert_called_once_with(self.bot.is_move_safe, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

    @patch.object(bot, "get_neck", side_effect=RuntimeError("side_effect"))
    @patch.object(bot, "edit_body", side_effect=RuntimeError("side effect"))
    def test_fallback_extract_game_state(self, mock_edit_body, mock_get_neck):

        mock_reset_is_move_safe = self.mocks.get("reset_is_move_safe", "unknown")
        mock_log_data = self.mocks.get("log_data", "unknown")
        mocks_to_assert = {"mock_reset_is_move_safe": mock_reset_is_move_safe, "mock_log_data": mock_log_data}
        for name , mock in mocks_to_assert.items():
            if not isinstance(mock, MagicMock):
                raise TypeError(f"Objekt: {name} nicht als MagicMock vorhanden")

        with self.assertRaises(RuntimeError):
            result = self.bot.choose_move(self.game_state)

        mock_reset_is_move_safe.assert_called_once()
        mock_log_data.assert_called_once_with("choose_move", {"game_state": self.game_state})
        mock_edit_body.assert_called_once_with(self.body)
        mock_get_neck.assert_not_called()

    def test_fallback_get_neck(self):

        pass

    def test_fallback_check_moves(self):

        pass




if __name__ == "__main__":

    unittest.main()

