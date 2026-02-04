
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

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
        self.repo_instance.active_branch = MagicMock()
        self.repo_instance.remote = MagicMock()
        self.origin = self.repo_instance.remote.return_value
        self.origin.push = MagicMock()

        self.addCleanup(self.stop_patcher)

    def stop_patcher(self):

        for patcher in self.patchers:

            patcher.stop()

    def test_push_on_correct_branch(self):

        self.repo_instance.active_branch.name = "test_branch"

        EmergencyLogger.push_to_git("/testing...", "test_branch")

        self.repo_instance.remote.assert_called_once_with(name="origin")
        self.origin.push.assert_called_once_with("test_branch")

    def test_push_on_wrong_branch(self):

        self.repo_instance.active_branch.name = "main_branch"

        with self.assertRaises(RuntimeError):
            EmergencyLogger.push_to_git("/testing...", "test_branch")

        self.repo_instance.remote.assert_not_called()
        self.origin.push.assert_not_called()

if __name__ == "__main__":

    unittest.main()
