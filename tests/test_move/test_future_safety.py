
import unittest
from unittest.mock import patch

from move import Move

class TestFutureSafety(unittest.TestCase):

    def setup_patchers(self):

        self.patchers = [
            patch.object(Move, "check_moves")
        ]

        mocks = {}

        for patcher in self.patchers:
            mock = patcher.start()
            mocks[mock._name] = mock

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()
    
    def test_behauvior(self):

        pass

        