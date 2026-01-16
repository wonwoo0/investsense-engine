import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

logging.getLogger('src.scout_gov').setLevel(logging.CRITICAL)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scout_gov import ScoutGov

class TestScoutGov(unittest.TestCase):
    @patch('src.scout_gov.requests.post')
    def test_fetch_us_spending_null_date(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "Award Amount": 1000000,
                    "Recipient Name": "Test Recipient",
                    "Action Date": None,
                    "Description": "Test Contract"
                }
            ]
        }
        mock_post.return_value = mock_response

        scout = ScoutGov()
        scout.min_value = 100

        start_date = "2023-01-01"
        results = scout.fetch_us_spending(["keyword"], start_date, "2023-01-31")

        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0]['date'], "Date should not be None")
        self.assertEqual(results[0]['date'], start_date, "Should fallback to start_date")

if __name__ == '__main__':
    unittest.main()
