
import unittest
from unittest.mock import patch , MagicMock , call

from move import Move
from logger.emergency_logger import EmergencyLogger

# Tests that select_move correctly selects from priority, safe and emergency moves.
class TestRandomChoice(unittest.TestCase):

    def setUp(self):
        self.bot = Move()

        self.mock_loger_queue = patch.object(EmergencyLogger, "loger_queue").start()
        self.mock_loger_queue.put = MagicMock()

        self.addCleanup(patch.stopall)

    def test_selects_priority_move(self):
        # verifies that a priority move is selected when available
        with patch.object(self.bot, "is_move_safe", new={
            "left":  {"is_safe": True},
            "right": {"is_safe": True},
            "up":    {"is_safe": True},
            "down":  {"is_safe": True},
        }):
            with patch.object(self.bot, "priority_moves", new=["left", "down"]):
                result = self.bot.select_move()

                self.mock_loger_queue.put.assert_called_with(
                    ("select_move", "Selected priority move", self.bot.turn_counter, 20)
                )
                self.assertIn(result["move"], ["left", "down"])

    def test_selects_safe_move(self):
        # verifies that a safe move is selected when no priority moves exist
        with patch.object(self.bot, "is_move_safe", new={
            "left":  {"is_safe": False},
            "right": {"is_safe": True},
            "up":    {"is_safe": True},
            "down":  {"is_safe": False},
        }):
            with patch.object(self.bot, "priority_moves", new=[]):
                result = self.bot.select_move()

                self.mock_loger_queue.put.assert_called_once_with(
                    ("select_move", "Selected safe move", self.bot.turn_counter, 20)
                )
                self.assertIn(result["move"], ["right", "up"])

    def test_selects_emergency_move(self):
        # verifies that an emergency move is selected when no safe moves exist
        with patch.object(self.bot, "is_move_safe", new={
            "left":  {"is_safe": False},
            "right": {"is_safe": False},
            "up":    {"is_safe": False},
            "down":  {"is_safe": False},
        }):
            with patch.object(self.bot, "priority_moves", new=[]):
                result = self.bot.select_move()

                self.mock_loger_queue.put.assert_called_with(
                    ("select_move", "Selected emergency move", self.bot.turn_counter, 40)
                )
                self.assertIn(result["move"], ["left", "right", "up", "down"])

    def test_fallback_on_exception(self):
        # verifies that an emergency move is returned when random.choice raises an exception
        exc = RuntimeError("side effect")
        with patch.object(self.bot, "is_move_safe", new=MagicMock(wraps={
            "left":  {"is_safe": False},
            "right": {"is_safe": False},
            "up":    {"is_safe": False},
            "down":  {"is_safe": False},
        })):
            with patch.object(self.bot, "priority_moves", new=[]):
                with patch("move.random.choice", side_effect=exc):
                    result = self.bot.select_move()

                    self.mock_loger_queue.put.assert_called_once_with(
                        ("select_move", exc, self.bot.turn_counter, 40)
                    )
                    self.assertIn(result["move"], ["down"])

if __name__ == "__main__":

    unittest.main()