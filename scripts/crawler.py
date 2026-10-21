"""
High-performance web crawler and multi-signal extractor for SEO and GEO.
Extracts:
- Technical signals: Status, Headers, Canonical, Meta Robots, DOM structure, CWV proxies
- AI Bot Accessibility: Inspects robots.txt for GPTBot, PerplexityBot, ClaudeBot, Google-Extended
- Structured Data: Parses and validates existing JSON-LD schemas
- Content & GEO signals: Word count, Heading hierarchy, Flesch readability,
  Answer-First blocks (first 40-60 words under headings), Statistics/Numbers density,
  Authoritative citations, Comparison tables, and Lists.
"""

import urllib.request
from urllib.parse import urlparse, urljoin
import re
import json
import time
from bs4 import BeautifulSoup

OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 AntigravityGeoSeo/1.0'
}

AI_BOTS = [
    'GPTBot',
    'PerplexityBot',
    'ClaudeBot',
    'Google-Extended',
    'Bytespider',
    'CCBot'
]

def check_robots_ai_access(base_url):
    """
    Fetches robots.txt and checks whether generative AI crawlers are permitted or blocked.
    """
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    blocked_bots = []
    allowed_bots = []
    robots_content = ""

    try:
        req = urllib.request.Request(robots_url, headers=HEADERS)
        with OPENER.open(req, timeout=8) as resp:
            robots_content = resp.read().decode('utf-8', errors='replace')
        
        lines = [line.strip() for line in robots_content.splitlines() if line.strip() and not line.startswith('#')]
        current_agent = None
        disallows = {}

        for line in lines:
            if line.lower().startswith('user-agent:'):
                current_agent = line.split(':', 1)[1].strip()
                if current_agent not in disallows:
                    disallows[current_agent] = []
            elif line.lower().startswith('disallow:') and current_agent:
                path = line.split(':', 1)[1].strip()
                disallows[current_agent].append(path)

        for bot in AI_BOTS:
            # Check specific bot rule or wildcard * rule
            rules = disallows.get(bot, [])
            wildcard_rules = disallows.get('*', [])
            
            is_blocked = False
            if '/' in rules or '/*' in rules:
                is_blocked = True
            elif '/' in wildcard_rules and bot not in disallows:
                is_blocked = True
                
            if is_blocked:
                blocked_bots.append(bot)
            else:
                allowed_bots.append(bot)

    except Exception as e:
        # If robots.txt is 404 or unreachable, default to accessible
        allowed_bots = list(AI_BOTS)

    return {
        'robots_url': robots_url,
        'blocked_bots': blocked_bots,
        'allowed_bots': allowed_bots,
        'is_ai_friendly': len(blocked_bots) == 0,
        'raw_robots': robots_content[:1500] if robots_content else "robots.txt not found (accessible)"
    }

def calculate_flesch_reading_ease(text, lang='ru'):
    """
    Calculates Flesch Reading Ease score.
    Higher = easier to read (target 50-70 for commercial/informational B2C/B2B).
    """
    words = re.findall(r'[а-яёa-z0-9]+', text.lower())
    if not words:
        return 60.0

    num_words = len(words)
    raw_sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 5]
    num_sentences = max(1, len(sentences))

    # Syllable approximation (vowel count)
    vowels = set('аеёиоуыэюяaeiouy')
    total_syllables = sum(sum(1 for char in word if char in vowels) for word in words)
    total_syllables = max(num_words, total_syllables)

    asl = num_words / num_sentences
    asw = total_syllables / num_words

    if lang == 'ru':
        # Russian adaptation of Flesch (Oborneva formula)
        score = 206.835 - (1.3 * asl) - (60.1 * asw)
    else:
        score = 206.835 - (1.015 * asl) - (84.6 * asw)

    return max(0.0, min(100.0, score))

def extract_geo_content_blocks(soup):
    """
    Extracts sections under H2/H3 headings, evaluates Answer-First compliance
    (first 40-60 words), and detects statistical claims and authoritative quotes.
    """
    blocks = []
    headings = soup.find_all(['h2', 'h3'])

    for h in headings:
        heading_text = h.get_text().strip()
        if not heading_text or len(heading_text) < 4:
            continue

        # Collect subsequent paragraph text until next heading
        sibling_paragraphs = []
        curr = h.next_sibling
        while curr:
            if getattr(curr, 'name', None) in ['h1', 'h2', 'h3', 'h4']:
                break
            if getattr(curr, 'name', None) in ['p', 'div', 'ul', 'ol', 'table']:
                p_text = curr.get_text(separator=' ', strip=True)
                if p_text:
                    sibling_paragraphs.append(p_text)
            curr = curr.next_sibling

        section_body = ' '.join(sibling_paragraphs)
        words = re.findall(r'\w+', section_body)

        if len(words) < 5:
            continue

        # Evaluate Answer-First pattern in initial 40-60 words
        opening_window = ' '.join(words[:60])
        fluff_patterns = re.compile(
            r'^(в современном мире|ни для кого не секрет|как известно|важно отметить|следует подчеркнуть|сегодня невозможно представить|каждый из нас|в этой статье мы|давайте разберемся)',
            re.I
        )
        has_fluff = bool(fluff_patterns.search(opening_window))
        
        # Declarative direct answer indicators
        is_answer_first = not has_fluff and len(words) >= 20

        # Stats detection: numbers with symbols, currencies, percentages, metric units
        stats_matches = re.findall(
            r'\b\d+(?:[\.,]\d+)?\s*(?:%|руб|рублей|\$|€|тыс|млн|млрд|кг|г|км|м|см|мм|квт|человек|лет|минут|секунд|дней|часов)\b',
            section_body,
            re.I
        )

        # Authoritative quote / citation detection
        citations_matches = re.findall(
            r'\b(?:согласно|по данным|исследование|отчет|гост|санпин|эксперт|университет|гарвард|ст\.\s*\d+|закон|институт|статистика|опрос)\b',
            section_body,
            re.I
        )

        blocks.append({
            'heading': heading_text,
            'body_snippet': section_body[:400],
            'word_count': len(words),
            'opening_60_words': opening_window,
            'is_answer_first': is_answer_first,
            'has_fluff': has_fluff,
            'stats_count': len(stats_matches),
            'stats_examples': stats_matches[:3],
            'citations_count': len(citations_matches),
            'citations_examples': citations_matches[:3]
        })

    return blocks

