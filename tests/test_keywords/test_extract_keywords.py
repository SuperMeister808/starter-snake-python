
import unittest
from unittest.mock import patch , MagicMock

from keywords import Keywords

class TestExtractKeywords(unittest.TestCase):

    keywords = Keywords()
    def setUp(self):
        
        self.patchers = [
            patch.object(self.keywords, "check_datatype", name="mock_check_datatype")
        ]
        self.mocks = {}

        self.start_patchers()
        self.addCleanup(self.stop_patchers)

    def start_patchers(self):

        for i , patcher in enumerate(self.patchers):
            mock = patcher.start()
            try:
                self.mocks [mock.name] = mock
            except AttributeError:
                if isinstance(mock, MagicMock):
                    self.mocks [mock._mock_name] = mock
                else:
                    self.mocks [i] = mock

    def stop_patchers(self):

        for patcher in self.patchers:
            patcher.stop()

    def check_calls(self):

        for name , mock in self.mocks.items():
            if not isinstance(mock, MagicMock):
                continue
            mock.assert_called()
    
    def test_correct_needed_keywords(self):

        pass

    def test_unnecessary_keywords(self):

        pass

    def test_needed_keywords_missing(self):

        pass

    def test_needed_keywords_missing_and_unnecessary_keywords(self):

        pass