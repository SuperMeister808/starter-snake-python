
import unittest
from unittest.mock import patch , MagicMock

from move import Move

class TestCalculateOpponentsPositions(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.maxDiff = None
        
        self.mocks = {}
        self.patchers = [
            patch.object(self.bot.future_safety, "log_data", name="mock_log_data"),
        ]

        self.start_patchers()
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()
    
    def general_call_assertion(self):

        for name , mock in self.mocks.items():
            if isinstance(mock, MagicMock):
                mock.assert_called()
    
    def test_extract_positions_one_snake_head_is_safe(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": [{"id": "opponent", "length": 3, "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=False) as mock_is_growing:
            
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            #priority order: right, left, up, down
            expected_opponents_positions = {"opponent": {"unsafe": [{"x": 2, "y": 2}, {"x": 2, "y": 3}], "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}]}}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            self.general_call_assertion()
            mock_is_growing.assert_called_once()

    def test_extract_positions_one_snake_head_is_unsafe(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": [{"id": "opponent", "length": 5, "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=False) as mock_is_growing:
            
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            #priority order: right, left, up, down
            expected_opponents_positions = {"opponent": {"unsafe": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}], "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}]}}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            self.general_call_assertion()
            mock_is_growing.assert_called_once()
    
    def test_extract_positions_one_snake_is_growing(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": [{"id": "opponent", "length": 3, "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=True) as mock_is_growing:
            
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            #priority order: right, left, up, down
            expected_opponents_positions = {"opponent": {"unsafe": 
                                                         [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}], 
                                                         "priority": 
                                                         [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}]}}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            self.general_call_assertion()
            mock_is_growing.assert_called_once()

    def test_extract_positions_multiple_snakes(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": [{"id": "opponent_0", "length": 3, "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 4}]}, {"id": "opponent_1", "length": 5, "head": {"x": 2, "y": 2}, "body": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 4, "y": 2}]}]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=False) as mock_is_growing:
            
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            #priority order: right, left, up, down
            expected_opponents_positions = {"opponent_0": {"unsafe": [{"x": 2, "y": 2},
                                                                      {"x": 2, "y": 3}], 
                                                           "priority": [{"x": 3, "y": 2},
                                                                        {"x": 1, "y": 2},
                                                                        {"x": 2, "y": 3},
                                                                        {"x": 2, "y": 1}]},
                                            "opponent_1": {"unsafe": [{"x": 2, "y": 2},
                                                                      {"x": 3, "y": 2},
                                                                      {"x": 3, "y": 2},
                                                                      {"x": 1, "y": 2},
                                                                      {"x": 2, "y": 3},
                                                                      {"x": 2, "y": 1}], 
                                                           "priority": [{"x": 3, "y": 2},
                                                                        {"x": 1, "y": 2},
                                                                        {"x": 2, "y": 3},
                                                                        {"x": 2, "y": 1}]}}
                        
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            self.general_call_assertion()
            mock_is_growing.assert_called()

    def test_extract_positions_no_snakes(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": []}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=False) as mock_is_growing:
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            expected_opponents_positions = {}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            #log is called before iteration
            self.general_call_assertion()
            mock_is_growing.assert_not_called()


    def test_missing_body_parts_between_head_and_tail(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": [{"head": {"x": 2, "y": 2}, "id": "opponent", "length": 3, "body": [{"x": 2, "y": 2}, {"x": 2, "y": 3}]}]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=False) as mock_is_growing:
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            expected_opponents_positions = {"opponent": {"unsafe": [{"x": 2, "y": 2}], "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}]}}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            self.general_call_assertion()
            mock_is_growing.assert_called_once()

    def test_snake_has_wrong_type(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": ["opponent"]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=False) as mock_is_growing:
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            expected_opponents_positions = {}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            #log is called before iteration
            self.general_call_assertion()
            mock_is_growing.assert_not_called()


    
    #Edge-Case
    def test_only_head(self):

        game_state = {"you": {"id": "you"}, "board": {"snakes": [{"id": "opponent", "head": {"x": 2, "y": 2}, "length": 3, "body": [{"x": 2, "y": 2}]}]}}
        my_length = 4
        with patch.object(self.bot, "is_growing", return_value=True) as mock_is_growing:
            self.bot.calculate_opponents_positions(game_state=game_state, my_length=my_length)
            expected_opponents_positions = {"opponent": {"unsafe": [{"x": 2, "y": 2}], "priority": [{"x": 3, "y": 2}, {"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 1}]}}
            self.assertEqual(self.bot.opponents_positions, expected_opponents_positions)

            self.general_call_assertion()
            mock_is_growing.assert_not_called()


if __name__ == "__main__":
    unittest.main()