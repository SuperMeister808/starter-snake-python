from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
import json
class TestLoadContents(TestCase):

    file = "..."
    level_index = "..."
    turn_index = "..."
    log_index = "..."
    log_analyzer = LogAnalyzer(file, level_index, turn_index, log_index)
    def setUp(self):
        
        self.mocks = {}
        self.patchers = [
            patch.object(self.log_analyzer, "read_log", name="mock_read_log"),
            patch.object(self.log_analyzer, "validate_contents", wraps=self.log_analyzer.validate_contents, name="mock_validate_contents")
        ]
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
    
    @patch.object(log_analyzer, "contents", new={})
    def test_load_valide_contents(self):

        contents = {"line_number": "line_number", "level": "level", "turn": "turn", "log": "log"}
        read_data = json.dumps(contents)
        mock = mock_open(read_data=read_data)
        with patch("builtins.open", mock):
            self.log_analyzer.load_contents()
            self.assertEqual(self.log_analyzer.contents, {"line_number": "line_number", "level": "level", "turn": "turn", "log": "log"}) 
            mock.assert_called_once_with("ressources/contents.json", "r")
            mock_validate_contents = self.mocks ["mock_validate_contents"]
            mock_validate_contents.assert_called_once()
            mock_read_log = self.mocks ["mock_read_log"]
            mock_read_log.assert_not_called()
            
    @patch.object(log_analyzer, "contents", new={})
    def test_load_invalid_contents_keys(self):

        contents = {"line_number": "line_number", "level": "level", "turn": "turn"}
        read_data = json.dumps(contents)
        mock = mock_open(read_data=read_data)
        with patch("builtins.open", mock):
            self.log_analyzer.load_contents()
            #self.assertEqual(self.log_analyzer.contents, {}) 
            mock.assert_called_once_with("ressources/contents.json", "r")
            mock_validate_contents = self.mocks ["mock_validate_contents"]
            mock_validate_contents.assert_called_once()
            mock_read_log = self.mocks ["mock_read_log"]
            mock_read_log.assert_called_once()

    def test_invalid_contents_type(self):

        pass

if __name__ == "__main__":
    main()