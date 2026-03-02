
import unittest
from unittest.mock import patch
from future_safety import FutureSafety
from move import Move

class TestFutureSafetyFallback(unittest.TestCase):

    def setUp(self):
        self.bot = Move()
        
        self.patchers = []
        self.mocks = {}  

        self.addCleanup(self.stop_patchers)

    def setup_patchers(self, patcher_call_future_safety_result):
        patcher_call_future_safety = self.create_patcher_call_future_safety(patcher_call_future_safety_result)
        self.patchers.append(patcher_call_future_safety)
        self.start_patchers()

    def create_patcher_call_future_safety(self, result):

        patcher = patch.object(FutureSafety, "call_future_safety", return_value=result)
        return patcher
    
    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):
            try:
                mock = patcher.start()
                self.mocks [mock._mock_name] = mock
            except AttributeError:
                self.mocks [i] = mock

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            try:
                mock.assert_called_once()
            except AttributeError:
                pass
    
    def test_first_call_safe_move(self):

        self.setup_patchers(True)

        calls = 6
        game_state = "..."
        body = "..."
        move = "..."
        head = "..."
        my_length = "..."
        neck = "..."
        result = self.bot.fallback_future_safety(calls, game_state, body, move, head, my_length, neck)

        self.assertTrue(result)


    def test_last_call_safe_move(self):

        run_counter = 6
        
        while run_counter >= 0:
            if run_counter == 0:
                self.setup_patchers(True)
            else:
                self.setup_patchers(False)

            calls = 6
            game_state = "..."
            body = "..."
            move = "..."
            head = "..."
            my_length = "..."
            neck = "..."
            result = self.bot.fallback_future_safety(calls, game_state, body, move, head, my_length, neck)

            if run_counter == 0:
                self.assertTrue(result)
            else:
                self.assertFalse(result)
            run_counter = run_counter - 1

            self.stop_patchers()

    def test_no_safe_move(self):

        self.setup_patchers(False)

        calls = 6
        game_state = "..."
        body = "..."
        move = "..."
        head = "..."
        my_length = "..."
        neck = "..."
        result = self.bot.fallback_future_safety(calls, game_state, body, move, head, my_length, neck)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()