import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.scout_shield as scout_shield

class TestScoutShield(unittest.TestCase):
    def setUp(self):
        # Reset global state before each test
        scout_shield.rate_limit_count = 0
        scout_shield.query_count = 0
    
    @patch('src.scout_shield.DDGS')
    def test_search_risks(self, mock_ddgs_cls):
        mock_ddgs_instance = MagicMock()
        mock_ddgs_cls.return_value.__enter__.return_value = mock_ddgs_instance
        mock_ddgs_cls.return_value.__exit__.return_value = False
        
        mock_ddgs_instance.news.return_value = [
            {"title": "Risk News", "url": "http://example.com"}
        ]
        
        with patch('time.sleep'):  # Skip actual sleeping in tests
            results = scout_shield.search_risks("Test Corp", "TEST")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['asset'], "TEST")
        self.assertEqual(results[0]['risk_level'], "HIGH")

if __name__ == '__main__':
    unittest.main()
