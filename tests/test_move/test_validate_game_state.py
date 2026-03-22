
import unittest
from unittest.mock import patch

from validate_game_state import validate_game_state

# Tests that validate_game_state correctly validates game state keys and types.
class TestValidateGameState(unittest.TestCase):

    def test_correct_key_and_type(self):
        # verifies that a valid key with correct type returns True
        self.assertTrue(validate_game_state({"game": {}}))

    def test_incorrect_key(self):
        # verifies that an unrecognised key returns False
        self.assertFalse(validate_game_state({"incorrect_key": {}}))

    def test_incorrect_type(self):
        # verifies that a valid key with wrong type returns False
        self.assertFalse(validate_game_state({"game": 0}))

    def test_incorrect_key_and_incorrect_type(self):
        # verifies that False is returned when both key and type are invalid
        self.assertFalse(validate_game_state({"game": 0, "incorrect_key": {}}))

    def test_turn_accepts_integer(self):
        # verifies that turn key correctly accepts an integer value
        self.assertTrue(validate_game_state({"turn": 0}))

if __name__ == "__main__":

    unittest.main()

