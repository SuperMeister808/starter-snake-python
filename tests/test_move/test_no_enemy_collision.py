
import unittest
from unittest.mock import patch , MagicMock
from move import Move

class TestNoEnemyCollision(unittest.TestCase):

    bot = Move()
    def setUp(self):
        
        self.head = {"x": 2, "y": 2}
        self.game_state = "..."
        self.patchers = [
            patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, self.game_state), name="mock_extract_keywords")
        ]
        self.mocks = {}

    def start_patchers(self):
        
        for patcher in self.patchers:
            mock = patcher.start()
            if isinstance(mock, MagicMock):
                self.mocks [mock._mock_name] = mock

    def stop_patchers(self):
        for patcher in self.patchers:
            patcher.stop()

    def general_call_assertion(self):
        
        for name, mock in self.mocks.items():
            if isinstance(mock, MagicMock):
              mock.assert_called()

    def assert_call_extract_keywords(self):
        
        mock_extract_keywords = self.mocks.get("mock_extract_keywords", "unknown")
        if not isinstance(mock_extract_keywords, MagicMock):
            raise TypeError("Object: mock_extract_keywords is not a MagicMock()")
        
        mock_extract_keywords.assert_called_once_with(self.head, self.game_state)
    
    def test_unsafe_moves(self):
        
        pass
    
    def test_priority_moves(self):
        
        pass
    
    def test_unsafe_moves_and_priority_moves(self):
        
        pass
    
    def test_no_unsafe_and_no_priority_moves(self):
        
        pass
    
if __name__ == "__main__":

    unittest.main()