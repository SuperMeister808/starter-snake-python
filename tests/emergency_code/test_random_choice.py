
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestRandomChoice(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()



    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()
    
    def test_random_choice_memory_moves(self):

        game_state = {"testing...": "testing..."}

        memory_moves = ["left", "up"]
        safe_moves = ["left", "right", "up"]

        result = self.bot.random_choice(game_state, memory_moves, safe_moves)

        expected = ["left", "up"]
        next_move = result["move"]

        self.assertEqual(result, {"move": next_move})
        self.assertIn(next_move, expected)
        


    def test_random_choice_safe_moves(self):

        pass

    def test_random_choice_emergency_moves(self):

        pass

    def test_move_down(self):

        pass

if __name__ == "__main__":

    unittest.main()