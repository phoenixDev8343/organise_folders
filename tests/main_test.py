```python
# tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.organizer import organize_folder
from src.ui.fancy_ui import display_results
from main import organize_folder as main_organize_folder

class TestMain(unittest.TestCase):

    @patch('pathlib.Path.home')
    def test_downloads_dir(self, mock_path_home):
        mock_path_home.return_value = Path('/home/user')
        downloads_dir = Path.home() / "Downloads"
        self.assertEqual(downloads_dir, Path('/home/user/Downloads'))

    @patch('src.organizer.organize_folder')
    def test_organize_folder(self, mock_organize_folder):
        mock_organize_folder.return_value = ['file1', 'file2']
        downloads_dir = Path('/home/user/Downloads')
        moved_files = main_organize_folder(downloads_dir)
        mock_organize_folder.assert_called_once_with(downloads_dir)
        self.assertEqual(moved_files, ['file1', 'file2'])

    @patch('src.organizer.organize_folder')
    @patch('src.ui.fancy_ui.display_results')
    def test_display_results(self, mock_display_results, mock_organize_folder):
        mock_organize_folder.return_value = ['file1', 'file2']
        downloads_dir = Path('/home/user/Downloads')
        main_organize_folder(downloads_dir)
        mock_display_results.assert_called_once_with(['file1', 'file2'])

    @patch('pathlib.Path.home')
    @patch('src.organizer.organize_folder')
    @patch('src.ui.fancy_ui.display_results')
    def test_main(self, mock_display_results, mock_organize_folder, mock_path_home):
        mock_path_home.return_value = Path('/home/user')
        mock_organize_folder.return_value = ['file1', 'file2']
        mock_display_results.return_value = None
        with patch('builtins.print') as mock_print:
            with patch('__main__.organize_folder', mock_organize_folder):
                with patch('__main__.display_results', mock_display_results):
                    import main
                    mock_organize_folder.assert_called_once_with(Path('/home/user/Downloads'))
                    mock_display_results.assert_called_once_with(['file1', 'file2'])
                    mock_print.assert_called_once_with(['file1', 'file2'])

if __name__ == "__main__":
    unittest.main()
```