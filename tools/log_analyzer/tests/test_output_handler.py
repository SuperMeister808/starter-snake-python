from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open , call
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
import tempfile
import os
import logging

# Tests that output_handler correctly routes log output to the specified handlers.
class TestOutputFormat(TestCase):

    def setUp(self):
        self.log_analyzer = LogAnalyzer("...", "...", "...", "...", "...")
        self.captured_handlers = []
        self.VALID_CAPTURED_OUTPUT_HANDLERS = ["file", "console"]

        patch.object(self.log_analyzer.logger, "log").start()
        patch.object(self.log_analyzer, "add_handler", side_effect=lambda output_handler:self.captured_handlers.extend(output_handler)).start()
        patch.object(self.log_analyzer, "remove_handler").start()
        patch.object(self.log_analyzer, "setup_handlers").start()
        patch.object(self.log_analyzer, "close_handlers").start()
        
        self.addCleanup(patch.stopall)

    def test_correct_output(self):
        # verifies that the log is called with correct arguments
        with patch.object(self.log_analyzer.logger, "handlers", new=["file", "console"]):
            output = {"line_number": 0, "turn": 0, "level": 40, "log": "Something went wrong"}
            self.log_analyzer.output_handler(["console", "file"], output)

            self.log_analyzer.logger.log.assert_called_once_with(
                40, "Something went wrong", extra={"line_number": 0, "turn": 0}
            )
            assert all(handler in self.VALID_CAPTURED_OUTPUT_HANDLERS for handler in self.captured_handlers)

    def test_one_key_missing(self):
        # verifies that missing keys default to unknown
        with patch.object(self.log_analyzer.logger, "handlers", new=["file", "console"]):
            output = {"line_number": 0, "level": 40, "log": "Something went wrong"}
            self.log_analyzer.output_handler(["console", "file"], output)

            self.log_analyzer.logger.log.assert_called_once_with(
                40, "Something went wrong", extra={"line_number": 0, "turn": "unknown"}
            )
            assert all(handler in self.VALID_CAPTURED_OUTPUT_HANDLERS for handler in self.captured_handlers)

    def test_invalid_output(self):
        # verifies that RuntimeError is raised when output is not a dictionary
        with patch.object(self.log_analyzer.logger, "handlers", new=["file", "console"]):
            with self.assertRaises(RuntimeError):
                self.log_analyzer.output_handler(["console", "file"], [])

            self.log_analyzer.logger.log.assert_not_called()

    def test_no_handlers_added(self):
        # verifies that RuntimeError is raised when no handlers are active
        output = {"line_number": 0, "turn": 0, "level": 40, "log": "Something went wrong"}
        with patch.object(self.log_analyzer.logger, "handlers", new=[]):
            with self.assertRaises(RuntimeError):
                self.log_analyzer.output_handler(["console", "file"], output)

            self.log_analyzer.logger.log.assert_not_called()

if __name__ == "__main__":

    main()