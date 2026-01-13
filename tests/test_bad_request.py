
import unittest

from unittest.mock import patch

from requests import request

class TestBadRequest(unittest.main):

    def not_bad_request(self):

        data = {"game": {}}

        url = " http://0.0.0.0:8000"
        
        headers = {"contents": "application/json"}