
import unittest
from unittest.mock import patch , MagicMock , call

from move import Move
from logger.emergency_logger import EmergencyLogger

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

        result = self.bot.select_move()

        self.mock_loger_queue.put.assert_called_with(("select_move", "Selected priority move", self.bot.turn_counter, 20))

        expected = ["left", "down"]
        next_move = result["move"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    @patch.object(bot, "is_move_safe", new={"left": {"is_safe": False}, "right": {"is_safe": True}, "up": {"is_safe": True}, "down": {"is_safe": False}})
    @patch.object(bot, "priority_moves", new=[])
    def test_random_choice_safe_moves(self):

        self.start_patchers()
        
        result = self.bot.select_move()

        self.mock_loger_queue.put.assert_called_once_with(("select_move",  "Selected safe move", self.bot.turn_counter, 20))

        next_move = result ["move"]
        expected = ["right", "up"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    @patch.object(bot, "is_move_safe", new={"left": {"is_safe": False}, "right": {"is_safe": False}, "up": {"is_safe": False}, "down": {"is_safe": False}})
    @patch.object(bot, "priority_moves", new=[])
    def test_random_choice_emergency_moves(self):

        self.start_patchers()

        result = self.bot.select_move()

        expected_calls = [
            call(("select_move", "Selected emergency move", self.bot.turn_counter, 40))
        ]
        
        self.mock_loger_queue.put.assert_has_calls(expected_calls)

        next_move = result ["move"]
        expected = ["left", "right", "up", "down"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    exc = RuntimeError("side effect")
    @patch.object(bot, "is_move_safe", new=MagicMock(wraps={"left": {"is_safe": False}, "right": {"is_safe": False}, "up": {"is_safe": False}, "down": {"is_safe": False}}))
    @patch.object(bot, "priority_moves", new=[])
    @patch("move.random.choice", side_effect=exc)
    def test_fallback(self, mock_random_choice):
        
        self.start_patchers()
        
        result = self.bot.select_move()
        
        self.mock_loger_queue.put.assert_called_once_with(("select_move", self.exc, self.bot.turn_counter, 40))
        mock_random_choice.assert_called_once()

        next_move = result ["move"]
        expected = ["left", "right", "down", "up"]
        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

if __name__ == "__main__":

    unittest.main()