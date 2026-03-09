
import unittest

from unittest.mock import patch

from move import Move

class TestIsGrowing(unittest.TestCase):

  bot = Move()
  def setUp(self):
     
     self.head = {"x": 2, "y": 2}
     self.game_state = "..."
  
  def test_is_growqing(self):
        
      game_state = {"board": {"food": [{"x": 2, "y": 3}]}}
      with patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, game_state)) as mock_extract_keywords:
         
         result = self.bot.is_growing(head=self.head, game_state=game_state)
         self.assertTrue(result)

         mock_extract_keywords.assert_called_once()
  
  
  def test_is_growing_multiple_times(self):
     
    game_state = {"board": {"food": [{"x": 1, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 1}, {"x": 2, "y": 3}]}}
    with patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, game_state)) as mock_extract_keywords:
       result = self.bot.is_growing(head=self.head, game_state=self.game_state)
       self.assertTrue(result)

       mock_extract_keywords.assert_called_once()
  
  def test_is_not_growing(self):
     
     game_state = {"board": {"food": []}}
     with patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, game_state)) as mock_extract_keywords:
        result = self.bot.is_growing(head=self.head, game_state=game_state)
        self.assertFalse(result)

        mock_extract_keywords.assert_called_once()

  def test_is_not_growing_food_out_of_range(self):
     
     game_state = {"board": {"food": [{"x": 4, "y": 4}, {"x": 0, "y": 0}, {"x": 0, "y": 4}, {"x": 4, "y": 0}]}}
     with patch.object(self.bot.keywords, "extract_keywords", return_value=(self.head, game_state)) as mock_extract_keywords:
        result = self.bot.is_growing(head=self.head, game_state=game_state)
        self.assertFalse(result)

        mock_extract_keywords.assert_called_once()


if __name__ == "__main__":

    unittest.main()
