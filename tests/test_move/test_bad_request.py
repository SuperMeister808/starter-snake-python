
import unittest

from unittest.mock import patch

from requests import request

from server import Server

class TestBadRequest(unittest.TestCase):

    def setUp(self):
        
        self.server = Server("Testing...", "Testing...", "Testing...", False, 8000)
    
    def test_correct_key_and_correct_type(self):

        data = {"game": {}}

        with patch.object(self.server, "handlers", {"move": lambda game_state: {"Succes": "Called move"}}):
        
            test_client = self.server.app.test_client()
            
            response = test_client.post("/move", json=data)

            self.assertEqual(response.json, {"Succes": "Called move"})

    def test_bad_request_move(self):

        data = {"game": 1}

        with patch.object(self.server, "handlers", {"move": lambda game_state: {"Succes": "Called move"}}):
        
            test_client = self.server.app.test_client()
            
            response = test_client.post("/move", json=data)

            self.assertEqual(response.json, {"Error": "Game State Validation Failed!"})

if __name__ == "__main__":

    unittest.main()



            