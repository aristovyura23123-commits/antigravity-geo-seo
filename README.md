# Antigravity GEO & SEO Multi-Agent Engine

> Автономная мультиагентная система поисковой оптимизации для традиционного SEO и генеративных ИИ-движков (Google AI Overviews, Perplexity AI, ChatGPT Search, Claude).

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Princeton GEO-bench](https://img.shields.io/badge/GEO--bench-Compliant-green.svg)](https://arxiv.org/abs/2311.09735)

---

## Архитектура и методология

Инструмент реализует научные стандарты **Princeton GEO-bench** (Princeton University, IIT Delhi, Allen AI) и строгие детерминированные формулы оценки:

```
[Target URL / Domain]
         │
         ▼
[1. Crawler & Multi-Signal Extractor] ─── DOM, Robots.txt, Schemas, Content Blocks
         │
         ├─────────────────────────────────────────┐
         ▼                                         ▼
[2. Traditional SEO Engine]              [3. Princeton GEO Engine]
 - Technical Score (Exact deductions)     - Share of Model (SoM)
 - Content Score (Topical, Structure)     - Citation Probability Index (CPI)
 - Authority & Linking                    - Extractability Index (EI)
         │                                         │
         └───────────────────┬─────────────────────┘
                             │
                             ▼
              [4. Overall Growth Score: 0.50*SEO + 0.50*GEO]
                             │
                             ▼
              [5. Opportunity Detection & Ranking]
                 Priority = (Impact * Conf) / (Effort^1.2) * Urgency
                             │
                             ▼
              [6. Artifact Generator (Zero Placeholders)]
                 - JSON-LD Schemas (Org, FAQPage, WebPage)
                 - Answer-First Modules (40–60 words, Stats)
                 - Semantic Comparison Tables
                 - AI-friendly robots.txt rules
                             │
                             ▼
              [7. QA Gate & AST Validator]
                             │
                             ▼
       [8. Interactive 7-Section HTML Report + JSON & CSV]
```

---

## Математические формулы

### 1. Традиционный SEO Score
$$\text{Technical SEO Score} = 100 - \sum \min(\text{Penalty}_i \times \text{Count}_i, \text{MaxPenalty}_i)$$
$$\text{Content Score} = 0.35 \times \text{Topical} + 0.25 \times \text{Structure} + 0.20 \times \text{Readability} + 0.20 \times \text{Intent}$$
$$\text{Composite SEO Score} = 0.40 \times \text{Technical} + 0.40 \times \text{Content} + 0.20 \times \text{Authority}$$

### 2. Princeton GEO-bench Score
$$\text{Extractability Index (EI)} = 0.30 \times \text{Stats} + 0.30 \times \text{Quotes} + 0.20 \times \text{AnswerFirst} + 0.20 \times \text{Tables}$$
$$\text{Composite GEO Score} = 0.35 \times \text{SoM} + 0.25 \times \text{CPI} + 0.25 \times \text{EI} + 0.15 \times \text{Topical}$$
$$\text{Overall Growth Score} = 0.50 \times \text{SEO} + 0.50 \times \text{GEO}$$

### 3. Приоритизация бэклога
$$\text{Priority Score} = \frac{\text{Impact} \times \text{Confidence}}{\text{Effort}^{1.2}} \times \text{Urgency}$$

---

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install beautifulsoup4
```

### 2. Запуск аудита через консоль
```bash
python3 scripts/geo_seo_cli.py --url "Ваш сайт" --brand "Ваш бренд"
```

### 3. Запуск тестов
```bash
python3 -m unittest discover tests
```

---

## Сформированные артефакты

После выполнения аудита система генерирует три взаимодополняющих формата:
1. **Интерактивный HTML Дашборд** (`geo_seo_report_domain.html`):
   - Executive Dashboard с круговыми индикаторами и шкалами прогресса.
   - Матрица тестирования ИИ-промптов по ключевым интентам.
   - Приоритизированные карточки задач с оценками Impact / Effort / Priority.
   - Готовые блоки кода с кнопками 1-click копирования (JSON-LD, Answer-First, robots.txt, HTML-таблицы).
   - Стратегическая дорожная карта внедрения на 30, 60 и 90 дней.
2. **Машиночитаемый JSON-отчет** (`geo_seo_report_domain.json`): Полное состояние системы, готовое к передаче в CI/CD или агентные пайплайны.
3. **CSV-каталог бэклога** (`opportunities_domain.csv`): Таблица задач для прямого импорта в Jira, Notion, ClickUp или Asana.

---

## Лицензия
MIT License.
