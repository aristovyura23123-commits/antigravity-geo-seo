#!/usr/bin/env python3
"""
Antigravity AI Multi-Agent GEO & SEO Engine — Unified CLI Interface.
Implements the end-to-end DAG workflow:
1. Crawling & DOM / Robot extraction
2. Deterministic SEO mathematical scoring
3. Princeton GEO-bench scoring (SoM, CPI, EI)
4. Non-linear Opportunity detection & prioritization: (Impact * Conf) / (Effort^1.2) * Urgency
5. Production-grade Schema.org JSON-LD & Answer-First artifact synthesis
6. QA Gate validation & fact-checking
7. Interactive 7-section HTML report, JSON & CSV export
"""

import sys
import os
import json
import argparse
from urllib.parse import urlparse

# Ensure local scripts can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.crawler import crawl_and_extract_signals
from scripts.seo_scoring import compute_all_seo_scores
from scripts.geo_scoring import (
    compute_extractability_index,
    simulate_share_of_model,
    compute_citation_probability_index,
    compute_composite_geo_score,
    compute_overall_growth_score
)
from scripts.opportunity_engine import detect_seo_geo_opportunities
from scripts.artifact_generator import generate_all_artifacts
from scripts.qa_validator import run_qa_certification
from scripts.reporter import (
    generate_html_report,
    generate_json_report,
    export_opportunities_csv
)

