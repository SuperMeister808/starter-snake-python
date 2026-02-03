
import unittest
from unittest.mock import patch , MagicMock

from emergency_logger import EmergencyLogger

class TestUploadToGit(unittest.TestCase):

    #testet nur Behaviour nicht Funktion
    
    @patch("emergency_logger.Repo")
    def test_correct_branch(self, mock_repo):

        #man ruft den mock auf eine Instanz auf
        mock_repo_instance = mock_repo.return_value
        #ruft eine Instanz eines Mock Objektes auf
        mock_repo_instance.git.add = MagicMock()
        mock_repo_instance.index.commit = MagicMock()
        mock_repo_instance.active_branch = MagicMock()
        #man kann Attribute definieren, da mock Objekte ein dynamisches __dict__ besitzen
        mock_repo_instance.active_branch.name = "test_branch"

        EmergencyLogger.upload_to_git("/testing...", "testing...", "test_branch")

        mock_repo_instance.git.add.assert_called_once_with(A=True)
        mock_repo_instance.git.commit.assert_called_once_with("-m", "testing...", "--allow-empty")



    def test_wrong_branch(self):

        pass

if __name__ == "__main__":

    unittest.main()