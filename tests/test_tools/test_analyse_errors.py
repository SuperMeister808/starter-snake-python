from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY
from unittest import main
from tools.log_analyzer import LogAnalyzer
class TestAnalyseErrors(TestCase):

    log_analyzer = LogAnalyzer()
    def setUp(self):
        
        self.patchers = [
            patch.object(self.log_analyzer, "output_handler", side_effect=lambda output_format, output: output, name="mock_output_handler")
        ]
        self.mocks = {}

        self.start_patchers()
        self.addCleanup(self.stop_patchers)
    
    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def test_only_allowed_errors(self):

        pass

    def test_unallowed_errors(self):

        pass

    def test_validation_failed(self):

        pass

    def test_unallowed_output_format(self):

        pass