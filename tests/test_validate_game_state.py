
import unittest
from unittest.mock import patch

from validate_game_state import validate_game_state

class TestValidateGameState(unittest.TestCase):

    def test_correct_game_state(self):

        game_state = {"game": {}, "ruleset": {}, "squad": {}, "turn": {}, "board": {}, "you": {}}

        self.assertTrue(validate_game_state(game_state))

    def test_wrong_key(self):

        game_state = {"game": {}, "rules": {}, "squad": {}, "turn": {}, "board": {}, "you": {}}

if __name__ == "__main__":

    unittest.main()

