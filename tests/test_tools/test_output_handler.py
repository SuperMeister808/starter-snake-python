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
        
        self.patchers = [patch.object(self.log_analyzer.logger, "log")]
        
    
    def test_incorrect_file_handler(self):

        pass

    def test_all_output_formats(self):

        pass
    
    def test_selected_output_formats(self):

        pass

    def test_unallowed_output_format(self):

        pass