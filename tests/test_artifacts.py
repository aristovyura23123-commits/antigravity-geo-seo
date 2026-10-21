"""
Unit tests for Artifact Generation and QA Gate Validator.
"""

import unittest
from scripts.artifact_generator import (
    generate_organization_schema,
    generate_faq_schema,
    generate_article_or_webpage_schema,
    generate_answer_first_rewrites,
    generate_all_artifacts
)
from scripts.qa_validator import (
    validate_json_ld_schema,
    validate_placeholders,
    validate_answer_first_module,
    run_qa_certification
)

class TestArtifactsAndQA(unittest.TestCase):

    def setUp(self):
        self.crawl_mock = {
            'url': 'https://example-shop.ru/catalog/baby',
            'domain': 'example-shop.ru',
            'brand_name': 'Example Shop',
            'status_code': 200,
            'is_accessible': True,
            'title': 'Детские товары премиум класса — Example Shop',
            'meta_description': 'Купить лучшие детские товары с быстрой доставкой по РФ.',
            'canonical_url': 'https://example-shop.ru/catalog/baby',
            'h1_tags': ['Детские товары и аксессуары'],
            'h2_tags': ['Как выбрать коляску для новорожденного', 'Преимущества сертифицированных материалов'],
            'word_count': 750,
            'total_stats_count': 6,
            'tables_count': 1,
            'existing_schemas': []
        }

    def test_schema_generation_and_ast_validation(self):
        artifacts = generate_all_artifacts(self.crawl_mock)
        combined = artifacts['combined_json_ld']
        
        self.assertEqual(combined['@context'], 'https://schema.org')
        self.assertIn('@graph', combined)
        self.assertEqual(len(combined['@graph']), 3)

        passed, errs, warns = validate_json_ld_schema(combined)
        self.assertTrue(passed, f"JSON-LD Schema validation failed: {errs}")

    def test_answer_first_compliance(self):
        rewrites = generate_answer_first_rewrites(self.crawl_mock)
        self.assertGreaterEqual(len(rewrites), 1)
        for r in rewrites:
            passed, errs, warns = validate_answer_first_module(r)
            self.assertTrue(passed)
            # check that word count is in reasonable range
            self.assertGreaterEqual(r['word_count'], 30)
            self.assertLessEqual(r['word_count'], 75)

    def test_qa_certification_pass(self):
        artifacts = generate_all_artifacts(self.crawl_mock)
        qa_res = run_qa_certification(self.crawl_mock, artifacts)
        self.assertTrue(qa_res['qa_passed'])
        self.assertGreaterEqual(qa_res['qa_score'], 80.0)

if __name__ == '__main__':
    unittest.main()
