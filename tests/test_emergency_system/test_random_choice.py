
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

        memory_moves = []
        
        safe_moves = {"left": 0, "right": 2, "up": 1}

        result = self.bot.random_choice(game_state, safe_moves, memory_moves)

        self.mock_loger_queue.put.assert_called_once_with(("random_choice", "Cannot choose from an empty sequence", game_state))

        next_move = result ["move"]
        expected = ["left", "right", "up"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    def test_random_choice_emergency_moves(self):

        game_state = {"testing...": "testing..."}

        memory_moves = []

        safe_moves = MagicMock()
        safe_moves.items = MagicMock()
        safe_moves.items.side_effect = RuntimeError("side effect")

        result = self.bot.random_choice(game_state, safe_moves, memory_moves)

        expected_calls = [
            call(("random_choice", "Cannot choose from an empty sequence", game_state)),
            call(("random_choice", "side effect", game_state))
        ]
        
        self.mock_loger_queue.put.assert_has_calls(expected_calls)
        safe_moves.items.assert_called_once()

        next_move = result ["move"]
        expected = ["left", "right", "up", "down"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)

    @patch("move.random.choice")
    def test_move_down(self, mock_random):

        exc = RuntimeError("side effect")
        mock_random.side_effect = exc

        game_state = {"testing...": "testing..."}
        safe_moves = {"test0": "testing...", "test1": "testing..."}
        memory_moves = []
        
        result = self.bot.random_choice(game_state, safe_moves, memory_moves)
        next_move = result ["move"]
        expected = ["down"]

        self.assertEqual(result, {"move": "down"})
        self.assertIn(next_move, expected)

        keys = []
        for key , value in safe_moves.items():
            keys.append(key)

        expected_calls_random = [call(memory_moves),
                          call(keys),
                          call(["left", "right", "up", "down"])]
        
        mock_random.assert_has_calls(expected_calls_random)

        expected_calls_put = [
            call(("random_choice", "side effect", game_state)),
            call(("random_choice", "side effect", game_state)),
            call(("random_choice", "side effect", game_state))
        ]

        self.mock_loger_queue.put.assert_has_calls(expected_calls_put)



        

if __name__ == "__main__":

    unittest.main()