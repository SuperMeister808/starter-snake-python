
import unittest
from unittest.mock import patch , MagicMock , call

from move import Move
from emergency_logger import EmergencyLogger

class TestRandomChoice(unittest.TestCase):

    bot = Move()
    def setUp(self):

        self.patchers = []
        self.mocks = {}
        
        self.patcher_loger_queue = patch.object(EmergencyLogger, "loger_queue")
        self.mock_loger_queue = None
        
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        self.start_patcher_loger_queue()
        self.setup_mock_loger_queue()
        
        for i , patcher in enumerate(self.patchers):
            mock = patcher.start()
            try:
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                if not isinstance(mock, MagicMock):
                    self.mocks [i] = mock
                else:
                    raise

    def start_patcher_loger_queue(self):

        mock = self.patcher_loger_queue.start()
        self.mocks ["mock_loger_queue"] = mock

    def setup_mock_loger_queue(self):

        self.mock_loger_queue = self.mocks ["mock_loger_queue"]
        self.mock_loger_queue.put = MagicMock()
    
    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for name, mock in self.mocks.items():
            mock.assert_called_once()
    
    @patch.object(bot, "is_move_safe", new={"left": {"is_safe": True}, "right": {"is_safe": True}, "up": {"is_safe": True}, "down": {"is_safe": True}})
    @patch.object(bot, "priority_moves", new=["left", "down"])
    def test_random_choice_memory_moves(self):
        
        self.start_patchers()

        result = self.bot.random_choice()

        self.mock_loger_queue.put.assert_called_with(("random_choice", "Successfully choosed priority move", self.bot.turn_counter, 20))

        expected = ["left", "down"]
        next_move = result["move"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    @patch.object(bot, "is_move_safe", new={"left": {"is_safe": False}, "right": {"is_safe": True}, "up": {"is_safe": True}, "down": {"is_safe": False}})
    @patch.object(bot, "priority_moves", new=[])
    def test_random_choice_safe_moves(self):

        self.start_patchers()
        
        result = self.bot.random_choice()

        self.mock_loger_queue.put.assert_called_once_with(("random_choice",  "Successfully choosed safe move", self.bot.turn_counter, 20))

        next_move = result ["move"]
        expected = ["right", "up"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    @patch.object(bot, "is_move_safe", new={"left": {"is_safe": False}, "right": {"is_safe": False}, "up": {"is_safe": False}, "down": {"is_safe": False}})
    @patch.object(bot, "priority_moves", new=[])
    def test_random_choice_emergency_moves(self):

        self.start_patchers()

        result = self.bot.random_choice()

        expected_calls = [
            call(("random_choice", "Choosed emergency move", self.bot.turn_counter, 40))
        ]
        
        self.mock_loger_queue.put.assert_has_calls(expected_calls)

        next_move = result ["move"]
        expected = ["left", "right", "up", "down"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    @patch.object(bot, "is_move_safe", new=MagicMock(wraps={"left": {"is_safe": False}, "right": {"is_safe": False}, "up": {"is_safe": False}, "down": {"is_safe": False}}))
    @patch.object(bot, "priority_moves", new=[])
    def test_fallback(self):
        
        self.bot.is_move_safe.items = MagicMock()
        exc = RuntimeError("side effect")
        self.bot.is_move_safe.items.side_effect = exc
        self.start_patchers()
        
        result = self.bot.random_choice()
        
        self.mock_loger_queue.put.assert_called_once_with(("random_choice", "side effect", self.bot.turn_counter, 40))
        
        next_move = result ["move"]
        expected = ["left", "right", "down", "up"]
        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

        



        

if __name__ == "__main__":

    unittest.main()