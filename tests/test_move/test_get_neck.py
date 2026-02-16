
import unittest
from unittest.mock import patch

from move import Move

class TestGetNeck(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

    def test_get_neck_game_elements(self):

        body = [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}]
        result = self.bot.get_neck(body)
        expected = {"x": 2, "y": 1}

        self.assertEqual(result, expected)

    def test_get_neck_other_elements(self):

        body = [0, 1, 2]
        result = self.bot.get_neck(body)
        expected = 1

        self.assertEqual(result, expected)

if __name__ == "__main__":

    unittest.main()