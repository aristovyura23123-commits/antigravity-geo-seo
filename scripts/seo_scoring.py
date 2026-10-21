"""
Deterministic Technical and Content SEO Scoring Engine.
Implements mathematical formulas from the AI Multi-Agent SEO/GEO Specification:
- Technical SEO Score: 100 - sum(min(Penalty_i * Count_i, MaxPenalty_i))
- Content Score: 0.35 * TopicalCoverage + 0.25 * StructureScore + 0.20 * Readability + 0.20 * IntentMatch
- Authority Score: Link profile, schema presence, and internal cohesion
- Composite SEO Score: 0.40 * Technical + 0.40 * Content + 0.20 * Authority
"""

def compute_technical_seo_score(crawl_data):
    """
    Computes deterministic Technical SEO Score with exact itemized deductions.
    """
    score = 100
    penalties = []

    # 1. Critical HTTP & Access
    if not crawl_data.get('is_accessible', True):
        p = 40
        score -= p
        penalties.append({'factor': 'HTTP Status Code', 'deduction': p, 'reason': f"Страница вернула ошибку {crawl_data.get('status_code', 500)}"})

    if crawl_data.get('is_noindex', False):
        p = 40
        score -= p
        penalties.append({'factor': 'Meta Robots Noindex', 'deduction': p, 'reason': "Страница закрыта от индексации директивой noindex"})

    # 2. AI Crawlers Accessibility (Robots.txt)
    robots = crawl_data.get('robots_data', {})
    blocked_bots = robots.get('blocked_bots', [])
    if blocked_bots:
        p = 15
        score -= p
        penalties.append({'factor': 'Robots.txt AI Crawlers Blocked', 'deduction': p, 'reason': f"Блокировка поисковых LLM-краулеров: {', '.join(blocked_bots)}"})

    # 3. Canonical tag
    canon = crawl_data.get('canonical_url', '')
    if not canon:
        p = 8
        score -= p
        penalties.append({'factor': 'Missing Canonical', 'deduction': p, 'reason': "Отсутствует тег rel=canonical"})

    # 4. Heading H1
    h1_count = crawl_data.get('h1_count', 0)
    if h1_count == 0:
        p = 10
        score -= p
        penalties.append({'factor': 'Missing H1', 'deduction': p, 'reason': "На странице отсутствует главный заголовок H1"})
    elif h1_count > 1:
        p = 5
        score -= p
        penalties.append({'factor': 'Multiple H1', 'deduction': p, 'reason': f"Найдено {h1_count} тегов H1 (рекомендуется ровно один)"})

    # 5. Title Tag
    t_len = crawl_data.get('title_length', 0)
    if t_len == 0:
        p = 15
        score -= p
        penalties.append({'factor': 'Empty Title', 'deduction': p, 'reason': "Отсутствует тег <title>"})
    elif t_len < 20:
        p = 5
        score -= p
        penalties.append({'factor': 'Short Title', 'deduction': p, 'reason': f"Тег Title слишком короткий ({t_len} символов, мин. 20)"})
    elif t_len > 90:
        p = 3
        score -= p
        penalties.append({'factor': 'Long Title', 'deduction': p, 'reason': f"Тег Title слишком длинный ({t_len} символов, риск усечения в SERP)"})

    # 6. Meta Description
    d_len = crawl_data.get('meta_description_length', 0)
    if d_len == 0:
        p = 10
        score -= p
        penalties.append({'factor': 'Missing Meta Description', 'deduction': p, 'reason': "Отсутствует мета-описание description"})
    elif d_len < 50:
        p = 4
        score -= p
        penalties.append({'factor': 'Short Meta Description', 'deduction': p, 'reason': f"Мета-описание слишком короткое ({d_len} символов)"})

    # 7. Images ALT
    missing_alt = crawl_data.get('images_missing_alt_count', 0)
    total_img = crawl_data.get('images_count', 0)
    if total_img > 0 and (missing_alt / total_img) > 0.3:
        p = 5
        score -= p
        penalties.append({'factor': 'Missing Image ALT', 'deduction': p, 'reason': f"{missing_alt} из {total_img} изображений не имеют атрибута alt"})

    # 8. Server latency / TTFB proxy
    fetch_time = crawl_data.get('fetch_time_sec', 0.5)
    if fetch_time > 3.0:
        p = 12
        score -= p
        penalties.append({'factor': 'High Server Response Time', 'deduction': p, 'reason': f"Время ответа сервера составило {fetch_time} с (норма до 1.5 с)"})
    elif fetch_time > 1.8:
        p = 6
        score -= p
        penalties.append({'factor': 'Moderate Response Time', 'deduction': p, 'reason': f"Время ответа сервера {fetch_time} с"})

    final_tech_score = max(0, min(100, score))
    return final_tech_score, penalties

