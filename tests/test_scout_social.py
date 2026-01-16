import pytest
from unittest.mock import MagicMock, patch
import sys
# Ensure src is in path
sys.path.append('.')

from src.scout_social import ScoutSocial

def test_save_results_success():
    scout = ScoutSocial()
    results = [{"title": "Test"}]
    
    # We mock open to ensure we don't write files and to verify the call
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        # We also need to ensure the directory exists or mkdir is mocked if used?
        # The code just does open(filename, 'w').
        # It assumes PATHS['INCOMING'] exists.
        
        scout._save_results(results)
        
        # If we get here without NameError, it worked (partially)
        mock_open.assert_called_once()
