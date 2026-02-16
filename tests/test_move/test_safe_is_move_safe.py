
import unittest
from unittest.mock import patch

from move import Move

class TestSafeIsMoveSafe(unittest.TestCase):

    def setUp(self):

        self.bot = Move()
    
    def setup_patchers(self, patcher_is_move_safe, patcher_is_move_safe_memory={}):

        self.patchers = []
        
        patcher_is_move_safe = self.create_patcher_is_move_safe(patcher_is_move_safe)
        self.patchers.append(patcher_is_move_safe)
        
        patcher_is_move_safe_memory = self.create_patcher_is_move_safe_memory(patcher_is_move_safe_memory)
        self.patchers.append(patcher_is_move_safe_memory)

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
    
    def create_patcher_is_move_safe_memory(self, patcher={}):

        patcher = patch.object(self.bot, "is_move_safe_memory", new=patcher)
        return patcher

    def test_regular_dictionary(self):

        patcher_is_move_safe = {"left": {}, "right": {}, "up": {}, "down": {}}
        patcher_is_move_safe_memory = {}
        self.setup_patchers(patcher_is_move_safe, patcher_is_move_safe_memory)

        self.start_patchers()

        self.bot.safe_is_move_safe()
        expected_is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        expected_is_move_safe_memory = {"left": {}, "right": {}, "up": {}, "down": {}}

        for i, patcher in enumerate(self.patchers):
            if i == 0:
                self.assertEqual(self.bot.is_move_safe, expected_is_move_safe)
            if i == 1:
                self.assertEqual(self.bot.is_move_safe_memory, expected_is_move_safe_memory)

        self.stop_patchers()

    def test_irregular_datatype(self):

        patcher_is_move_safe = ["left", "right", "up", "down"]
        patcher_is_move_safe_memory = []
        self.setup_patchers(patcher_is_move_safe, patcher_is_move_safe_memory)

        self.start_patchers()

        self.bot.safe_is_move_safe()
        expected_is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        expected_is_move_safe_memory = ["left", "right", "up", "down"]

        for i, patcher in enumerate(self.patchers):
            if i == 0:
                self.assertEqual(self.bot.is_move_safe, expected_is_move_safe)
            if i == 1:
                self.assertEqual(self.bot.is_move_safe_memory, expected_is_move_safe_memory)

        self.stop_patchers()

if __name__ == "__main__":
    unittest.main()