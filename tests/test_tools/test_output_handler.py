from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer import LogAnalyzer
class TestOutputFormat(TestCase):

    log_analyzer = LogAnalyzer()
    def setUp(self):
        
        pass
    
    def test_output_format_file_correct_file_handler(self):

        mock = mock_open()
        with patch("builtins.open", mock):
            output_format = "file"
            output = "Hello World!"
            file_handler = "dummy.txt"
            self.log_analyzer.output_handler(output_format, output, file_handler)
            mock().write.assert_called_once_with("Hello World!\n")

    def test_output_format_file_incorrect_file_handler(self):

        pass

    def test_output_format_console(self):

        pass

    def test_unallowed_output_format(self):

        pass