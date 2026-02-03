
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from emergency_logger import EmergencyLogger

class TestRandomChoice(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.patchers = [
            patch.object(EmergencyLogger, "loger_queue")
        ]

        mocks = {}

        for patcher in self.patchers:

            mock = patcher.start()
            mocks ["mock_loger_queue"] = mock

        self.mock_loger_queue = mocks ["mock_loger_queue"]
        self.mock_loger_queue.put = MagicMock()
        
        self.addCleanup(self.stop_patchers)

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()
    
    def test_random_choice_memory_moves(self):

        game_state = {"testing...": "testing..."}

        memory_moves = ["left", "up"]
        safe_moves = ["left", "right", "up"]

        result = self.bot.random_choice(game_state, safe_moves, memory_moves)
        self.mock_loger_queue.put.assert_not_called()

        expected = ["left", "up"]
        next_move = result["move"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    def test_random_choice_safe_moves(self):

        game_state = {"testing...": "testing..."}

        memory_moves = MagicMock()
        exc = RuntimeError("side effect")
        memory_moves.side_effect = exc
        
        safe_moves = ["left", "right", "up"]

        result = self.bot.random_choice(game_state, safe_moves, memory_moves)

        self.mock_loger_queue.put.assert_called_once_with("random choice", "side effect", game_state)

        next_move = result ["move"]
        expected = ["left", "right", "up"]

        self.assertEqual({"move": next_move})
        self.assertIn(next_move, expected)

    def test_random_choice_emergency_moves(self):

        pass

    def test_move_down(self):

        pass

if __name__ == "__main__":

    unittest.main()