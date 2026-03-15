from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer.log_analyzer import LogAnalyzer
class TestSafeContents(TestCase):

    file = "..."
    level_index = "..."
    turn_index = "..."
    log_index = "..."
    log_analyzer = LogAnalyzer(file, level_index, turn_index, log_index)
    def setUp(self):
       
       pass
    
    @patch.object(log_analyzer, "contents", new="...")
    def test_safe_contents(self):

        mock = mock_open()
        with patch("builtins.open", mock):
            self.log_analyzer.save_contents()
            mock().write.assert_called_once_with("...")

if __name__ == "__main__":
    main()
