"""
Unit tests for Technical and GEO mathematical scoring formulas.
"""

import unittest
from scripts.seo_scoring import (
    compute_technical_seo_score,
    compute_content_seo_score,
    compute_authority_score,
    compute_all_seo_scores
)
from scripts.geo_scoring import (
    compute_extractability_index,
    compute_citation_probability_index,
    compute_composite_geo_score,
    compute_overall_growth_score
)
from scripts.opportunity_engine import calculate_priority_score

class TestScoring(unittest.TestCase):

    def test_priority_score_formula(self):
        # Priority Score = (Impact * Confidence) / (Effort ^ 1.2) * Urgency
        impact = 8.5
        confidence = 0.90
        effort = 3.0
        urgency = 1.0
        # 3.0 ^ 1.2 = 3.73719
        # (8.5 * 0.9) / 3.73719 * 1.0 = 7.65 / 3.73719 = 2.04699 => 2.05
        score = calculate_priority_score(impact, confidence, effort, urgency)
        self.assertEqual(score, 2.05)

    def test_overall_growth_score_formula(self):
        # Overall = 0.50 * SEO + 0.50 * GEO
        seo = 64.0
        geo = 46.0
        overall = compute_overall_growth_score(seo, geo)
        self.assertEqual(overall, 55.0)

    def test_composite_geo_score_formula(self):
        # GEO = 0.35 * SoM + 0.25 * CPI + 0.25 * EI + 0.15 * TopicalCoverage
        som = 20.0
        cpi = 30.0
        ei = 60.0
        topical = 70.0
        # 0.35 * 20 = 7.0
        # 0.25 * 30 = 7.5
        # 0.25 * 60 = 15.0
        # 0.15 * 70 = 10.5
        # Sum = 7.0 + 7.5 + 15.0 + 10.5 = 40.0
        geo = compute_composite_geo_score(som, cpi, ei, topical)
        self.assertEqual(geo, 40.0)

    def test_technical_seo_penalties(self):
        crawl_mock = {
            'is_accessible': True,
            'is_noindex': False,
            'canonical_url': 'https://example.com/page',
            'h1_count': 1,
            'title_length': 45,
            'meta_description_length': 150,
            'images_count': 2,
            'images_missing_alt_count': 0,
            'fetch_time_sec': 0.4,
            'robots_data': {'blocked_bots': []}
        }
        score, penalties = compute_technical_seo_score(crawl_mock)
        self.assertEqual(score, 100)
        self.assertEqual(len(penalties), 0)

        # Inject AI bot block
        crawl_mock['robots_data']['blocked_bots'] = ['GPTBot']
        score_blocked, penalties_blocked = compute_technical_seo_score(crawl_mock)
        self.assertEqual(score_blocked, 85)


if __name__ == '__main__':
    unittest.main()
