import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scout_shield import search_risks

class TestScoutShield(unittest.TestCase):
    @patch('src.scout_shield.DDGS')
    def test_search_risks(self, mock_ddgs_cls):
        mock_ddgs_instance = MagicMock()
        mock_ddgs_cls.return_value.__enter__.return_value = mock_ddgs_instance
        
        mock_ddgs_instance.news.return_value = [
            {"title": "Risk News", "url": "http://example.com"}
        ]
        
        results = search_risks("Test Corp", "TEST")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['asset'], "TEST")
        self.assertEqual(results[0]['risk_level'], "HIGH")

if __name__ == '__main__':
    unittest.main()
