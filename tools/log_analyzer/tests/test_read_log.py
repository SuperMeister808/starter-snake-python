from unittest import TestCase
from unittest.mock import patch, MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
class TestReadLog(TestCase):

    file = "..."
    level_index = "..."
    turn_index = "..."
    log_index = "..."
    log_analyzer = LogAnalyzer(file, level_index, turn_index, log_index)
    def setUp(self):
        self.patchers = [
            patch.object(self.log_analyzer, "create_contents", name="mock_create_contents"),
            patch.object(self.log_analyzer, "save_contents", name="mock_save_contents")
        ]
        self.mocks = {}

        self.start_patchers()
        self.addCleanup(self.stop_patcherss)

    def start_patchers(self):
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patcherss(self):
        for pacher in self.patchers:
            pacher.stop()

    @patch.object(log_analyzer, "level_index", new=0)
    @patch.object(log_analyzer, "turn_index", new=1)
    @patch.object(log_analyzer, "log_index", new=2)
    def test_read_log_custom_args(self):

        file_handler = "..."
        mock_file = mock_open(read_data="HELLO WORLD !")
        with patch("builtins.open", mock_file):
            result = self.log_analyzer.read_log()
            mock_create_contents = self.mocks ["mock_create_contents"]
            expected_words = ["HELLO", "WORLD", "!"]
            mock_create_contents.assert_called_once_with(expected_words, 0, 0, 1, 2)
            mock_save_contents = self.mocks ["mock_save_contents"]
            mock_save_contents.assert_called_once()

    @patch.object(log_analyzer, "file", new={})
    @patch.object(log_analyzer, "level_index", new=0)
    @patch.object(log_analyzer, "turn_index", new=1)
    @patch.object(log_analyzer, "log_index", new=2)
    def test_read_log_unsupported_file_handler(self):

        file_handler = 0
        mock_file = mock_open(read_data="HELLO WORLD !")
        with patch("builtins.open", mock_file):
            with self.assertRaises(RuntimeError):
                result = self.log_analyzer.read_log()
                mock_create_contents = self.mocks ["mock_create_contents"]
                mock_create_contents.assert_not_called()
                mock_save_contents = self.mocks ["mock_save_contents"]
                mock_save_contents.assert_not_called()

if __name__ == "__main__":
    main()