from unittest import TestCase
from unittest.mock import patch, MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer

# Tests that read_log correctly reads and parses log file contents.
class TestReadLog(TestCase):

    def setUp(self):
        self.log_analyzer = LogAnalyzer("...", "...", "...", "...", "...")

        patch.object(self.log_analyzer, "create_contents").start()
        patch.object(self.log_analyzer, "save_contents").start()

        self.addCleanup(patch.stopall)

    def test_read_log_custom_args(self):
        # verifies that create_contents is called with correct words and indices
        with patch.object(self.log_analyzer, "level_index", new=0), \
             patch.object(self.log_analyzer, "turn_index", new=1), \
             patch.object(self.log_analyzer, "log_index", new=2):
            with patch("builtins.open", mock_open(read_data="HELLO WORLD !")):
                self.log_analyzer.read_log()

                self.log_analyzer.create_contents.assert_called_once_with(["HELLO WORLD !"], 0, 0, 1, 2)
                self.log_analyzer.save_contents.assert_called_once()

    def test_read_log_unsupported_file(self):
        # verifies that RuntimeError is raised when file path is not a string
        with patch.object(self.log_analyzer, "file", new={}):
            with self.assertRaises(RuntimeError):
                self.log_analyzer.read_log()

            self.log_analyzer.create_contents.assert_not_called()
            self.log_analyzer.save_contents.assert_not_called()

if __name__ == "__main__":
    main()