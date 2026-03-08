
import unittest

from unittest.mock import patch , MagicMock

from move import Move

class TestChooseMove(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        #Needed to be patched individualy
            #patch.object(self.bot, "edit_body", return_value="body"),
            #patch.object(self.bot, "get_neck", return_value="neck"),
            #patch.object(self.bot, "check_moves"),
        
        self.patchers = [
            patch.object(self.bot, "reset_is_move_safe", name="reset_is_move_safe"),
            patch.object(self.bot, "log_data", name="log_data"),
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

        mock_reset_is_move_safe = self.mocks ["reset_is_move_safe"]
        mock_check_priority_moves = self.mocks ["check_priority_moves"]
        mock_random_choice = self.mocks ["random_choice"]

        mock_reset_is_move_safe.assert_called_once()
        mock_check_priority_moves.assert_called_once()
        mock_random_choice.assert_called_once()

    

    
    @patch.object
    def test_no_fallback(self):

        pass

    def test_fallback_extract_game_state(self):#

        pass

    def test_fallback_get_neck(self):

        pass

    def test_fallback_check_moves(self):

        pass




if __name__ == "__main__":

    unittest.main()

