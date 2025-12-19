```python
# tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.organizer import organize_folder
from src.ui.fancy_ui import display_results
from main import downloads_dir

class TestMainFunctions(unittest.TestCase):

    @patch('src.organizer.organize_folder')
    @patch('src.ui.fancy_ui.display_results')
    def test_main_flow(self, mock_display_results, mock_organize_folder):
        # Arrange
        mock_moved_files = ['file1', 'file2']
        mock_organize_folder.return_value = mock_moved_files

        # Act
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                with patch('main.downloads_dir', Path.home() / "Downloads"):
                    import main

        # Assert
        mock_organize_folder.assert_called_once_with(downloads_dir)
        mock_display_results.assert_called_once_with(mock_moved_files)
        mock_print.assert_called_once_with(mock_moved_files)

    @patch('src.organizer.organize_folder')
    def test_organize_folder_called_with_downloads_dir(self, mock_organize_folder):
        # Arrange
        mock_moved_files = ['file1', 'file2']
        mock_organize_folder.return_value = mock_moved_files

        # Act
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                with patch('main.downloads_dir', downloads_dir):
                    import main

        # Assert
        mock_organize_folder.assert_called_once_with(downloads_dir)

    @patch('src.organizer.organize_folder')
    @patch('src.ui.fancy_ui.display_results')
    def test_display_results_called_with_moved_files(self, mock_display_results, mock_organize_folder):
        # Arrange
        mock_moved_files = ['file1', 'file2']
        mock_organize_folder.return_value = mock_moved_files

        # Act
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                with patch('main.downloads_dir', downloads_dir):
                    import main

        # Assert
        mock_display_results.assert_called_once_with(mock_moved_files)

    def test_downloads_dir_set_correctly(self):
        # Arrange
        expected_downloads_dir = Path.home() / "Downloads"

        # Act
        actual_downloads_dir = downloads_dir

        # Assert
        self.assertEqual(actual_downloads_dir, expected_downloads_dir)

    @patch('src.organizer.organize_folder')
    @patch('src.ui.fancy_ui.display_results')
    def test_empty_moved_files(self, mock_display_results, mock_organize_folder):
        # Arrange
        mock_moved_files = []
        mock_organize_folder.return_value = mock_moved_files

        # Act
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                with patch('main.downloads_dir', downloads_dir):
                    import main

        # Assert
        mock_organize_folder.assert_called_once_with(downloads_dir)
        mock_display_results.assert_called_once_with(mock_moved_files)
        mock_print.assert_called_once_with(mock_moved_files)

    @patch('src.organizer.organize_folder')
    @patch('src.ui.fancy_ui.display_results')
    def test_organize_folder_throws_exception(self, mock_display_results, mock_organize_folder):
        # Arrange
        mock_organize_folder.side_effect = Exception('Test exception')

        # Act and Assert
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                with patch('main.downloads_dir', downloads_dir):
                    with self.assertRaises(Exception):
                        import main

    @patch('src.ui.fancy_ui.display_results')
    def test_display_results_throws_exception(self, mock_display_results):
        # Arrange
        mock_moved_files = ['file1', 'file2']
        mock_display_results.side_effect = Exception('Test exception')
        with patch('src.organizer.organize_folder') as mock_organize_folder:
            mock_organize_folder.return_value = mock_moved_files

        # Act and Assert
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                with patch('main.downloads_dir', downloads_dir):
                    with self.assertRaises(Exception):
                        import main

if __name__ == "__main__":
    unittest.main()
```