
import unittest

from unittest.mock import patch

from requests import request

from server import Server

class TestBadRequest(unittest.TestCase):

    def setUp(self):
        
        self.server = Server("Testing...", "Testing...", "Testing...", False, 8000)

        self.patchers = [
            patch.object(self.server, "handlers", new={"move": lambda game_state: {"Succes": "Called move"}})
        ]

        self.start_patchers()
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:
            patcher.start()

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()
    
    def test_correct_key_and_correct_type(self):

        data = {"game": {}}

        test_client = self.server.app.test_client()
        response = test_client.post("/move", json=data)
        
        self.assertEqual(response.json, {"Succes": "Called move"})

    def test_incorrect_key(self):

        pass

    def test_incorrect_key_and_key_with_incorrect_type(self):

        pass

    def test_correct_type_key_turn(self):

        pass
    
    def test_bad_request_move(self):

        data = {"game": 1}

        with patch.object(self.server, "handlers", {"move": lambda game_state: {"Succes": "Called move"}}):
        
            test_client = self.server.app.test_client()
            
            response = test_client.post("/move", json=data)

            self.assertEqual(response.json, {"Error": "Game State Validation Failed!"})

if __name__ == "__main__":

    unittest.main()



            