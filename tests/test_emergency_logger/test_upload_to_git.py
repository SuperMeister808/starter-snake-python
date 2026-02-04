
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

class TestUploadToGit(unittest.TestCase):

    def setUp(self):
        

        self.patchers = [
            patch("emergency_logger.Repo")
        ]

        mocks = {}

        for patcher in self.patchers:
        
            mock = patcher.start()

            mocks ["mock_repo"] = mock

        #man erzeugt eine Instanz des Mock Objektes, da die Klasse repo auch als Instanz aufgerufen wird
        self.mock_repo_instance = mocks["mock_repo"].return_value
        #man kann Attribute von mock Objekten definieren, nötig für den Test-Code
        self.mock_repo_instance.git.add = MagicMock()
        self.mock_repo_instance.index.commit = MagicMock()
        self.mock_repo_instance.active_branch = MagicMock()

        self.addCleanup(self.stop_patcher)

    def stop_patcher(self):

        for patcher in self.patchers:

            patcher.stop()

    #testet nur Behaviour nicht Funktion
    
    def test_correct_branch(self):

        self.mock_repo_instance.active_branch.name = "test_branch"

        EmergencyLogger.upload_to_git("/testing...", "testing...", "test_branch")

        self.mock_repo_instance.git.add.assert_called_once_with(A=True)
        self.mock_repo_instance.git.commit.assert_called_once_with("-m", "testing...", "--allow-empty")


    def test_wrong_branch(self):

        self.mock_repo_instance.active_branch.name = "main_branch"

        with self.assertRaises(RuntimeError):
            EmergencyLogger.upload_to_git("/testing...", "testing...", "test_branch")

        self.mock_repo_instance.git.add.assert_not_called()
        self.mock_repo_instance.git.commit.assert_not_called()

if __name__ == "__main__":

    unittest.main()