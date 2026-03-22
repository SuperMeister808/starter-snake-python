
import unittest
from unittest.mock import patch

from keywords import Keywords

# Tests that get_allowed_keywords correctly filters kwargs to only allowed keywords.
class TestGetAllowedKeywords(unittest.TestCase):

    def setUp(self):
        self.keywords = Keywords()

        patch.object(self.keywords, "ALLOWED_KEYWORDS",
                     new=["head", "body", "neck", "my_length"]).start()

        self.addCleanup(patch.stopall)

    def test_only_allowed_keywords(self):
        # verifies that all allowed keywords are returned correctly
        result = self.keywords.get_allowed_keywords(
            head="head", body="body", neck="neck", my_length="my_length"
        )
        self.assertEqual(result, {"head": "head", "body": "body", "neck": "neck", "my_length": "my_length"})

    def test_filters_unallowed_keywords(self):
        # verifies that unallowed keywords are silently removed from the result
        result = self.keywords.get_allowed_keywords(
            head="head", body="body", neck="neck", my_length="my_length",
            anything="anything", wherever="wherever"
        )
        self.assertEqual(result, {"head": "head", "body": "body", "neck": "neck", "my_length": "my_length"})
        self.assertNotIn("anything", result)
        self.assertNotIn("wherever", result)

    def test_only_unallowed_keywords(self):
        # verifies that an empty dict is returned when all keywords are unallowed
        result = self.keywords.get_allowed_keywords(anything="anything", wherever="wherever")
        self.assertEqual(result, {})

if __name__ == "__main__":
    unittest.main()