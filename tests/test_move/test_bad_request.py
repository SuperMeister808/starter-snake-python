
import unittest

from unittest.mock import patch

from requests import request

from server import Server

class TestBadRequest(unittest.TestCase):

    
    def setUp(self):

        self.handlers = {"move": lambda game_state: {"Success": "Called move"}}
        self.server = Server(self.handlers, "Testing...", "Testing...", False, 8000)

    def start_patchers(self):

        for patcher in self.patchers:
            patcher.start()

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()
    
    @patch("server.validate_game_state", return_value=True)
    def test_correct_request(self, mock_validate_game_state):

        data = {"testing": "testing..."}
        test_client = self.server.app.test_client()
        response = test_client.post("/move", json=data)
        
        mock_validate_game_state.assert_called_once_with(data)

        self.assertEqual(response.json, {"Success": "Called move"})
        self.assertEqual(response.status_code, 200)

    @patch("server.validate_game_state", return_value=False)
    def test_bad_request(self, mock_validate_game_state):

        data = {"testing": "testing..."}
        test_client = self.server.app.test_client()
        response = test_client.post("/move", json=data)
        
        mock_validate_game_state.assert_called_once_with(data)

        self.assertEqual(response.json, {'error': 'Game state validation failed'})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":

    unittest.main()



            