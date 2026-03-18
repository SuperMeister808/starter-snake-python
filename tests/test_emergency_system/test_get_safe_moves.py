
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from logger.emergency_logger import EmergencyLogger

class TestGetSafeMoves(unittest.TestCase):
    
    bot = Move()
    head = {}
    game_state = {}
    body = []
    neck = {}
    my_length = 0

    def setUp(self):
        
        self.patchers = [
            patch.object(self.bot, "is_move_safe", new={"left": {"is_safe": True}, "right": {"is_safe": True}, "down": {"is_safe": True}, "up": {"is_safe": True}}),
            patch.object(EmergencyLogger.loger_queue, "put")
        ]

        self.mocks = {}
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):

            mock = patcher.start()
            try:
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    self.mocks [i] = mock
                else:
                    raise
    
    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for move , data in self.mocks.items():
            try:
                data.assert_called()
            except AttributeError:
                if not isinstance(data, MagicMock):
                    pass
                else:
                    raise
    
    @patch.object(bot.future_safety, "call_future_safety")
    def test_multiple_safe_moves(self, mock_call_future_safety):

        self.start_patchers()
        
        mock_call_future_safety.return_value = True
        result = self.bot.check_safe_moves(2, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

        for move , data in self.bot.is_move_safe.items():
            self.assertTrue(data["is_safe"])

    @patch.object(bot.future_safety, "call_future_safety")
    def test_no_safe_move(self, mock_call_future_safety):

        self.start_patchers()
        
        mock_call_future_safety.return_value = False
        result = self.bot.check_safe_moves(2, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)

        for move , data in self.bot.is_move_safe.items():
            self.assertFalse(data["is_safe"])

    @patch("move.deepcopy")
    def test_exception_is_move_safe(self, mock_deepcopy):

        self.start_patchers()
        
        exc = RuntimeError("side effect")
        mock_deepcopy.side_effect = exc

        self.bot.check_safe_moves(2, head=self.head, game_state=self.game_state, body=self.body, neck=self.neck, my_length=self.my_length)
        
        self.check_calls()
        mock_deepcopy.assert_called()
        
        expection = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        self.assertEqual(self.bot.is_move_safe, expection)

if __name__ == "__main__":

    unittest.main()