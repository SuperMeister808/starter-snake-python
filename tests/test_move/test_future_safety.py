
import unittest
from unittest.mock import patch , MagicMock

from move import Move
from future_safety import FutureSafety

class TestFutureSafety(unittest.TestCase):

    move = Move()
    future_safety = FutureSafety(move)
    def setUp(self):
        self.patchers = []

    def test_one_safe_move_left(self):

        pass

    def test_multiple_safe_moves_left(self):

        pass

    def test_node_ids_is_not_default(self):

        pass
        

if __name__ == "__main__":
    unittest.main()

        




        

        