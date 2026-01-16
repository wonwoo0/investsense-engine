import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

logging.getLogger('src.scout_gov').setLevel(logging.CRITICAL)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scout_gov import ScoutGov

class TestScoutGov429Handling(unittest.TestCase):
    def test_429_with_next_access_time(self):
        """Test that 429 response with nextAccessTime sets throttle flag"""
        scout = ScoutGov()
        
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "code": "900804",
            "message": "Message throttled out",
            "description": "You have exceeded your quota",
            "nextAccessTime": "2026-Jan-17 00:00:00+0000 UTC"
        }
        
        with patch('requests.get', return_value=mock_response):
            result = scout._request_with_backoff(
                scout.opps_url, 
                params={"api_key": "test"}, 
                is_sam_api=True
            )
        
        # Should return None and set throttled flag
        self.assertIsNone(result)
        self.assertTrue(scout.sam_throttled)
        self.assertEqual(scout.sam_next_access_time, "2026-Jan-17 00:00:00+0000 UTC")
    
    def test_subsequent_requests_skipped_when_throttled(self):
        """Test that subsequent requests are skipped when throttled"""
        scout = ScoutGov()
        scout.sam_throttled = True
        scout.sam_next_access_time = "2026-Jan-17 00:00:00+0000 UTC"
        
        with patch('requests.get') as mock_get:
            result = scout._request_with_backoff(
                scout.opps_url,
                params={"api_key": "test"},
                is_sam_api=True
            )
            
            # Should not make any HTTP request
            mock_get.assert_not_called()
            self.assertIsNone(result)
    
    def test_caching_prevents_repeated_requests(self):
        """Test that successful responses are cached"""
        scout = ScoutGov()
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            # First request
            result1 = scout._request_with_backoff(
                "http://test.com",
                params={"key": "value"},
                is_sam_api=False
            )
            
            # Second identical request
            result2 = scout._request_with_backoff(
                "http://test.com",
                params={"key": "value"},
                is_sam_api=False
            )
            
            # Should only make one actual HTTP request
            self.assertEqual(mock_get.call_count, 1)
            self.assertEqual(result1, result2)
    
    def test_early_exit_on_throttle(self):
        """Test that fetch_opportunities exits early when throttled"""
        scout = ScoutGov()
        
        # Mock the throttle response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "nextAccessTime": "2026-Jan-17 00:00:00+0000 UTC"
        }
        
        with patch('requests.get', return_value=mock_response):
            with patch.object(scout, '_get_target_keywords', return_value=['keyword1', 'keyword2', 'keyword3']):
                with patch.object(scout, 'fetch_us_spending', return_value=[]):
                    with patch.object(scout, '_save_results'):
                        scout.fetch_opportunities()
        
        # Should have set throttle flag after first failure
        self.assertTrue(scout.sam_throttled)

if __name__ == '__main__':
    unittest.main()