def crawl_and_inspect_page(url, brand_name=None):
    """
    Performs full DOM, Technical, Content, and GEO inspection on the target URL.
    """
    start_time = time.time()
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with OPENER.open(req, timeout=12) as resp:
            status_code = resp.status
            content_type = resp.headers.get('Content-Type', '')
            raw_html = resp.read()
            html = raw_html.decode('utf-8', errors='replace')
        fetch_time = round(time.time() - start_time, 3)
    except Exception as e:
        return {
            'url': url,
            'status_code': getattr(e, 'code', 500),
            'error': str(e),
            'is_accessible': False
        }

    soup = BeautifulSoup(html, 'html.parser')

    # Decompose scripts and styles for text analysis
    scripts = soup.find_all('script')
    existing_schemas = []
    for s in scripts:
        if s.get('type') == 'application/ld+json':
            try:
                schema_json = json.loads(s.string or '{}')
                existing_schemas.append(schema_json)
            except Exception:
                pass

    for tag in soup(['script', 'style', 'noscript', 'iframe']):
        tag.decompose()

    # Meta & Headers
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ""

    meta_desc_tag = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
    meta_description = meta_desc_tag.get('content', '').strip() if meta_desc_tag else ""

    meta_robots_tag = soup.find('meta', attrs={'name': re.compile(r'^robots$', re.I)})
    meta_robots = meta_robots_tag.get('content', '').strip() if meta_robots_tag else "index, follow"
    is_noindex = 'noindex' in meta_robots.lower()

    canonical_tag = soup.find('link', rel=re.compile(r'canonical', re.I))
    canonical_url = canonical_tag.get('href', '').strip() if canonical_tag else ""

    # Heading hierarchy
    h1_tags = [h.get_text().strip() for h in soup.find_all('h1') if h.get_text().strip()]
    h2_tags = [h.get_text().strip() for h in soup.find_all('h2') if h.get_text().strip()]
    h3_tags = [h.get_text().strip() for h in soup.find_all('h3') if h.get_text().strip()]

    # Structural elements
    tables = soup.find_all('table')
    lists = soup.find_all(['ul', 'ol'])
    images = soup.find_all('img')
    images_missing_alt = [img for img in images if not img.get('alt', '').strip()]

    # Links
    all_links = soup.find_all('a', href=True)
    internal_links = []
    external_links = []
    domain = urlparse(url).netloc

    for a in all_links:
        href = a['href'].strip()
        if href.startswith(('javascript:', 'tel:', 'mailto:', '#')):
            continue
        full_href = urljoin(url, href)
        if urlparse(full_href).netloc == domain:
            internal_links.append(full_href)
        else:
            external_links.append(full_href)

    # Full text & Readability
    body_text = ' '.join(soup.get_text(separator=' ', strip=True).split())
    words = re.findall(r'[а-яёa-z0-9]+', body_text.lower())
    word_count = len(words)
    readability_score = calculate_flesch_reading_ease(body_text)

    # GEO Content Blocks & Answer-First Analysis
    geo_blocks = extract_geo_content_blocks(soup)

    # Check robots.txt for AI bots
    robots_data = check_robots_ai_access(url)

    # Brand mentions
    brand = brand_name or domain.split('.')[0]
    brand_occurrences = len(re.findall(re.escape(brand), body_text, re.I))

    # All numbers and statistics across the whole page
    total_stats = len(re.findall(r'\b\d+(?:[\.,]\d+)?\s*(?:%|руб|\$|€|тыс|млн|кг|км|м|лет|дней|часов)\b', body_text, re.I))

    return {
        'url': url,
        'domain': domain,
        'brand_name': brand,
        'status_code': status_code,
        'fetch_time_sec': fetch_time,
        'is_accessible': status_code == 200,
        'title': title,
        'title_length': len(title),
        'meta_description': meta_description,
        'meta_description_length': len(meta_description),
        'meta_robots': meta_robots,
        'is_noindex': is_noindex,
        'canonical_url': canonical_url,
        'h1_count': len(h1_tags),
        'h1_tags': h1_tags,
        'h2_count': len(h2_tags),
        'h2_tags': h2_tags[:8],
        'h3_count': len(h3_tags),
        'word_count': word_count,
        'readability_flesch': round(readability_score, 1),
        'tables_count': len(tables),
        'lists_count': len(lists),
        'images_count': len(images),
        'images_missing_alt_count': len(images_missing_alt),
        'internal_links_count': len(internal_links),
        'external_links_count': len(external_links),
        'existing_schemas': existing_schemas,
        'existing_schema_types': [s.get('@type', 'Unknown') for s in existing_schemas],
        'robots_data': robots_data,
        'geo_blocks': geo_blocks,
        'total_stats_count': total_stats,
        'brand_mentions_count': brand_occurrences,
        'body_text_preview': body_text[:600]
    }

# Alias for external CLI and plugins
crawl_and_extract_signals = crawl_and_inspect_page

