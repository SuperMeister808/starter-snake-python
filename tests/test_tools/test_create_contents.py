from unittest import TestCase
from unittest.mock import patch , MagicMock , ANY
from unittest import main
from tools.log_analyzer import LogAnalyzer
class TestCreateContents(TestCase):

    log_analyzer = LogAnalyzer()
    def setUp(self):
        
        pass
    
    def test_default_args(self):

        words = ["something"]
        result = self.log_analyzer.create_contents(words)
        expected = {"line_number": "unknown", "level": "unknown", "turn": "unknown", "log": "unknown"}
        self.assertEqual(result, expected)

    def test_args(self):

        pass

    def test_too_high_index(self):

        pass

    #Edge-Cae
    def test_len_words_equals_0(self):

        pass

if __name__ == "__main__":
    main()