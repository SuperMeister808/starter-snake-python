from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open , call
from unittest import main
from tools.log_analyzer import LogAnalyzer
import tempfile
import os
import logging
class TestOutputFormat(TestCase):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"...")
        file = tmp.name
    log_analyzer = LogAnalyzer(file)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.close()
        os.remove(cls.file)

    def setUp(self):
        
        self.mocks = {}
        self.patchers = [patch.object(self.log_analyzer.logger, "log", name="mock_log")]
        self.start_patchers()

        self.addCleanup(self.stop_patchers)
        self.addCleanup(self.log_analyzer.remove_handler)
        self.addCleanup(self.log_analyzer.close_handlers)
        
    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    @patch.object(log_analyzer, "file", new="...")
    @patch.object(log_analyzer, "add_handler", wraps=log_analyzer.add_handler)
    def test_incorrect_file_handler(self, mock_add_handler):
        output_formats = ["console", "file"]
        output = "anything"
        with self.assertRaises(RuntimeError):
            self.log_analyzer.output_handler(output_formats, output)
        mock_add_handler.assert_not_called()

    def test_all_output_formats(self):

        output_formats = ["console", "file"]
        output = {"level": "level", "turn": "turn", "log": "log", "line_number": "line_number"}
        with patch.object(self.log_analyzer, "remove_handler") as mock_remove_handler:
            self.log_analyzer.output_handler(output_formats, output)
            self.assertEqual(len(self.log_analyzer.logger.handlers), 2)
            self.assertTrue(any(isinstance(handler, logging.FileHandler) for handler in self.log_analyzer.logger.handlers))
            self.assertTrue(any(isinstance(handler, logging.StreamHandler) for handler in self.log_analyzer.logger.handlers))
            mock_log = self.mocks ["mock_log"]
            expected_calls = [
                call("level", "log", extra={"line_number": "line_number", "turn": "turn"})
            ]
            mock_log.assert_has_calls(expected_calls)

    def test_selected_output_formats(self):

        output_formats = ["console"]
        output = {"level": "level", "turn": "turn", "log": "log", "line_number": "line_number"}
        with patch.object(self.log_analyzer, "remove_handler") as mock_remove_handler:
            self.log_analyzer.output_handler(output_formats, output)
            self.assertEqual(len(self.log_analyzer.logger.handlers), 1)
            self.assertFalse(any(isinstance(handler, logging.FileHandler) for handler in self.log_analyzer.logger.handlers))
            self.assertTrue(any(isinstance(handler, logging.StreamHandler) for handler in self.log_analyzer.logger.handlers))
            mock_log = self.mocks ["mock_log"]
            expected_calls = [
                call("level", "log", extra={"line_number": "line_number", "turn": "turn"})
            ]
            mock_log.assert_has_calls(expected_calls)

    @patch.object(log_analyzer, "add_handler", wraps=log_analyzer.add_handler)
    def test_unallowed_output_format(self, mock_add_handler):

        output_formats = ["console", "file", "unallowed"]
        output = "anything"
        with self.assertRaises(RuntimeError):
            self.log_analyzer.output_handler(output_formats, output)
        mock_add_handler.assert_not_called()

if __name__ == "__main__":
    main()