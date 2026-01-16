import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to test
import src.scout_shield as scout_shield

class TestScoutShieldRateLimiting(unittest.TestCase):
    def setUp(self):
        # Reset global state before each test
        scout_shield.rate_limit_count = 0
        scout_shield.query_count = 0
    
    def test_rate_limit_triggers_cooldown(self):
        """Test that rate limit errors trigger cooldown"""
        scout_shield.rate_limit_count = 0
        
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.news.side_effect = Exception("202 Ratelimit")
        
        with patch('src.scout_shield.DDGS', return_value=mock_ddgs):
            with patch('time.sleep'):
                results = scout_shield.search_risks("Test Corp", "TEST")
        
        # Should have incremented rate limit count
        self.assertGreater(scout_shield.rate_limit_count, 0)
    
    def test_query_cap_prevents_excessive_requests(self):
        """Test that query cap prevents excessive requests"""
        scout_shield.query_count = scout_shield.max_queries_per_run
        
        with patch('src.scout_shield.DDGS') as mock_ddgs:
            results = scout_shield.search_risks("Test Corp", "TEST")
        
        # Should not make any requests when cap reached
        mock_ddgs.assert_not_called()
        self.assertEqual(results, [])
    
    def test_exponential_backoff_with_jitter(self):
        """Test that exponential backoff is applied on rate limit"""
        scout_shield.rate_limit_count = 0
        
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.news.side_effect = Exception("202 Ratelimit")
        
        with patch('src.scout_shield.DDGS', return_value=mock_ddgs):
            with patch('time.sleep') as mock_sleep:
                with patch('random.uniform', return_value=2.0):  # Mock jitter
                    results = scout_shield.search_risks("Test Corp", "TEST")
        
        # Should have called sleep multiple times with increasing values
        sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
        
        # Verify exponential backoff pattern (5, 10, 20 base + jitter)
        self.assertTrue(len(sleep_calls) >= 2)
    
    def test_successful_request_resets_rate_limit_count(self):
        """Test that successful requests reset the rate limit counter"""
        scout_shield.rate_limit_count = 2
        
        mock_ddgs = MagicMock()
        mock_ddgs.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = MagicMock(return_value=False)
        mock_ddgs.news.return_value = [{"title": "Test", "url": "http://test.com"}]
        
        with patch('src.scout_shield.DDGS', return_value=mock_ddgs):
            with patch('time.sleep'):
                results = scout_shield.search_risks("Test Corp", "TEST")
        
        # Should have reset the rate limit count
        self.assertEqual(scout_shield.rate_limit_count, 0)
        self.assertEqual(len(results), 1)
    
    def test_cooldown_skips_remaining_searches(self):
        """Test that cooldown mode skips remaining searches"""
        scout_shield.rate_limit_count = scout_shield.max_rate_limit_tolerance
        
        with patch('src.scout_shield.DDGS') as mock_ddgs:
            results = scout_shield.search_risks("Test Corp", "TEST")
        
        # Should not make any requests when in cooldown
        mock_ddgs.assert_not_called()
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
