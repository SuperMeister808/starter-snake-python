from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer

# Tests that create_contents correctly parses log line words into structured content dictionaries.
class TestCreateContents(TestCase):

    def setUp(self):
        self.log_analyzer = LogAnalyzer("...", "...", "...", "...", "...")

    def test_default_args(self):
        # verifies that all fields default to unknown when no indices are provided
        result = self.log_analyzer.create_contents(["something"])
        self.assertEqual(result, {"line_number": "unknown", "level": "unknown", "turn": "unknown", "log": "unknown"})

    def test_args(self):
        # verifies that fields are correctly extracted using provided indices
        result = self.log_analyzer.create_contents(["somelevel", "Turn 0", "somelog"], 0, 0, 1, 2)
        self.assertEqual(result, {"line_number": 0, "level": "somelevel", "turn": 0, "log": "somelog"})

    def test_too_high_index(self):
        # verifies that out of range indices fall back to unknown
        result = self.log_analyzer.create_contents(["somelevel", "someturn", "somelog"], 0, 0, 5, 2)
        self.assertEqual(result, {"line_number": 0, "level": "somelevel", "turn": "unknown", "log": "somelog"})

    def test_empty_words(self):
        # edge case — verifies that an empty words list returns all unknown fields
        result = self.log_analyzer.create_contents([], 0, 0, 5, 2)
        self.assertEqual(result, {"line_number": 0, "level": "unknown", "turn": "unknown", "log": "unknown"})

if __name__ == "__main__":
    main()