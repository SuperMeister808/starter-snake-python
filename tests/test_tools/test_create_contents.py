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

        words = ["somelevel", "someturn", "somelog"]
        line_number = 0
        result = self.log_analyzer.create_contents(words, line_number, 0, 1, 2)
        expected = {"line_number": 0, "level": "somelevel", "turn": "someturn", "log": "somelog"}
        self.assertEqual(result, expected)

    def test_too_high_index(self):

        pass

    #Edge-Cae
    def test_len_words_equals_0(self):

        pass

if __name__ == "__main__":
    main()