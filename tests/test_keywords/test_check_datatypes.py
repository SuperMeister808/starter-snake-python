
import unittest
from unittest.mock import patch

from keywords import Keywords

import unittest
from unittest.mock import patch

from keywords import Keywords

# Tests that check_datatype correctly validates keyword types and raises on invalid input.
class TestCheckDatatypes(unittest.TestCase):

    def setUp(self):
        self.keywords = Keywords()

        patch.object(self.keywords, "TYPE_MAP", new={
            "dictionary": dict,
            "list":       list,
            "string":     str,
            "integer":    int,
            "float":      float,
        }).start()

        self.addCleanup(patch.stopall)

        # base valid keywords used across tests
        self.valid = {
            "dictionary": {},
            "list":       [],
            "string":     "",
            "integer":    0,
            "float":      0.5,
        }

    def test_correct_keys(self):
        # verifies that no exception is raised for valid keyword types
        self.keywords.check_datatype(self.valid)

    def test_wrong_dictionary_type(self):
        # verifies that TypeError is raised when dictionary receives a list
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "dictionary": []})
        
    def test_wrong_list_type(self):
        # verifies that TypeError is raised when list receives a dict
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "list": {}})

    def test_wrong_string_type(self):
        # verifies that TypeError is raised when string receives a dict
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "string": {}})

    def test_wrong_integer_type(self):
        # verifies that TypeError is raised when integer receives a dict
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "integer": {}})

    def test_wrong_float_type(self):
        # verifies that TypeError is raised when float receives a dict
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "float": {}})

    def test_unlisted_key(self):
        # verifies that RuntimeError is raised for an unrecognised keyword
        with self.assertRaises(RuntimeError):
            self.keywords.check_datatype({**self.valid, "unlisted": ""})

    def test_unlisted_and_wrong_type(self):
        # verifies that TypeError is raised when both an unlisted key and wrong type exist
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "float": {}, "unlisted": ""})

    def test_multiple_wrong_types(self):
        # verifies that TypeError is raised when multiple keywords have wrong types
        with self.assertRaises(TypeError):
            self.keywords.check_datatype({**self.valid, "string": {}, "float": {}})

if __name__ == "__main__":
    unittest.main()
