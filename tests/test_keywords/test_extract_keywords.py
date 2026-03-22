
import unittest
from unittest.mock import patch , MagicMock

from keywords import Keywords

# Tests that extract_keywords correctly extracts and validates required keywords.
class TestExtractKeywords(unittest.TestCase):

    def setUp(self):
        self.keywords = Keywords()

        patch.object(self.keywords, "get_allowed_keywords",
                     return_value={"head": "head", "body": "body", "neck": "neck", "my_length": "my_length"}).start()
        patch.object(self.keywords, "check_datatype").start()

        self.addCleanup(patch.stopall)

    def test_correct_needed_keywords(self):
        # verifies that all required keywords are extracted in the correct order
        result = self.keywords.extract_keywords(
            ["head", "body", "neck", "my_length"], testing="testing..."
        )

        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")
        self.assertEqual(result, ["head", "body", "neck", "my_length"])

    def test_unnecessary_keywords(self):
        # verifies that only requested keywords are returned even if more are available
        result = self.keywords.extract_keywords(
            ["head", "body", "neck"], testing="testing..."
        )

        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")
        self.assertEqual(result, ["head", "body", "neck"])

    def test_needed_keywords_missing(self):
        # verifies that KeyError is raised when a required keyword is not available
        with self.assertRaises(KeyError):
            self.keywords.extract_keywords(
                ["head", "body", "neck", "my_length", "missing"], testing="testing..."
            )

        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")

    def test_missing_and_unnecessary_keywords(self):
        # verifies that KeyError is raised even when some keywords are unnecessary
        with self.assertRaises(KeyError):
            self.keywords.extract_keywords(
                ["head", "body", "neck", "missing"], testing="testing..."
            )

        self.keywords.get_allowed_keywords.assert_called_once_with(testing="testing...")

if __name__ == "__main__":
    unittest.main()