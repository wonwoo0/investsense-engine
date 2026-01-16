import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scout_social import ScoutSocial

class TestScoutSocialCircuitBreaker(unittest.TestCase):
    def test_circuit_breaker_trips_after_threshold(self):
        """Test that circuit breaker trips after consecutive 403s"""
        scout = ScoutSocial()
        scout.circuit_breaker_threshold = 3
        
        mock_response = MagicMock()
        mock_response.status_code = 403
        
        with patch('requests.get', return_value=mock_response):
            with patch.object(scout, '_get_target_keywords', return_value=['kw1', 'kw2', 'kw3', 'kw4']):
                with patch.object(scout, '_save_results'):
                    scout.fetch_reddit()
        
        # Circuit should be open after 3 consecutive 403s
        self.assertTrue(scout.circuit_open)
        self.assertEqual(scout.consecutive_403s, 3)
    
    def test_circuit_breaker_resets_on_success(self):
        """Test that consecutive 403 count resets on successful request"""
        scout = ScoutSocial()
        
        mock_403 = MagicMock()
        mock_403.status_code = 403
        
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"data": {"children": []}}
        
        with patch('requests.get', side_effect=[mock_403, mock_403, mock_200]):
            with patch.object(scout, '_get_target_keywords', return_value=['kw1', 'kw2', 'kw3']):
                with patch.object(scout, '_save_results'):
                    scout.fetch_reddit()
        
        # Should reset counter after success
        self.assertEqual(scout.consecutive_403s, 0)
        self.assertFalse(scout.circuit_open)
    
    def test_exponential_backoff_on_403(self):
        """Test that exponential backoff is applied on 403"""
        scout = ScoutSocial()
        
        mock_response = MagicMock()
        mock_response.status_code = 403
        
        with patch('requests.get', return_value=mock_response):
            with patch('time.sleep') as mock_sleep:
                with patch.object(scout, '_get_target_keywords', return_value=['kw1', 'kw2']):
                    with patch.object(scout, '_save_results'):
                        scout.fetch_reddit()
                
                # Should have called sleep with increasing wait times
                # First 403: sleep(2) for politeness, then sleep(2) for backoff
                # Second 403: sleep(2) for politeness, then sleep(4) for backoff
                # Third would trip circuit breaker
                sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
                
                # We expect at least some exponential backoff calls
                self.assertTrue(any(t > 2 for t in sleep_calls), 
                               f"Expected exponential backoff but got: {sleep_calls}")
    
    def test_circuit_breaker_skips_remaining_keywords(self):
        """Test that remaining keywords are skipped when circuit opens"""
        scout = ScoutSocial()
        
        mock_response = MagicMock()
        mock_response.status_code = 403
        
        keywords = ['kw1', 'kw2', 'kw3', 'kw4', 'kw5']
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            with patch.object(scout, '_get_target_keywords', return_value=keywords):
                with patch.object(scout, '_save_results'):
                    with patch('time.sleep'):  # Skip actual sleeping in test
                        scout.fetch_reddit()
        
        # Should stop after circuit breaker threshold (3), not process all 5
        self.assertTrue(scout.circuit_open)
        # We make 3 requests before circuit trips
        self.assertEqual(mock_get.call_count, 3)

if __name__ == '__main__':
    unittest.main()
