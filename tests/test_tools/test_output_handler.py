from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY , mock_open
from unittest import main
from tools.log_analyzer import LogAnalyzer
import tempfile
import os
class TestOutputFormat(TestCase):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"...")
        file = tmp.name
    log_analyzer = LogAnalyzer(file)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.close()
        os.remove(cls.file)

    def setUp(self):
        
        self.mocks = {}
        self.patchers = [patch.object(self.log_analyzer.logger, "log", side_effect=lambda output_format, output: output, name="mock_log")]
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

    @patch.object(log_analyzer, "file", new="...")
    @patch.object(log_analyzer, "add_handler", wraps=log_analyzer.add_handler)
    def test_incorrect_file_handler(self, mock_log_analyzer):
        output_formats = ["console", "file"]
        output = "anything"
        with self.assertRaises(RuntimeError):
            self.log_analyzer.output_handler(output_formats, output)
        mock_log_analyzer.assert_not_called()

    def test_all_output_formats(self):

        pass
    
    def test_selected_output_formats(self):

        pass

    def test_unallowed_output_format(self):

        pass

if __name__ == "__main__":
    main()