"""
Generative Engine Optimization (GEO & AEO) Scoring Engine.
Implements the Princeton GEO-bench (Princeton, IIT Delhi, Allen AI) methodology:
- Share of Model (SoM): % of synthesized LLM responses containing the brand/domain
- Citation Probability Index (CPI): % of brand mentions converting to clickable links
- Extractability Index (EI):
    EI = 0.30 * StatsPresence + 0.30 * AuthorityQuotes + 0.20 * AnswerFirst + 0.20 * StructuredTables
- Composite GEO Score:
    GEO Score = 0.35 * SoM + 0.25 * CPI + 0.25 * EI + 0.15 * TopicalCoverage
- Overall Growth Score:
    Overall Growth Score = 0.50 * SEO Score + 0.50 * GEO Score
"""

def compute_extractability_index(crawl_data):
    """
    Computes the RAG Extractability Index (EI) evaluating how easily RAG parsers
    and LLMs can chunk, extract, and synthesize facts from this document.
    """
    word_count = max(1, crawl_data.get('word_count', 0))
    total_stats = crawl_data.get('total_stats_count', 0)
    geo_blocks = crawl_data.get('geo_blocks', [])
    tables_count = crawl_data.get('tables_count', 0)
    lists_count = crawl_data.get('lists_count', 0)

    # 1. Stats Presence (30% weight): quantitative facts per 300 words
    stats_density = (total_stats / (word_count / 300.0)) if word_count >= 100 else 0
    if stats_density >= 2.0:
        s_stats = 100.0
    elif stats_density >= 1.0:
        s_stats = 80.0
    elif stats_density >= 0.4:
        s_stats = 55.0
    elif total_stats >= 1:
        s_stats = 35.0
    else:
        s_stats = 10.0

    # 2. Authority Quotes & Sources (30% weight)
    citations_count = sum(b.get('citations_count', 0) for b in geo_blocks)
    if citations_count >= 4:
        s_quotes = 100.0
    elif citations_count >= 2:
        s_quotes = 80.0
    elif citations_count == 1:
        s_quotes = 55.0
    else:
        s_quotes = 15.0

    # 3. Answer-First Compliance (20% weight)
    if geo_blocks:
        answer_first_count = sum(1 for b in geo_blocks if b.get('is_answer_first', False) and not b.get('has_fluff', False))
        s_answer_first = round((answer_first_count / len(geo_blocks)) * 100.0, 1)
    else:
        s_answer_first = 30.0

    # 4. Structured Tables & Lists (20% weight)
    if tables_count >= 2:
        s_tables = 100.0
    elif tables_count == 1:
        s_tables = 85.0
    elif lists_count >= 2:
        s_tables = 65.0
    elif lists_count == 1:
        s_tables = 45.0
    else:
        s_tables = 10.0

    ei_score = round(
        0.30 * s_stats +
        0.30 * s_quotes +
        0.20 * s_answer_first +
        0.20 * s_tables,
        1
    )

    details = {
        'stats_presence': s_stats,
        'stats_presence_score': s_stats,
        'authority_quotes': s_quotes,
        'authority_quotes_score': s_quotes,
        'answer_first_compliance': s_answer_first,
        'answer_first_score': s_answer_first,
        'structured_tables': s_tables,
        'structured_tables_score': s_tables,
        'total_stats_found': total_stats,
        'citations_found': citations_count,
        'answer_first_blocks_ratio': f"{sum(1 for b in geo_blocks if b.get('is_answer_first', False))}/{max(1, len(geo_blocks))}"
    }

    return ei_score, details

def compute_share_of_model(crawl_data, probed_trials=None, brand_name=None):
    """
    Computes or estimates Share of Model (SoM).
    If empirical LLM probing is not executed, calculates a deterministic baseline
    based on entity presence, domain authority, and structured data signals.
    """
    if isinstance(probed_trials, list) and len(probed_trials) > 0:
        mentions = sum(1 for t in probed_trials if isinstance(t, dict) and t.get('brand_mentioned', False))
        return round((mentions / len(probed_trials)) * 100.0, 1)

    # Empirical deterministic baseline
    base = 15.0
    if crawl_data.get('existing_schemas'):
        base += 15.0
    if crawl_data.get('brand_mentions_count', 0) >= 3:
        base += 15.0
    if crawl_data.get('word_count', 0) > 600:
        base += 10.0
    if crawl_data.get('robots_data', {}).get('is_ai_friendly', True):
        base += 15.0

    return min(85.0, base)

def compute_citation_probability_index(som_score, crawl_data):
    """
    Computes Citation Probability Index (CPI) measuring whether brand mentions
    convert into clickable hyperlinks and citations in synthesized LLM answers.
    """
    has_canonical = bool(crawl_data.get('canonical_url'))
    has_schema = bool(crawl_data.get('existing_schemas'))
    is_accessible = crawl_data.get('is_accessible', True)

    cpi = som_score * 0.7
    if has_canonical and is_accessible:
        cpi += 15.0
    if has_schema:
        cpi += 10.0

    return round(min(100.0, cpi), 1)

def compute_composite_geo_score(som_score, cpi_score, ei_score, topical_coverage):
    """
    GEO Score = 0.35 * SoM + 0.25 * CPI + 0.25 * EI + 0.15 * TopicalCoverage
    """
    geo_score = round(
        0.35 * som_score +
        0.25 * cpi_score +
        0.25 * ei_score +
        0.15 * topical_coverage,
        1
    )
    return geo_score

def compute_overall_growth_score(seo_score, geo_score):
    """
    Overall Growth Score = 0.50 * SEO Score + 0.50 * GEO Score
    """
    return round(0.50 * seo_score + 0.50 * geo_score, 1)

# Aliases
simulate_share_of_model = compute_share_of_model

