
import unittest

from unittest.mock import patch

from requests import request

from move import Move

class TestBadRequest(unittest.main):

    def not_bad_request(self):

        data = {"game": {}}

        url = " http://0.0.0.0:8000"
        
        headers = {"contents": "application/json"}

        with patch.object(Move, "choose_move", return_value="Called") as choose_move:
        
            response = request.post(data=data, url=url, headers=headers)

            choose_move.assert_called_once()