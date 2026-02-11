
import unittest
from unittest.mock import patch

from move import Move

class TestGetBody(unittest.TestCase):

    def setUp(self):
        
        self.bot = Move()

    def test_move_left(self):

        snake = [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}]
        new_head = {"x": 0, "y": 1}

        result = self.bot.call_get_body(new_head, snake)

        expected = [{"x": 0, "y": 1}, {"x": 1, "y": 1}, {"x": 2, "y": 1}]

        self.assertEqual(result, expected)

    def test_move_down(self):

        snake = [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}]
        new_head = {"x": 1, "y": 0}

        result = self.bot.call_get_body(new_head, snake)
        expected = [{"x": 1, "y": 0}, {"x": 1, "y": 1}, {"x": 2, "y": 1}]

        self.assertEqual(result, expected)

    def test_irregular_move(self):

        snake = [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}]
        new_head = {"x": 0, "y": 0}

        result = self.bot.call_get_body(new_head, snake)
        expected = [{"x": 0, "y": 0}, {"x": 1, "y": 1}, {"x": 2, "y": 1}]

        self.assertEqual(result, expected)

    def test_id_in_body(self):

        snake = [{"id": "Testing..."}, {"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}]
        new_head = {"x": 0, "y": 1}

        result = self.bot.call_get_body(new_head, snake)
        expected = [{"x": 0, "y": 1}, {"x": 1, "y": 1}]


if __name__ == "__main__":

    unittest.main()