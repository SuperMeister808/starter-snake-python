
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

        pass

    def test_random_choice_safe_moves(self):

        pass

    def test_random_choice_emergency_moves(self):

        pass

    def test_move_down(self):

        pass