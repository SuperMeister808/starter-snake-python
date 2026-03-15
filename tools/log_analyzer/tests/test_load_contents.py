from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
class TestLoadContents(TestCase):

    file = "..."
    level_index = "..."
    turn_index = "..."
    log_index = "..."
    log_analyzer = LogAnalyzer(file, level_index, turn_index, log_index)
    def setUp(self):
        
        self.mocks = {}
        self.patchers = [
            patch.object(self.log_analyzer, "read_log", name="mock_read_log")
        ]

        self.addCleanup(self.stop_patchers)

    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()
    
    def test_load_valide_contents(self):

        pass

    def test_load_invalid_contents(self):

        pass