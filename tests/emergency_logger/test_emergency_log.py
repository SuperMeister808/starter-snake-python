
import unittest
from unittest.mock import patch , mock_open

from emergency_logger import EmergencyLogger

class TestEmergencyLog(unittest.TestCase):

    def setUp(self):
        
        self.m = mock_open()
        
        self.patchers = [
            patch("builtins.open", self.m)
        ]

        self.mocks = {}
        
        for  patcher in self.patchers:

            mock = patcher.start()

            self.mocks [mock._mock_name] = mock

        self.addCleanup(self.stop_patchers)

    def stop_patchers(self):

        for patcher in self.patchers:

            patcher.stop()

    def check_calls(self):

        for name, mock in self.mocks.items():

            mock.assert_called_once()
    
    def test_correct_arguments(self):

        game_state = {"turn": 1}

        exception = "Testing..."

        where = "test_correct_arguments"

        EmergencyLogger.emergency_log(where, exception, game_state)
        
        self.check_calls()

        calls = [call.args[0] for call in self.m().write.call_args_list]

        list = [f"[{game_state["turn"]}]", exception, where]
        
        for e in list:

            assert any(e in call for call in calls)

    def test_unknown_turn(self):

        game_state = {}

        exception = "Testing..."

        where = "test_correct_arguments"

        EmergencyLogger.emergency_log(where, exception, game_state)
        
        self.check_calls()

        calls = [call.args[0] for call in self.m().write.call_args_list]

        list = [f"[unknown]", exception, where]
        
        for e in list:

            assert any(e in call for call in calls)

    def test_type_error(self):

        game_state = "turn: 1"

        exception = "Testing..."

        where = "test_correct_arguments"

        EmergencyLogger.emergency_log(where, exception, game_state)
        
        self.check_calls()

        calls = [call.args[0] for call in self.m().write.call_args_list]

        list = [f"[unknown]", exception, where]
        
        for e in list:

            assert any(e in call for call in calls)



if __name__ == "__main__":

    unittest.main()