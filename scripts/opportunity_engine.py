"""
Opportunity Detection Engine & Mathematical Prioritization.
Implements the formula:
    Priority Score = (Impact * Confidence) / (Effort ^ 1.2) * Urgency

Ranks opportunities across:
- AI Crawler Infrastructure (Robots.txt)
- Structured Data (JSON-LD Schemas)
- GEO Answer-First Modular Rewrites
- Factual & Statistical Density (Information Gain)
- Tabular Comparison Data
- Technical & On-Page Core Factors
"""

def calculate_priority_score(impact, confidence, effort, urgency):
    """
    Computes deterministic priority score with progressive non-linear effort penalty.
    """
    effort_penalized = max(0.8, effort) ** 1.2
    score = (impact * confidence) / effort_penalized * urgency
    return round(score, 2)

def detect_seo_geo_opportunities(crawl_data, seo_details, geo_details):
    """
    Scans diagnostic signals from crawler, SEO, and GEO modules,
    and returns ranked opportunities with concrete payloads.
    """
    opportunities = []

    # 1. Robots.txt AI Bot Access
    robots = crawl_data.get('robots_data', {})
    blocked = robots.get('blocked_bots', [])
    if blocked:
        impact = 9.5
        confidence = 0.98
        effort = 1.0
        urgency = 2.0
        p_score = calculate_priority_score(impact, confidence, effort, urgency)
        
        allowed_snippet = (
            "# Разрешить доступ поисковым ИИ-краулерам для GEO/AEO\n"
            "User-agent: GPTBot\nAllow: /\n\n"
            "User-agent: PerplexityBot\nAllow: /\n\n"
            "User-agent: ClaudeBot\nAllow: /\n\n"
            "User-agent: Google-Extended\nAllow: /\n"
        )
        
        opportunities.append({
            'id': 'OPP-AI-ROBOTS',
            'title': 'Открыть доступ поисковым ИИ-краулерам в robots.txt',
            'category': 'GEO Инфраструктура',
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'urgency': urgency,
            'priority_score': p_score,
            'issue_description': f"В robots.txt обнаружена блокировка или ограничение для ИИ-ботов: {', '.join(blocked)}. Страницы исключаются из индексов SearchGPT, Perplexity и Claude.",
            'expected_outcome': 'Индексация страниц в векторных базах и RAG-памяти языковых моделей (рост Share of Model на +30-40%).',
            'actionable_payload': allowed_snippet,
            'payload_type': 'robots_txt'
        })

    # 2. Schema.org JSON-LD Structured Data
    existing_schemas = crawl_data.get('existing_schemas', [])
    has_faq = any(s.get('@type') == 'FAQPage' for s in existing_schemas)
    has_article = any(s.get('@type') in ['Article', 'BlogPosting', 'NewsArticle'] for s in existing_schemas)

    if not existing_schemas or not has_faq:
        impact = 8.5
        confidence = 0.95
        effort = 1.5
        urgency = 1.5
        p_score = calculate_priority_score(impact, confidence, effort, urgency)
        
        opportunities.append({
            'id': 'OPP-SCHEMA-JSONLD',
            'title': 'Внедрить семантическую микроразметку JSON-LD (FAQPage + Article / Organization)',
            'category': 'Структурированные данные & Граф знаний',
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'urgency': urgency,
            'priority_score': p_score,
            'issue_description': "На странице отсутствует валидная микроразметка FAQPage или Article. Поисковые LLM не могут однозначно извлечь сущности и пары «вопрос-ответ».",
            'expected_outcome': 'Получение расширенных сниппетов (Rich Snippets) в Google/Яндекс и цитирование в блоках Google AI Overviews.',
            'actionable_payload': 'Сгенерирован готовый JSON-LD скрипт в разделе артефактов.',
            'payload_type': 'schema_jsonld'
        })

    # 3. Answer-First Modular Content Structure
    ei_details = geo_details.get('ei_details', {})
    answer_first_score = ei_details.get('answer_first_score', 0)
    geo_blocks = crawl_data.get('geo_blocks', [])
    fluffy_blocks = [b for b in geo_blocks if b.get('has_fluff', False) or not b.get('is_answer_first', False)]

    if answer_first_score < 70 or fluffy_blocks:
        impact = 8.2
        confidence = 0.90
        effort = 2.2
        urgency = 1.3
        p_score = calculate_priority_score(impact, confidence, effort, urgency)
        
        opportunities.append({
            'id': 'OPP-ANSWER-FIRST',
            'title': 'Реструктурировать контент в формат Answer-First (первые 40-60 слов)',
            'category': 'GEO Контентная оптимизация',
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'urgency': urgency,
            'priority_score': p_score,
            'issue_description': f"Обнаружено {len(fluffy_blocks)} разделов с общими вводными штампами или отложенным ответом. RAG-парсеры игнорируют «водянистые» чанки при синтезе ответа.",
            'expected_outcome': 'Попадание текста страницы в прямой синтез ответов Perplexity, ChatGPT и Gemini (рост Extractability Index на +25%).',
            'actionable_payload': 'Сгенерированы переписанные модульные блоки в разделе артефактов.',
            'payload_type': 'content_rewrite'
        })

    # 4. Statistical & Quantitative Density Gaps
    stats_score = ei_details.get('stats_presence_score', 0)
    if stats_score < 60:
        impact = 7.5
        confidence = 0.88
        effort = 2.0
        urgency = 1.2
        p_score = calculate_priority_score(impact, confidence, effort, urgency)

        opportunities.append({
            'id': 'OPP-STATS-DENSITY',
            'title': 'Повысить плотность фактов и количественных метрик (Information Gain)',
            'category': 'Информационная ценность & E-E-A-T',
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'urgency': urgency,
            'priority_score': p_score,
            'issue_description': f"Плотность чисел и статистических выкладок ниже нормы GEO-bench ({crawl_data.get('total_stats_count', 0)} метрик на страницу). Языковые модели предпочитают страницы с доказательными цифрами.",
            'expected_outcome': 'Рост авторитетности контента и увеличение частоты цитирования на 30–40% согласно исследованию Princeton GEO.',
            'actionable_payload': 'Добавить точные процентные доли, сроки, цены, диапазоны и результаты тестов в ключевые абзацы.',
            'payload_type': 'guideline'
        })

    # 5. Missing Comparison Tables
    tables_count = crawl_data.get('tables_count', 0)
    if tables_count == 0:
        impact = 7.0
        confidence = 0.85
        effort = 1.8
        urgency = 1.1
        p_score = calculate_priority_score(impact, confidence, effort, urgency)

        opportunities.append({
            'id': 'OPP-STRUCTURED-TABLES',
            'title': 'Внедрить семантические таблицы сравнения или характеристик',
            'category': 'RAG Структура данных',
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'urgency': urgency,
            'priority_score': p_score,
            'issue_description': "На странице отсутствуют структурированные таблицы (<table>). Табличные данные обладают максимальным весом при векторном извлечении RAG-парсерами.",
            'expected_outcome': 'Прямое включение табличных строк в генеративные ответы при сравнении альтернатив.',
            'actionable_payload': 'Сформирован шаблон таблицы сравнения в разделе артефактов.',
            'payload_type': 'table_snippet'
        })

    # 6. Canonical & Technical Metadata
    canon = crawl_data.get('canonical_url', '')
    if not canon:
        impact = 6.8
        confidence = 0.95
        effort = 1.0
        urgency = 1.4
        p_score = calculate_priority_score(impact, confidence, effort, urgency)

        url = crawl_data.get('url', '')
        opportunities.append({
            'id': 'OPP-CANONICAL-FIX',
            'title': 'Установить самореферентный тег rel=canonical',
            'category': 'Техническое SEO',
            'impact': impact,
            'confidence': confidence,
            'effort': effort,
            'urgency': urgency,
            'priority_score': p_score,
            'issue_description': "Отсутствует тег <link rel='canonical'>. Риск появления дублей страниц при наличии параметров или редиректов.",
            'expected_outcome': 'Консолидация ссылочного веса на едином основном URL.',
            'actionable_payload': f'<link rel="canonical" href="{url}" />',
            'payload_type': 'html_head'
        })

    # Sort opportunities in descending order of Priority Score
    opportunities.sort(key=lambda x: x['priority_score'], reverse=True)
    return opportunities
