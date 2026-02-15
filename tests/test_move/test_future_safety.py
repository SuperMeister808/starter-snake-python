
import unittest
from unittest.mock import patch

from move import Move

class TestFutureSafety(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()
    
    def setup_patchers(self):

        self.patchers = [
            patch.object(self.bot, "check_moves", return_value=None)
        ]
        self.patcher_is_move_safe = patch.object(self.bot, "is_move_safe", new={"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}})

        self.mocks = {}

        for patcher in self.patchers:
            mock = patcher.start()
            self.mocks[mock._name] = mock
        self.patcher_is_move_safe.start()

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()
        self.patcher_is_move_safe.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            self.assertEqual(mock.call_count, 2)
    
    def test_behauvior(self):

        self.setup_patchers()
        
        game_state = {"you": {"body": [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}], "head": {"x": 1, "y": 1}}}
        move = "left"

        result = self.bot.call_future_safety(move, game_state)

        self.check_calls()
        self.assertEqual(result, True)

if __name__ == "__main__":
    unittest.main()

        




        

        