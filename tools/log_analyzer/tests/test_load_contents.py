from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
import json
import os

# Tests that load_contents correctly loads and validates the JSON cache.
class TestLoadContents(TestCase):

    def setUp(self):
        self.log_analyzer = LogAnalyzer("...", "...", "...", "...", "...")
        self.log_analyzer.contents = []

        patch.object(self.log_analyzer, "read_log").start()
        patch.object(self.log_analyzer, "validate_contents", wraps=self.log_analyzer.validate_contents).start()

        self.addCleanup(patch.stopall)

    CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "contents.json")
    VALID_CONTENT = {"line_number": "line_number", "level": "level", "turn": "turn", "log": "log"}

    def _call(self, contents):

        mock = mock_open(read_data=json.dumps(contents))
        with patch("builtins.open", mock):
            self.log_analyzer.load_contents()
            mock.assert_called_once_with(self.CACHE_PATH, "r")
            return mock

    def test_load_valid_contents(self):
        # verifies that valid contents are loaded and set correctly
        contents = [self.VALID_CONTENT]
        self._call(contents)

        self.assertEqual(self.log_analyzer.contents, contents)
        self.log_analyzer.validate_contents.assert_called_once_with(contents)
        self.log_analyzer.read_log.assert_not_called()

    def test_load_invalid_contents_missing_keys(self):
        # verifies that contents with missing keys trigger a re-read of the log
        contents = [{"line_number": "line_number", "level": "level", "turn": "turn"}]
        self._call(contents)

        self.assertEqual(self.log_analyzer.contents, [])
        self.log_analyzer.validate_contents.assert_called_once_with(contents)
        self.log_analyzer.read_log.assert_called_once()

    def test_load_invalid_contents_extra_keys(self):
        # verifies that contents with extra keys trigger a re-read of the log
        contents = [{**self.VALID_CONTENT, "unallowed": "unallowed"}]
        self._call(contents)

        self.assertEqual(self.log_analyzer.contents, [])
        self.log_analyzer.validate_contents.assert_called_once_with(contents)
        self.log_analyzer.read_log.assert_called_once()

    def test_load_invalid_contents_wrong_type(self):
        # verifies that contents with wrong type trigger a re-read of the log
        contents = {**self.VALID_CONTENT, "unallowed": "unallowed"}
        self._call(contents)

        self.assertEqual(self.log_analyzer.contents, [])
        self.log_analyzer.validate_contents.assert_called_once_with(contents)
        self.log_analyzer.read_log.assert_called_once()

if __name__ == "__main__":
    main()