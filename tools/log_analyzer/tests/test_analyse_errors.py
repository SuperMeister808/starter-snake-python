from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , call
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer

# Tests that analyse_errors correctly scans contents and outputs critical errors.
class TestAnalyseErrors(TestCase):

    def setUp(self):
        self.log_analyzer = LogAnalyzer("...", "...", "...", "...", "...")
        self.capture_output = []

        patch.object(self.log_analyzer, "output_handler", side_effect=self._fake_output_handler).start()
        patch.object(self.log_analyzer, "validate_level", wraps=self.log_analyzer.validate_level).start()
        patch.object(self.log_analyzer, "validate_log", wraps=self.log_analyzer.validate_log).start()
        patch.object(self.log_analyzer, "setup_logger").start()
        patch.object(self.log_analyzer, "setup_file_handler").start()

        self.addCleanup(patch.stopall)
        self.addCleanup(self._reset_capture_output)

    def _fake_output_handler(self, output_format, output):
        self.capture_output.append(output)

    def _reset_capture_output(self):
        self.capture_output = []

    def _call(self, contents, output_formats=None):
        if output_formats is None:
            output_formats = ["console"]
        with patch.object(self.log_analyzer, "contents", new=contents):
            return self.log_analyzer.analyse_errors(output_formats)

    ALLOWED_ERROR = "random_choice: Choosed emergency move"
    UNALLOWED_ERROR = "random_choice: Failed!"
    COMPLETION = {"line_number": "unknown", "level": 20, "log": "Analyse errors completed!", "turn": "unknown"}

    def test_only_allowed_errors(self):
        # verifies that allowed errors are not flagged and only completion message is output
        contents = [
            {"line_number": 0, "level": "ERROR", "turn": 0, "log": self.ALLOWED_ERROR},
            {"line_number": 1, "level": "INFO",  "turn": 0, "log": "random_choice: Success!"},
        ]
        self._call(contents)

        self.assertEqual(self.capture_output, [self.COMPLETION])
        self.log_analyzer.output_handler.assert_called_once_with(["console"], ANY)
        self.assertEqual(self.log_analyzer.validate_level.call_count, 2)
        self.assertEqual(self.log_analyzer.validate_log.call_count, 2)

    def test_unallowed_errors(self):
        # verifies that unallowed errors are flagged and included in output
        contents = [
            {"line_number": 1, "level": "ERROR", "turn": 0, "log": self.UNALLOWED_ERROR},
            {"line_number": 0, "level": "INFO",  "turn": 0, "log": "random_choice: Success!"},
        ]
        self._call(contents)

        expected_outputs = [
            {"line_number": 1, "level": 40, "log": self.UNALLOWED_ERROR, "turn": 0},
            self.COMPLETION,
        ]
        self.assertEqual(self.capture_output, expected_outputs)
        self.assertEqual(self.log_analyzer.output_handler.call_count, 2)
        self.assertEqual(self.log_analyzer.validate_level.call_count, 2)
        self.assertEqual(self.log_analyzer.validate_log.call_count, 2)

    def test_validation_failed(self):
        # verifies that invalid contents produce warning outputs and are not flagged as errors
        contents = [
            {"line_number": 0, "level": "ERROR", "turn": 0, "log": self.UNALLOWED_ERROR},
            {"line_number": 1, "turn": 0, "log": "random_choice: Success!"},
        ]
        self._call(contents)

        for output in self.capture_output:
            self.assertIsInstance(output, dict)
            self.assertIn(output["line_number"], [0, 1, "unknown"])
            self.assertIn(output["level"], [20, 30, 40])
            self.assertIsInstance(output["turn"], (int, str))
            logs = ["Line cannot be analyzed:", "Analyse errors completed!", self.UNALLOWED_ERROR]
            self.assertTrue(any(e in output["log"] for e in logs))

        self.log_analyzer.validate_level.assert_has_calls([call("ERROR"), call("unknown")])
        self.log_analyzer.validate_log.assert_has_calls([call(self.UNALLOWED_ERROR)])

    def test_unallowed_output_format(self):
        # verifies that RuntimeError is raised for an unrecognised output format
        contents = [{"line_number": 0, "level": "ERROR", "turn": 0, "log": self.UNALLOWED_ERROR}]
        with self.assertRaises(RuntimeError):
            self._call(contents, output_formats=["..."])

        self.log_analyzer.output_handler.assert_not_called()
        self.log_analyzer.validate_level.assert_not_called()
        self.log_analyzer.validate_log.assert_not_called()

    @patch.object(LogAnalyzer, "load_contents", side_effect=RuntimeError)
    def test_log_not_read(self, mock_load_contents):
        # verifies that RuntimeError is raised when contents are empty and load fails
        with self.assertRaises(RuntimeError):
            self._call(contents=[])

        self.log_analyzer.output_handler.assert_not_called()
        mock_load_contents.assert_called_once()

if __name__ == "__main__":
    main()