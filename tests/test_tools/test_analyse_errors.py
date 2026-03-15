from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , call
from unittest import main
from tools.log_analyzer import LogAnalyzer
import io
import tempfile
import os
class TestAnalyseErrors(TestCase):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"...")
        file = tmp.name  
    log_analyzer = LogAnalyzer(file)
    def setUp(self):
        
        self.capture_output = []
        
        self.patchers = [patch.object(self.log_analyzer, "output_handler", side_effect=self.fake_output_handler, name="mock_output_handler"),
                         patch.object(self.log_analyzer, "validate_level", wraps=self.log_analyzer.validate_level, name="mock_validate_level"),
                         patch.object(self.log_analyzer, "validate_log", wraps=self.log_analyzer.validate_log, name="mock_validate_log"),
                         patch.object(self.log_analyzer, "setup_logger")]
        self.mocks = {}

        self.start_patchers()
        #LIFO
        self.addCleanup(self.reset_capture_output)
        self.addCleanup(self.stop_patchers)
    
    
    def fake_output_handler(self, output_format, output):
        self.capture_output.append(output)

    def fake_validate_level(self, level):
        if level == "unknown":
            raise self.exc

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

        output_formats = ["console"]
        result = self.log_analyzer.analyse_errors(output_formats)
        expected_outputs = ["Analyse_errors complete!"]
        self.assertEqual(self.capture_output, expected_outputs)

        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_level", "mock_validate_log"]
        mock_output_handler , mock_validate_level , mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        mock_output_handler.assert_called_once_with(output_formats, ANY)
        self.assertEqual(mock_validate_level.call_count, 2)
        self.assertEqual(mock_validate_log.call_count, 2)

    new_contents = [{"line_number": 1, "level": "ERROR", "turn": 0, "log": "random_choice: Failed!"},
                    {"line_number": 0, "level": "INFO", "turn": 0, "log": "random_choice: Success!"}]
    @patch.object(log_analyzer, "contents", new=new_contents)
    def test_unallowed_errors(self):

        output_formats = ["console"]
        result = self.log_analyzer.analyse_errors(output_formats)
        expected_outputs = [{"line_number": 1, "level": 40, "log": "random_choice: Failed!", "turn": 0}, {"line_number": "unknown", "level": 20, "log": "Analyse errors completed!", "turn": "unknown"}]
        self.assertEqual(self.capture_output, expected_outputs)

        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_level", "mock_validate_log"]
        mock_output_handler , mock_validate_level , mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        expected_calls = [
            call(output_formats, ANY),
            call(output_formats, ANY)
        ]
        mock_output_handler.assert_has_calls(expected_calls)
        self.assertEqual(mock_output_handler.call_count, 2)
        self.assertEqual(mock_validate_level.call_count, 2)
        self.assertEqual(mock_validate_log.call_count, 2)

    new_contents = [{"line_number": 0, "level": "ERROR", "turn": 0, "log": "random_choice: Failed!"},
                    {"line_number": 1, "turn": 0, "log": "random_choice: Success!"}]
    exc = KeyError("side effect")
    @patch.object(log_analyzer, "contents", new=new_contents)
    @patch.object(log_analyzer, "validate_level", side_effect=exc)
    def test_validation_failed(self, mock_validate_level):

        output_formats = ["console"]
        result = self.log_analyzer.analyse_errors(output_formats)
        for output in self.capture_output:
                self.assertIsInstance(output, dict)
                line_number = output ["line_number"]
                level = output ["level"]
                turn = output ["turn"]
                log = output ["log"]
                line_numbers = [0, 1, "unknown"]
                self.assertIn(line_number, line_numbers)
                levels = [20, 40]
                self.assertIn(level, levels)
                self.assertIsInstance(turn, (int, str))
                if isinstance(turn, int):
                    turns = [0]
                    self.assertIn(turn, turns)
                else:
                    turns = ["unknown"]
                    self.assertIn(turn, turns)
                logs = ["Line can not be analyzed:", "Analyse errors completed!"]
                self.assertTrue(any(e in log for e in logs))
                

        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_log"]
        mock_output_handler, mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        expected_calls = [
            call(output_formats, ANY),
            call(output_formats, ANY)
        ]
        mock_output_handler.assert_has_calls(expected_calls)
        expected_calls = [
            call("ERROR"),
            call("unknown")
        ]
        mock_validate_level.assert_has_calls(expected_calls)
        mock_validate_log.assert_not_called()

    new_contents = [{"line_number": 0, "level": "ERROR", "turn": 0, "log": "random_choice: Failed!"},
                    {"line_number": 1, "turn": 0, "log": "random_choice: Success!"}]
    @patch.object(log_analyzer, "contents", new=new_contents)
    def test_unallowed_output_format(self):

        output_formats = ["..."]
        with self.assertRaises(RuntimeError):
            self.log_analyzer.analyse_errors(output_formats)
        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_level", "mock_validate_log"]
        mock_output_handler, mock_validate_level, mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        mock_output_handler.assert_not_called()
        mock_validate_level.assert_not_called()
        mock_validate_log.assert_not_called()

    new_contents = []
    @patch.object(log_analyzer, "contents", new=new_contents)
    def test_log_not_read(self):

        output_formats = ["console"]
        with self.assertRaises(RuntimeError):
            self.log_analyzer.analyse_errors(output_formats)
        NEEDED_MOCKS = ["mock_output_handler", "mock_validate_level", "mock_validate_log"]
        mock_output_handler, mock_validate_level, mock_validate_log = found_mocks = self.find_mocks(NEEDED_MOCKS)
        mock_output_handler.assert_not_called()
        mock_validate_level.assert_not_called()
        mock_validate_log.assert_not_called()


if __name__ == "__main__":
    main()
    os.remove(TestAnalyseErrors.file)