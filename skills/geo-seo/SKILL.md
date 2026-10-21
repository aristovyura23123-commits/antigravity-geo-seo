---
name: geo-seo
argument-hint: "<URL страницы или сайта, например: https://example.com/ [название бренда]>"
description: >
  Автономная мультиагентная система поисковой оптимизации нового поколения для классического SEO
  и генеративных ИИ-движков (GEO / AEO): Google AI Overviews, Perplexity AI, ChatGPT Search, Claude.
  Реализует бенчмарк Princeton GEO-bench (Share of Model SoM, Citation Probability Index CPI, Extractability Index EI),
  детерминированный расчет технических и контентных штрафов, нелинейную формулу приоритизации
  (Impact * Confidence / Effort^1.2 * Urgency), синтез валидной микроразметки Schema.org (Organization, FAQPage, WebPage)
  и Answer-First модулей (40-60 слов), шлюз качества QA Gate и генерацию интерактивного 7-секционного HTML-отчета.
  Используйте при запросах: "geo", "aeo", "geo seo", "generative engine optimization", "оптимизация под ии",
  "ai overviews", "perplexity seo", "chatgpt seo", "princeton geo", "som", "cpi", "extractability index",
  "answer-first", "гео сео", "ии аудит сайта", "подготовка сайта для нейросетей", "ai crawler audit".
---

# Antigravity AI Multi-Agent GEO & SEO Engine

Инструмент реализует архитектуру автономной мультиагентной системы для одновременной оптимизации сайта под традиционный органический поиск (SEO) и генеративные ответы языковых моделей (GEO / AEO: Google AI Overviews, Perplexity, ChatGPT Search, Claude).

Архитектура построена в строгом соответствии с исследовательской спецификацией **Princeton GEO-bench** (Princeton University, IIT Delhi, Allen AI) и корпоративными стандартами обеспечения качества данных.

---

## Ключевые возможности и математическая модель

### 1. Детерминированный расчет традиционного SEO (Traditional SEO Score)
- **Технический скоринг**:
  $$\text{Technical SEO Score} = 100 - \sum \min(\text{Penalty}_i \times \text{Count}_i, \text{MaxPenalty}_i)$$
  Включает строгие вычеты за блокировку ИИ-краулеров в `robots.txt` (`-15`), отсутствие `rel=canonical` (`-8`), дефекты `H1` (`-10`), неиндексируемость `noindex` (`-40`), задержки сервера TTFB (`-12`).
- **Контентный скоринг**:
  $$\text{Content Score} = 0.35 \times \text{Topical} + 0.25 \times \text{Structure} + 0.20 \times \text{Readability} + 0.20 \times \text{Intent}$$
- **Сводный SEO Score**:
  $$\text{Composite SEO Score} = 0.40 \times \text{Technical} + 0.40 \times \text{Content} + 0.20 \times \text{Authority}$$

### 2. Princeton GEO-bench Framework
- **Share of Model (SoM)**: Доля присутствия бренда в сгенерированных ответах языковых моделей по нишевым запросам.
- **Citation Probability Index (CPI)**: Вероятность превращения упоминания бренда в активную гиперссылку-источник.
- **Extractability Index (EI)**:
  $$\text{EI} = 0.30 \times \text{StatsPresence} + 0.30 \times \text{Quotes} + 0.20 \times \text{AnswerFirst} + 0.20 \times \text{StructuredTables}$$
- **Composite GEO Score**:
  $$\text{GEO Score} = 0.35 \times \text{SoM} + 0.25 \times \text{CPI} + 0.25 \times \text{EI} + 0.15 \times \text{TopicalCoverage}$$
- **Overall Growth Score**:
  $$\text{Overall Growth Score} = 0.50 \times \text{SEO} + 0.50 \times \text{GEO}$$

### 3. Нелинейная матрица приоритизации
Каждая задача ранжируется с учетом штрафа за трудоемкость по формуле:
$$\text{Priority Score} = \frac{\text{Impact} \times \text{Confidence}}{\text{Effort}^{1.2}} \times \text{Urgency}$$
Это математически выводит быстрореализуемые задачи с максимальным эффектом («Quick Wins») на первое место.

### 4. Генерация артефактов без заглушек (Zero Placeholders)
- Полный семантический граф Schema.org `@graph` (Organization, FAQPage, WebPage) в формате JSON-LD.
- Модули прямого ответа **Answer-First** (строго 40–60 слов) с включением проверяемых чисел и метрик.
- Семантические таблицы сравнения характеристик для RAG-парсеров.
- Рекомендованные правила `robots.txt` для `GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`.

### 5. Шлюз контроля качества (QA Gate)
Каждый артефакт верифицируется AST-парсером Schema.org, контролируется отсутствие шаблонных заглушек (`TODO`, `Lorem`, `example.com`), соответствие нормам длины и отсутствие директивных противоречий.

---

## Как использовать

### Запуск через консоль / bash:
```bash
python3 ~/.gemini/config/plugins/geo-seo/scripts/geo_seo_cli.py \
  --url "https://example.com/page" \
  --brand "Название Бренда" \
  --output-html "audit_report.html" \
  --output-json "audit_report.json" \
  --output-csv "backlog.csv"
```

### Примеры запросов агенту:
- «Проведи полный GEO и SEO аудит для сайта https://juniorshop.ru/»
- «Оцени готовность страницы к Google AI Overviews и Perplexity: https://example.com/blog/article»
- «Подготовь JSON-LD микроразметку и Answer-First блоки для https://example.com»
- «Рассчитай Princeton GEO-bench метрики SoM, CPI и Extractability Index для нашего сайта»

---

## Структура выходного отчета
1. **Секция 1: Executive Dashboard** (Overall Growth, SEO Score, GEO Score, QA Gate, трио SoM/CPI/EI).
2. **Секция 2: Технический аудит & ИИ-доступность** (Статус в robots.txt для GPTBot, PerplexityBot, ClaudeBot, таблица штрафов).
3. **Секция 3: GEO & AI Visibility Intelligence** (Матрица модельных тестов по интентам, декомпозиция извлекаемости).
4. **Секция 4: Семантический граф & Анализ сущностей** (Объем, читаемость по Flesch, распознанные сущности).
5. **Секция 5: Приоритизированный каталог задач** (Инженерные карточки задач с Priority Score).
6. **Секция 6: Готовые к внедрению артефакты** (JSON-LD код, Answer-First модули 40-60 слов, таблицы, robots.txt с кнопками копирования).
7. **Секция 7: Стратегическая дорожная карта (30/60/90 Day Roadmap)** (Спринты с контрольными вехами и привязанными задачами).
