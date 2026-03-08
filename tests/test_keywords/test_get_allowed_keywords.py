
import unittest
from unittest.mock import patch

from keywords import Keywords

class TestGetAllowedKeywords(unittest.TestCase):

    keywords = Keywords()

    @patch.object(keywords, "ALLOWED_KEYWORDS", new=["head", "body", "neck", "my_length"])
    def test_only_allowed_keywords(self):

        result = self.keywords.get_allowed_keywords(head="head", body="body", neck="neck", my_length="my_length")
        head = result["head"]
        body = result["body"]
        neck = result["neck"]
        my_length = result["my_length"]

        self.assertEqual(head, "head")
        self.assertEqual(body, "body")
        self.assertEqual(neck, "neck")
        self.assertEqual(my_length, "my_length")

    def test_sort_unallowed_keywords_out(self):

        pass

    def test_only_unallowed_keywords(self):

        pass

if __name__ == "__main__":
    unittest.main()