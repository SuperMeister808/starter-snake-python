
import unittest
from unittest.mock import patch , MagicMock

class TestPushToGit(unittest.TestCase):

    def setUp(self):
        
        self.patchers = [
            patch("emergency_logger.Repo")
        ]

        mocks = {}
        
        for patcher in self.patchers:

            mock = patcher.start()
            mocks ["mock_repo"] = mock

        self.repo_instance = mocks["mock_repo"].return_value
        self.repo_instance.remote = MagicMock()
        origin = self.repo_instance.remote.return_value
        origin.push = MagicMock()

        self.addCleanup(self.stop_patcher)

    def stop_patcher(self):

        for patcher in self.patchers:

            patcher.stop()

    def test_push_on_correct_branch(self):

        pass

    def test_push_on_wrong_branch(self):

        pass
