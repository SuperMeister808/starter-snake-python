
import unittest
from unittest.mock import patch , MagicMock

from keywords import Keywords

class TestExtractKeywords(unittest.TestCase):

    keywords = Keywords()
    def setUp(self):
        
        self.patchers = [
            patch.object(self.keywords, "get_allowed_keywords", return_value={"head": "head", "body": "body", "neck": "neck", "my_length": "my_length"}, name="mock_get_allowed_keywords"),
            patch.object(self.keywords, "check_datatype", name="mock_check_datatype")
        ]
        self.mocks = {}

        self.start_patchers()
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):
            mock = patcher.start()
            try:
                self.mocks [mock.name] = mock
            except AttributeError:
                if isinstance(mock, MagicMock):
                    self.mocks [mock._mock_name] = mock
                else:
                    self.mocks [i] = mock

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            if not isinstance(mock, MagicMock):
                continue
            mock.assert_called()
    
    def test_correct_needed_keywords(self):

        needed_keywords = ["head", "body", "neck", "my_length"]
        result = self.keywords.extract_keywords(needed_keywords, testing="testing...")
        
        self.check_calls()
        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")

        self.assertEqual(result, ["head", "body", "neck", "my_length"])
        head , body , neck , my_length = result
        self.assertEqual(head, "head")
        self.assertEqual(body, "body")
        self.assertEqual(neck, "neck")
        self.assertEqual("my_length", my_length)

    def test_unnecessary_keywords(self):

        needed_keywords = ["head", "body", "neck"]
        result = self.keywords.extract_keywords(needed_keywords, testing="testing...")
        
        self.check_calls()
        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")

        self.assertEqual(result, ["head", "body", "neck"])
        head , body , neck= result
        self.assertEqual(head, "head")
        self.assertEqual(body, "body")
        self.assertEqual(neck, "neck")

    def test_needed_keywords_missing(self):

        needed_keywords = ["head", "body", "neck", "my_length", "missing"]
        with self.assertRaises(KeyError):
            self.keywords.extract_keywords(needed_keywords, testing="testing...")
        
        self.check_calls()
        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")

    def test_missing_and_unnecessary_keywords(self):

        needed_keywords = ["head", "body", "neck", "missing"]
        with self.assertRaises(KeyError):
            self.keywords.extract_keywords(needed_keywords, testing="testing...")
        
        self.check_calls()
        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")

if __name__ == "__main__":
    unittest.main()