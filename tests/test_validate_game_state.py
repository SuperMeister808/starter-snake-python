
import unittest
from unittest.mock import patch

from validate_game_state import validate_game_state

class TestValidateGameState(unittest.TestCase):

    def test_correct_game_state(self):

        game_state = {"game": {}, "ruleset": {}, "squad": {}, "turn": 1, "board": {}, "you": {}}

        self.assertTrue(validate_game_state(game_state))

    def test_wrong_key(self):

        game_state = {"game": {}, "rules": {}, "squad": {}, "turn": 1, "board": {}, "you": {}}

        self.assertFalse(validate_game_state(game_state))

    def test_wrong_data(self):

        game_state = {"game": {}, "ruleset": {}, "squad": {}, "turn": {}, "board": {}, "you": {}}

        self.assertFalse(validate_game_state(game_state))

    def test_wrong_key_and_wrong_data(self):

        game_state = {"gamer": {}, "ruleset": 1, "squad": {}, "turn": 1, "board": {}, "you": {}}

        self.assertFalse(validate_game_state(game_state))

if __name__ == "__main__":

    unittest.main()

