
import unittest
from unittest.mock import patch

class TestFutureSafety(unittest.TestCase):

    def test_safe_moves_left(self):

        game_state = {"you": {"head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 1}, {"x": 1, "y": 1}, {"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}, {"x": 3, "y": 3}]}}

    def test_no_safe_moves_left(self):

        pass