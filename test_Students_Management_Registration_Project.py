import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from Students_Management_Registration_Project import delete_account_page

class TestDeleteAccountPage(unittest.TestCase):

    @patch('Students_Management_Registration_Project.tk.Frame')
    @patch('Students_Management_Registration_Project.tk.Label')
    @patch('Students_Management_Registration_Project.tk.Button')
    @patch('Students_Management_Registration_Project.confirmation_box')
    @patch('Students_Management_Registration_Project.sqlite3.connect')
    @patch('Students_Management_Registration_Project.massage_box')
    @patch('Students_Management_Registration_Project.welcome_page')
    def test_delete_account_page(self, mock_welcome_page, mock_massage_box, mock_connect, mock_confirmation_box, mock_button, mock_label, mock_frame):
        # Mocking the tkinter root and pages_fm
        root = MagicMock()
        pages_fm = MagicMock()

        # Setting up the mock confirmation box to return True
        mock_confirmation_box.return_value = True

        # Mocking the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Call the function
        delete_account_page()

        # Check if the confirmation box was called
        mock_confirmation_box.assert_called_once_with(massage='Do You Want to Delete\n Your Account?')

        # Check if the database delete operation was performed
        mock_cursor.execute.assert_called_once_with("DELETE FROM data WHERE id_number == '{student_id}'")

        # Check if the commit and close methods were called on the connection
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

        # Check if the massage box was called with the correct message
        mock_massage_box.assert_called_once_with(massage='Account Deleted Successfully!')

        # Check if the welcome page was called
        mock_welcome_page.assert_called_once()

if __name__ == '__main__':
    unittest.main()