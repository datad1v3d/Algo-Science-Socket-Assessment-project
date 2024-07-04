"""
this module tests the check_string_in_file function using various test cases
"""

import sys
import os
import unittest
# to enable python check the my_project directory to be able to import from server
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from my_server.server import FileHandler

class TestCheckStringInFile(unittest.TestCase):
    """ class to test the check string in file function in server.py """
    def test_string_exists(self):
        """Test case when the string exists in the file"""
        client_string = "10;0;1;16;0;7;3;0;"
        expected_result = "STRING EXISTS\n"
        actual_result = FileHandler().check_string_in_file(client_string)
        self.assertEqual(actual_result, expected_result)

    def test_string_not_found(self):
        """Test case when the string does not exist in the file"""
        client_string = "Hello"
        expected_result = "STRING NOT FOUND\n"
        actual_result = FileHandler().check_string_in_file(client_string)
        self.assertEqual(actual_result, expected_result)

    def test_partial_string_match(self):
        """Test case when a partial match of the string exists in the file"""
        client_string = "10;0;1;16;0;"
        expected_result = "STRING NOT FOUND\n"
        actual_result = FileHandler().check_string_in_file(client_string)
        self.assertEqual(actual_result, expected_result)

if __name__ == "__main__":
    unittest.main()
