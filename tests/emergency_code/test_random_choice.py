
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestRandomChoice(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.patchers = [
            patch("move.random.choice")
        ]

        mocks = {}

        for patcher in self.patchers:

            mock = patcher.start()
            mocks ["mock_random"] = mock

        self.mock_random = mocks ["mock_random"]
        self.mock_random.return_value = "left"

        self.addCleanup(self.stop_patchers)

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