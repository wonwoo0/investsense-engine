
import unittest
from src.scout_dedup import get_authority_score

class TestScoutDedup(unittest.TestCase):
    def test_get_authority_score_none_date(self):
        # specific signal that caused the crash
        signal = {'link': 'http://example.com', 'date': None}
        try:
            score = get_authority_score(signal)
            self.assertIsInstance(score, float)
        except TypeError:
            self.fail("get_authority_score raised TypeError with None date")

if __name__ == '__main__':
    unittest.main()
