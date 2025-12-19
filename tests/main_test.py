```python
# tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.organizer import organize_folder
from src.ui.fancy_ui import display_results
from main import downloads_dir

class TestMain(unittest.TestCase):
    @patch('src.organizer.organize_folder')
    def test_organize_folder_called(self, mock_organize_folder):
        # Arrange
        mock_organize_folder.return_value = ['file1', 'file2']
        
        # Act
        from main import main
        main()

        # Assert
        mock_organize_folder.assert_called_once_with(downloads_dir)

    @patch('src.ui.fancy_ui.display_results')
    @patch('src.organizer.organize_folder')
    def test_display_results_called(self, mock_organize_folder, mock_display_results):
        # Arrange
        mock_organize_folder.return_value = ['file1', 'file2']

        # Act
        from main import main
        main()

        # Assert
        mock_display_results.assert_called_once_with(['file1', 'file2'])

    @patch('src.organizer.organize_folder')
    def test_main_prints_moved_files(self, mock_organize_folder):
        # Arrange
        mock_organize_folder.return_value = ['file1', 'file2']
        import sys
        import io
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # Redirect stdout.

        # Act
        from main import main
        main()

        # Assert
        sys.stdout = sys.__stdout__  # Reset stdout.
        self.assertIn("['file1', 'file2']", capturedOutput.getvalue())

    @patch('src.organizer.organize_folder', side_effect=Exception('Test exception'))
    def test_main_handles_exception(self, mock_organize_folder):
        # Act and Assert
        with self.assertRaises(Exception):
            from main import main
            main()

    def test_downloads_dir_is_users_downloads_folder(self):
        # Arrange and Act
        expected_downloads_dir = Path.home() / "Downloads"

        # Assert
        self.assertEqual(downloads_dir, expected_downloads_dir)

if __name__ == "__main__":
    unittest.main()
```