def compute_content_seo_score(crawl_data):
    """
    Computes Content Score: 0.35 * TopicalCoverage + 0.25 * StructureScore + 0.20 * Readability + 0.20 * IntentMatch.
    """
    # 1. Topical Coverage (word count & depth proxy)
    wc = crawl_data.get('word_count', 0)
    if wc >= 800:
        topical = 95.0
    elif wc >= 450:
        topical = 80.0
    elif wc >= 250:
        topical = 65.0
    elif wc >= 100:
        topical = 45.0
    else:
        topical = 20.0

    # 2. Structure Score (H1, H2, H3, Lists, Tables)
    h2_count = crawl_data.get('h2_count', 0)
    h3_count = crawl_data.get('h3_count', 0)
    lists_count = crawl_data.get('lists_count', 0)
    tables_count = crawl_data.get('tables_count', 0)

    structure_pts = 0
    if crawl_data.get('h1_count', 0) == 1:
        structure_pts += 25
    if h2_count >= 2:
        structure_pts += 25
    elif h2_count == 1:
        structure_pts += 15
    if h3_count >= 1:
        structure_pts += 15
    if lists_count >= 1:
        structure_pts += 15
    if tables_count >= 1:
        structure_pts += 20
    structure = min(100.0, float(structure_pts))

    # 3. Readability (Flesch score normalized)
    raw_flesch = crawl_data.get('readability_flesch', 60.0)
    if 45.0 <= raw_flesch <= 75.0:
        readability = 100.0
    elif 30.0 <= raw_flesch < 45.0 or 75.0 < raw_flesch <= 85.0:
        readability = 80.0
    else:
        readability = 55.0

    # 4. Intent Match (presence of direct actionable headings & questions)
    geo_blocks = crawl_data.get('geo_blocks', [])
    answer_first_count = sum(1 for b in geo_blocks if b.get('is_answer_first', False))
    total_blocks = max(1, len(geo_blocks))
    intent = min(100.0, max(40.0, (answer_first_count / total_blocks) * 100.0))

    final_content_score = round(
        0.35 * topical +
        0.25 * structure +
        0.20 * readability +
        0.20 * intent,
        1
    )

    details = {
        'topical_coverage': topical,
        'structure_score': structure,
        'readability_score': readability,
        'intent_match': intent
    }

    return final_content_score, details

def compute_authority_score(crawl_data):
    """
    Computes Authority Score based on internal linking density,
    presence of structured data (JSON-LD schemas), and outbound citations.
    """
    schemas = crawl_data.get('existing_schemas', [])
    int_links = crawl_data.get('internal_links_count', 0)
    ext_links = crawl_data.get('external_links_count', 0)

    score = 40.0  # baseline
    if schemas:
        score += 25.0
    if int_links >= 15:
        score += 20.0
    elif int_links >= 5:
        score += 10.0
    if ext_links >= 1:
        score += 15.0

    return min(100.0, score)

def compute_composite_seo_score(tech_score, content_score, authority_score):
    """
    Total SEO Score = 0.40 * Technical + 0.40 * Content + 0.20 * Authority
    """
    composite = round(
        0.40 * tech_score +
        0.40 * content_score +
        0.20 * authority_score,
        1
    )
    return composite

def compute_all_seo_scores(crawl_data):
    """
    Computes all SEO components and returns a unified dictionary.
    """
    tech_score, penalties = compute_technical_seo_score(crawl_data)
    content_score, content_subscores = compute_content_seo_score(crawl_data)
    auth_score = compute_authority_score(crawl_data)
    composite = compute_composite_seo_score(tech_score, content_score, auth_score)

    return {
        'technical_score': tech_score,
        'content_score': content_score,
        'authority_score': auth_score,
        'composite_seo_score': composite,
        'penalties': penalties,
        'content_subscores': content_subscores
    }


