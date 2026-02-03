
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger
from move import Move

class TestChooseMove(unittest.TestCase):

    def setUp(self):
        
        self.patchers = [
            patch.object(EmergencyLogger, "loger_queue")
        ]

        self.mocks = {}
        
        for patcher in self.patchers:

            mock = patcher.start()
            self.mocks ["EmergencyLogger.loger_queue"] = mock

        mocked_loger_queue = self.mocks ["EmergencyLogger.loger_queue"]
        mocked_loger_queue.put = MagicMock()

        self.addCleanup(self.stop_patchers)

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()
    
    @patch.object(Move, "reset_is_move_safe")
    def test_reset_is_move_safe(self, mock_reset):

        mock_reset.side_effect = RuntimeError("side effect")

        bot = Move()

        bot.choose_move

    def test_not_backward(self):

        pass

    def test_not_wall_collision(self):

        pass

    def test_not_itself_collision(self):

        pass

    def test_not_enemy_collision(self):

        pass

    def test_calculate_food(self):

        pass

    def test_safe_moves(self):

        pass

    def test_priority_moves(self):

        pass

    def test_random_choice_priority_moves(self):

        pass

    def test_random_choice_safe_moves(self):

        pass