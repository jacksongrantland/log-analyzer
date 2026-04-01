#!/usr/bin/env python3
"""
Unit tests for the Structured Log Analyzer
"""

import unittest
import tempfile
import os
from analyzer import analyze_log

class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a temporary log file for testing
        self.test_log_content = """2026-04-01 10:32:15 ERROR Failed to connect to database
2026-04-01 10:32:20 INFO Server started
2026-04-01 10:32:30 WARNING High memory usage
2026-04-01 10:32:35 ERROR Failed to connect to database
2026-04-01 10:32:40 INFO User logged in
"""
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        self.test_file.write(self.test_log_content)
        self.test_file.close()

    def tearDown(self):
        # Clean up the temporary file
        os.unlink(self.test_file.name)

    def test_analyze_log_basic(self):
        """Test basic log analysis functionality"""
        result = analyze_log(self.test_file.name)

        self.assertEqual(result['total_lines'], 5)
        self.assertEqual(result['levels']['ERROR'], 2)
        self.assertEqual(result['levels']['WARNING'], 1)
        self.assertEqual(result['levels']['INFO'], 2)

        # Check top messages
        top_messages = result['top_messages']
        self.assertEqual(len(top_messages), 4)  # Should have 4 unique messages
        # Check the most repeated: "FAILED TO CONNECT TO DATABASE" appears twice
        self.assertIn(('FAILED TO CONNECT TO DATABASE', 2), top_messages)

    def test_analyze_log_no_matches(self):
        """Test log file with no matching log levels"""
        no_match_content = """This is just some text
Another line without keywords
Yet another line
"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        temp_file.write(no_match_content)
        temp_file.close()

        try:
            result = analyze_log(temp_file.name)
            self.assertEqual(result['total_lines'], 3)
            self.assertEqual(result['levels']['ERROR'], 0)
            self.assertEqual(result['levels']['WARNING'], 0)
            self.assertEqual(result['levels']['INFO'], 0)
            self.assertEqual(result['top_messages'], [])
        finally:
            os.unlink(temp_file.name)

    def test_analyze_log_file_not_found(self):
        """Test handling of non-existent file"""
        with self.assertRaises(SystemExit):
            analyze_log('non_existent_file.log')

if __name__ == '__main__':
    unittest.main()