from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open , call
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
import tempfile
import os
import logging
class TestOutputFormat(TestCase):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"...")
        file = tmp.name
    file_handler = "..."
    level_index = "..."
    turn_index = "..."
    log_index = "..."
    log_analyzer = LogAnalyzer(file, file_handler, level_index, turn_index, log_index)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.close()
        os.remove(cls.file)

    def setUp(self):
        
        self.mocks = {}
        self.patchers = [patch.object(self.log_analyzer.logger, "log", name="mock_log")]
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

    @patch.object(log_analyzer.logger, "handlers", new=["file", "console"])
    def test_correct_output(self):
        output_formats = ["console", "file"]
        output = {"line_number": 0, "turn": 0, "level": 40, "log": "Something went wrong"}
        self.log_analyzer.output_handler(output_formats, output)
        mock_log = self.mocks ["mock_log"]
        mock_log.assert_called_once_with(40, "Something went wrong", extra={"line_number": 0, "turn": 0})

    @patch.object(log_analyzer.logger, "handlers", new=["file", "console"])
    def test_one_key_is_missing(self):

        output_formats = ["console", "file"]
        output = {"line_number": 0, "level": 40, "log": "Something went wrong"}
        self.log_analyzer.output_handler(output_formats, output)
        mock_log = self.mocks ["mock_log"]
        mock_log.assert_called_once_with(40, "Something went wrong", extra={"line_number": 0, "turn": "unknown"})

    def test_invalid_output(self):

        pass

    def test_no_handlers_added(self):
        
        pass

if __name__ == "__main__":
    main()