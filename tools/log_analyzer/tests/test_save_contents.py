from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
import json
class TestSaveContents(TestCase):

    file = "..."
    file_handler = "..."
    level_index = "..."
    turn_index = "..."
    log_index = "..."
    log_analyzer = LogAnalyzer(file, file_handler, level_index, turn_index, log_index)
    def setUp(self):
       
       pass
    
    @patch.object(log_analyzer, "contents", new=[])
    def test_save_contents(self):

        mock = mock_open()
        with patch("builtins.open", mock):
            contents_json = json.dumps(self.log_analyzer.contents)
            self.log_analyzer.save_contents()
            mock.assert_called_once_with(r'C:\Users\emilc\game_agent\starter-snake-python\tools\log_analyzer\ressources\contents.json', 'w')
            mock().write.assert_called_once_with(contents_json)

if __name__ == "__main__":
    main()
