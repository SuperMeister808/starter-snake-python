
import unittest
from unittest.mock import patch

from validate_game_state import validate_game_state

class TestValidateGameState(unittest.TestCase):

    def test_correct_key_and_correct_type(self):

        data = {"game": {}}
        result = validate_game_state(data)
        
        self.assertTrue(result)

    def test_incorrect_key(self):

        data = {"incorrect_key": {}}
        result = validate_game_state(data)
        
        self.assertFalse(result)

    def test_incorrect_type(self):

        data = {"game": 0}
        result = validate_game_state(data)

        self.assertFalse(result)

    def test_incorrect_key_and_key_with_incorrect_type(self):

        data = {"game": 0, "incorrect_key": {}}
        result = validate_game_state(data)

        self.assertFalse(result)

    def test_correct_type_key_turn(self):

        data = {"turn": 0}
        result = validate_game_state(data)

        self.assertTrue(result)

if __name__ == "__main__":

    unittest.main()

