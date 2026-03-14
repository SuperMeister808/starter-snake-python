from unittest import TestCase
from unittest.mock import patch, MagicMock , ANY
from unittest import main
from tools.log_analyzer import LogAnalyzer
class TestReadLog(TestCase):

    log_analyzer = LogAnalyzer()
    def setUp(self):
        self.patchers = [
            patch.object(self.log_analyzer, "create_contents")
        ]
        self.mocks = {}

        self.start_patchers()
        self.addCleanup(self.stop_patcherss)

    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patcherss(self):
        for pacher in self.patchers:
            pacher.stop()
    
    def test_read_log_default_args(self):
        
        pass

    def test_read_log_custom_args(self):

        pass

    def test_read_log_unsupported_file_handler(self):

        pass