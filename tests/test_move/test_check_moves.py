
import unittest
from unittest.mock import patch

from move import Move

class TestCheckMoves(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.addCleanup(self.stop_patchers)



    def setup_patchers(self, patcher_emergency_system_return_value):

        self.patchers = []

        patcher_emergency_system = self.create_patcher_emergency_system(patcher_emergency_system_return_value)
        self.patchers.append(patcher_emergency_system)

        self.start_patchers()

    def start_patchers(self):

        self.mocks = {}

        for i, patcher in enumerate(self.patchers):
            mock = patcher.start()
            self.mocks[i] = mock



    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def create_patcher_emergency_system(self, patcher_emergency_system_return_value):

        patcher = patch.object(self.bot, "emergency_system", return_value=patcher_emergency_system_return_value)
        
        return patcher

    def test_call_emergency_system_no_return_value(self):

        pass

    def test_call_emergency_system_return_value(self):

        pass

    def test_call_emergency_system_return_value_during_iteration(self):

        pass