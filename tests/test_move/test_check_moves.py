
import unittest
from unittest.mock import patch

from move import Move

class TestCheckMoves(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

        self.patchers = []
        self.mocks = {}

        self.head = "Testing..."
        self.game_state = "Testing..."
        self.body = "Testing..."
        self.neck = "Testing..."

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

    def check_calls(self, call_count):

        calls = [((self.game_state, self.bot.reset_is_move_safe), dict()),
                 ((self.game_state, self.bot.not_backward), dict(head=self.head, game_state=self.game_state, body=self.body, neck=self.neck)),
                 ((self.game_state, self.bot.not_wall_collision), dict(head=self.head, game_state=self.game_state, body=self.body, neck=self.neck)),
                 ((self.game_state, self.bot.not_itself_collision), dict(head=self.head, game_state=self.game_state, body=self.body, neck=self.neck)),
                 ((self.game_state, self.bot.not_enemy_collision), dict(head=self.head, game_state=self.game_state, body=self.body, neck=self.neck)),
                 ((self.game_state, self.bot.calculate_food), dict(head=self.head, game_state=self.game_state, body=self.body, neck=self.neck))]
        
        mock = self.mocks[0]
        
        assert any(c in calls for c in mock.call_args_list)

        self.assertEqual(mock.call_count, call_count)
    
    def test_call_emergency_system_no_return_value(self):

        patcher_emergency_system_return_value = None
        self.setup_patchers(patcher_emergency_system_return_value)
        
        self.bot.check_moves(self.head, self.game_state, self.body, self.neck)
        self.check_calls(6)

    def test_call_emergency_system_return_value(self):

        patcher_emergency_system_return_value = "Testing..."
        self.setup_patchers(patcher_emergency_system_return_value)

        self.bot.check_moves(self.head, self.game_state, self.body, self.neck)
        self.check_calls(1)

if __name__ == "__main__":
    unittest.main()