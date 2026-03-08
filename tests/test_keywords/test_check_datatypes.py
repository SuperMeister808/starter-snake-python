
import unittest
from unittest.mock import patch

from keywords import Keywords

class TestCheckDatatypes(unittest.TestCase):

    keywords = Keywords()
    def setUp(self):
        
        self.patchers = [
            patch.object(self.keywords, "DICTIONARY_KEYS", new=["dictionary"]),
            patch.object(self.keywords, "LIST_KEYS", new=["list"]),
            patch.object(self.keywords, "STRING_KEYS", new=["string"]),
            patch.object(self.keywords, "INTEGER_KEYS", new=["integer"]),
            patch.object(self.keywords, "FLOAT_KEYS", new=["float"])
        ]

        self.start_patchers()
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:
            patcher.start()

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()
    
    def test_correct_keys(self):

        keywords = {"dictionary": {}, "list": [], "string": "", "integer": 0, "float": 0.5}
        self.keywords.check_datatype(keywords)
    
    def test_wrong_dictionary_key(self):

        pass

    def test_wrong_list_key(self):

        pass

    def test_wrong_string_key(self):

        pass

    def test_wrong_integer_key(self):

        pass

    def test_wrong_float_key(self):

        pass

    def test_unlisted_key(self):

        pass

if __name__ == "__main__":
    unittest.main()