from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , call
from unittest import main
from tools.log_analyzer import LogAnalyzer
class TestAnalyseErrors(TestCase):

    log_analyzer = LogAnalyzer()
    def setUp(self):
        
        self.capture_output = []
        
        self.patchers = [patch.object(self.log_analyzer, "output_handler", side_effect=self.fake_output_handler, name="mock_output_handler"),
                         patch.object(self.log_analyzer, "validate_level", wraps=self.log_analyzer.validate_level, name="mock_validate_level"),
                         patch.object(self.log_analyzer, "validate_log", wraps=self.log_analyzer.validate_log, name="mock_validate_log")]
        self.mocks = {}

        self.start_patchers()
        #LIFO
        self.addCleanup(self.reset_capture_output)
        self.addCleanup(self.stop_patchers)
    
    def fake_output_handler(self, output_format, output):
        self.capture_output.append(output)

    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def find_mocks(self, mock_names):
        found_mocks = []
        for name in mock_names:
            mock = self.mocks.get(name, "unknown")
            found_mocks.append(mock)

        return found_mocks
    
    def reset_capture_output(self):

        self.capture_output = []

    new_contents = [{"line_number": 0, "level": "ERROR", "turn": 0, "log": "random_choice: Choosed emergency move"},
                    {"line_number": 1, "level": "INFO", "turn": 0, "log": "random_choice: Success!"}]
    @patch.object(log_analyzer, "contents", new=new_contents)
    def test_only_allowed_errors(self):

        output_format = "console"
        result = self.log_analyzer.analyse_errors(output_format)
        expected_outputs = ["Analyse_errors complete!"]
        self.assertEqual(self.capture_output, expected_outputs)

        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_level", "mock_validate_log"]
        mock_output_handler , mock_validate_level , mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        mock_output_handler.assert_called_once_with(output_format, ANY)
        self.assertEqual(mock_validate_level.call_count, 2)
        self.assertEqual(mock_validate_log.call_count, 2)

    new_contents = [{"line_number": 1, "level": "ERROR", "turn": 0, "log": "random_choice: Failed!"},
                    {"line_number": 0, "level": "INFO", "turn": 0, "log": "random_choice: Success!"}]
    @patch.object(log_analyzer, "contents", new=new_contents)
    def test_unallowed_errors(self):

        output_format = "console"
        result = self.log_analyzer.analyse_errors(output_format)
        expected_outputs = [{"line_number": 1, "level": "ERROR", "log": "random_choice: Failed!"}, "Analyse_errors complete!"]
        self.assertEqual(self.capture_output, expected_outputs)

        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_level", "mock_validate_log"]
        mock_output_handler , mock_validate_level , mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        expected_calls = [
            call(output_format, ANY),
            call(output_format, ANY)
        ]
        mock_output_handler.assert_has_calls(expected_calls)
        self.assertEqual(mock_output_handler.call_count, 2)
        self.assertEqual(mock_validate_level.call_count, 2)
        self.assertEqual(mock_validate_log.call_count, 2)

    def test_validation_failed(self):

        pass

    def test_unallowed_output_format(self):

        pass

if __name__ == "__main__":
    main()