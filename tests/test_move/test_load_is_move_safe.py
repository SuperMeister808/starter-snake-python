
import unittest
from unittest.mock import patch

from move import Move

class TestLoadIsMoveSafe(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

    def setup_patchers(self, patcher_is_move_safe, patcher_is_move_safe_memory):

        self.patchers = []

        patcher_is_move_safe = self.create_patcher_is_move_safe(patcher_is_move_safe)
        self.patchers.append(patcher_is_move_safe)

        patcher_is_move_safe_memory = self.create_patcher_is_move_safe(patcher_is_move_safe_memory)
        self.patchers.append(patcher_is_move_safe_memory)

    def start_patchers(self):

        for patcher in self.patchers:
            patcher.start()

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def create_patcher_is_move_safe(self, patcher):

        patcher = patch.object(self.bot, "is_move_safe", new=patcher)
        return patcher
    
    def create_patcher_is_move_safe_memory(self, patcher):

        patcher = patch.object(self.bot, "is_move_safe_memory", new=patcher)
        return patcher

    
    def test_regular_datatype(self):

        patcher_is_move_safe = {"left": {}, "right": {}, "up": {}, "down": {}}
        patcher_is_move_safe_memory = {}
        self.setup_patchers(patcher_is_move_safe, patcher_is_move_safe_memory)
        
        self.start_patchers()
        




    def test_irreglular_datatype(self):

        pass