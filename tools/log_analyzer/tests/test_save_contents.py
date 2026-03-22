from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
import json
import os

# Tests that save_contents correctly writes contents to the JSON cache file.
class TestSaveContents(TestCase):

    CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "contents.json")

    def setUp(self):
        self.log_analyzer = LogAnalyzer("...", "...", "...", "...", "...")
        self.log_analyzer.contents = []

    def test_save_contents(self):
        # verifies that contents are correctly serialized and written to the cache file
        mock = mock_open()
        with patch("builtins.open", mock):
            expected_json = json.dumps(self.log_analyzer.contents)
            self.log_analyzer.save_contents()

            mock.assert_called_once_with(self.CACHE_PATH, "w")
            mock().write.assert_called_once_with(expected_json)

if __name__ == "__main__":
    main()
