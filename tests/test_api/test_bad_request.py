
import unittest

from unittest.mock import patch

from requests import request

from server import Server

# Tests that the /move endpoint correctly handles valid and invalid game states.
class TestBadRequest(unittest.TestCase):

    def setUp(self):
        self.handlers = {"move": lambda game_state: {"Success": "Called move"}}
        self.server = Server(self.handlers, "Testing...", "Testing...", False, 8000)
        self.client = self.server.app.test_client()
        self.data = {"testing": "testing..."}

    @patch("server.validate_game_state", return_value=True)
    def test_correct_request(self, mock_validate_game_state):
        # verifies that a valid game state returns the move response with status 200
        response = self.client.post("/move", json=self.data)

        mock_validate_game_state.assert_called_once_with(self.data)
        self.assertEqual(response.json, {"Success": "Called move"})
        self.assertEqual(response.status_code, 200)

    @patch("server.validate_game_state", return_value=False)
    def test_bad_request(self, mock_validate_game_state):
        # verifies that an invalid game state returns an error response with status 400
        response = self.client.post("/move", json=self.data)

        mock_validate_game_state.assert_called_once_with(self.data)
        self.assertEqual(response.json, {"error": "Game state validation failed"})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":

    unittest.main()



            