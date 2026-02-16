
import unittest
from unittest.mock import patch

from move import Move

class TestSafeIsMoveSafe(unittest.TestCase):

    def setup(self):

        self.bot = Move()
    
    def setup_patchers(self, patcher_is_move_safe):

        self.patchers = []
        
        patcher_is_move_safe = self.create_patcher_is_move_safe(patcher_is_move_safe)
        self.patchers.append(patcher_is_move_safe)

        return self.patchers
    
    def start_patchers(self):

        self.mocks = {}
        
        for i, patcher in enumerate(self.patchers):
            mock = patcher.start()
            self.mocks[i] = mock

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

        self.patchers.clear()
        self.mocks.clear()
    
    def create_patcher_is_move_safe(self, patcher):

        patcher_is_move_safe = patch.object(self.bot, "is_move_safe", new=patcher)
        return patcher_is_move_safe
    
    def test_regular_dictionary(self):

        patcher_is_move_safe = {"left": {}, "right": {}, "up": {}, "down": {}}
        self.setup_patchers(patcher_is_move_safe)

    def test_irregular_datatype(self):

        pass