def run_pipeline(url, brand_name=None, output_html=None, output_json=None, output_csv=None):
    """
    Executes the autonomous audit and optimization pipeline.
    """
    print("=" * 70)
    print("🚀  ANTIGRAVITY AI MULTI-AGENT GEO & SEO ENGINE")
    print("    Enterprise Princeton GEO-bench & Mathematical Scoring Framework")
    print("=" * 70)
    print(f"[*] Анализ целевого URL: {url}")
    if brand_name:
        print(f"[*] Целевой бренд/сущность: {brand_name}")

    # 1. Crawl & Signal Extraction
    print("\n[1/6] 🌐 Запуск агента сбора данных (DOM, Robots.txt, Schema.org)...")
    crawl_data = crawl_and_extract_signals(url, brand_name=brand_name)
    if not crawl_data.get('is_accessible'):
        print(f"[-] Внимание: код ответа {crawl_data.get('status_code')}. Анализ продолжается с учетом штрафов.")

    # 2. SEO Mathematical Scoring
    print("[2/6] ⚙️  Расчет детерминированных SEO-показателей (Technical, Content, Authority)...")
    seo_scores = compute_all_seo_scores(crawl_data)

    # 3. Princeton GEO-bench Scoring
    print("[3/6] 🧠 Расчет Princeton GEO-bench метрик (SoM, CPI, EI)...")
    ei_score, ei_details = compute_extractability_index(crawl_data)
    
    som_score = simulate_share_of_model(crawl_data, brand_name=brand_name)
    cpi_score = compute_citation_probability_index(som_score, crawl_data)
    
    # Use content topical coverage proxy
    topical_cov = seo_scores.get('content_score', 60.0)
    geo_score = compute_composite_geo_score(som_score, cpi_score, ei_score, topical_cov)
    
    overall_growth_score = compute_overall_growth_score(seo_scores['composite_seo_score'], geo_score)

    geo_scores = {
        'overall_growth_score': overall_growth_score,
        'composite_geo_score': geo_score,
        'som_score': som_score,
        'cpi_score': cpi_score,
        'ei_score': ei_score,
        'subscores': ei_details
    }

    # 4. Opportunity Detection & Ranking
    print("[4/6] 🎯 Генерация и приоритизация каталога возможностей (Priority Formula)...")
    opportunities = detect_seo_geo_opportunities(crawl_data, seo_scores, geo_scores)

    # 5. Production Artifact Synthesis
    print("[5/6] 📦 Синтез артефактов внедрения (JSON-LD Schemas, Answer-First модули)...")
    artifacts = generate_all_artifacts(crawl_data)

    # 6. QA Gate & Fact-Checking
    print("[6/6] 🛡️  Прохождение шлюза качества (QA Gate Certification)...")
    qa_results = run_qa_certification(crawl_data, artifacts)

    # File outputs
    domain_clean = urlparse(url).netloc.replace(':', '_')
    html_path = output_html or f"geo_seo_report_{domain_clean}.html"
    json_path = output_json or f"geo_seo_report_{domain_clean}.json"
    csv_path = output_csv or f"opportunities_{domain_clean}.csv"

    # Generate Reports
    html_content = generate_html_report(crawl_data, seo_scores, geo_scores, opportunities, artifacts, qa_results)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    json_data = generate_json_report(crawl_data, seo_scores, geo_scores, opportunities, artifacts, qa_results)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    export_opportunities_csv(opportunities, csv_path)

    # Output Terminal Summary
    print("\n" + "=" * 70)
    print("📊 СВОДНЫЕ РЕЗУЛЬТАТЫ АУДИТА (EXECUTIVE SUMMARY)")
    print("=" * 70)
    print(f"Overall Growth Score : {overall_growth_score}/100  (0.50*SEO + 0.50*GEO)")
    print(f"Traditional SEO Score: {seo_scores['composite_seo_score']}/100  [Техника: {seo_scores['technical_score']} | Контент: {seo_scores['content_score']} | Ссылки: {seo_scores['authority_score']}]")
    print(f"Generative Engine (GEO): {geo_score}/100  [SoM: {som_score}% | CPI: {cpi_score}% | EI: {ei_score}]")
    print(f"QA Gate Certification: {'✅ ПРОЙДЕН' if qa_results['qa_passed'] else '⚠️ ТРЕБУЕТ ВНИМАНИЯ'} ({qa_results['qa_score']}%)")
    print("-" * 70)
    print(f"Выявлено возможностей для роста: {len(opportunities)}")
    if opportunities:
        print("\nТоп-3 приоритетных задачи (по Priority Score):")
        for i, opp in enumerate(opportunities[:3], 1):
            print(f" {i}. [{opp['id']}] {opp['title']}")
            print(f"    Impact: {opp['impact']} | Effort: {opp['effort']} | Urgency: {opp['urgency']} => Priority Score: {opp['priority_score']}")

    print("\n" + "=" * 70)
    print("📁 СФОРМИРОВАННЫЕ ОТЧЕТЫ И АРТЕФАКТЫ:")
    print(f"  ● Интерактивный HTML дашборд: {os.path.abspath(html_path)}")
    print(f"  ● Машиночитаемый JSON отчет:  {os.path.abspath(json_path)}")
    print(f"  ● CSV каталог для бэклога:    {os.path.abspath(csv_path)}")
    print("=" * 70)

    return {
        'overall_growth_score': overall_growth_score,
        'seo_scores': seo_scores,
        'geo_scores': geo_scores,
        'opportunities': opportunities,
        'qa_results': qa_results,
        'html_path': os.path.abspath(html_path),
        'json_path': os.path.abspath(json_path),
        'csv_path': os.path.abspath(csv_path)
    }

def main():
    parser = argparse.ArgumentParser(
        description="Antigravity Enterprise GEO & SEO Autonomous Multi-Agent Tool"
    )
    parser.add_argument('--url', '-u', required=True, help="Целевой URL сайта для аудита и оптимизации")
    parser.add_argument('--brand', '-b', default=None, help="Название бренда или ключевой сущности (опционально)")
    parser.add_argument('--output-html', help="Путь для сохранения интерактивного HTML отчета")
    parser.add_argument('--output-json', help="Путь для сохранения JSON отчета")
    parser.add_argument('--output-csv', help="Путь для сохранения CSV бэклога")

    args = parser.parse_args()

    # Prepend scheme if missing
    target_url = args.url
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    try:
        run_pipeline(
            url=target_url,
            brand_name=args.brand,
            output_html=args.output_html,
            output_json=args.output_json,
            output_csv=args.output_csv
        )
    except Exception as e:
        print(f"\n❌ Ошибка выполнения пайплайна: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
