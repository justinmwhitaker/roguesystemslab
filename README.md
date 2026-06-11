# Prospect-CLI
Prospecting automation concept and implementation blueprint.

## Goal
Build a terminal-first app/agent that accepts:
- Product description
- ICP definition
- Prospect filters (example: decision makers at companies with fewer than 100 employees)

Then:
1. Discovers candidate prospects from selected sources.
2. Enriches each profile with role/company fit signals.
3. Calculates a conversion-likelihood score.
4. Exports ranked prospects to CSV.

---

## Important compliance note
Direct LinkedIn scraping/automation often conflicts with LinkedIn Terms of Service and can create legal and account-risk issues. A production system should prefer compliant sources such as:
- LinkedIn-approved partner integrations/APIs (if available to your org)
- Licensed B2B data providers
- First-party CRM/enrichment data

Use this architecture with policy/legal review before deployment.

---

## Current implementation status (May 2026)
This repo currently includes:
- Interactive CLI mode (default if no subcommand is provided)
- Non-interactive `run` subcommand with flags
- Source-aware adapter routing for `web` and `linkedin`
- CSV output with deterministic scoring

The external-source adapters are MVP-level and use public search endpoints. They are intended for experimentation and should be replaced by licensed/provider APIs for production.

## How to run

### Interactive mode
Run `prospector` with no subcommand and answer prompts:

1) What product are we looking for prospects for?
2) What is the target client?
3) What is the target company size?
4) Where should Prospect look? (Web, LinkedIn)
5) How many prospects do I want returned?
6) How many days should be searched? (1-180 days)

```bash
prospector
```

### Non-interactive mode
```bash
prospector run \
  --product "AI-first SOC automation platform" \
  --icp "Seed-Series B B2B SaaS companies" \
  --filters "decision makers, <100 employees, US" \
  --target-company-size "1-100" \
  --sources "web,linkedin" \
  --lookback-days 30 \
  --max-prospects 50 \
  --out prospects.csv
```

### 2) Workflow modules
- **Input parser**
  - Normalizes product/ICP/filter constraints into structured criteria.
- **Lead discovery**
  - Builds search queries and collects candidate LinkedIn profile/company URLs via compliant acquisition paths.
- **Profile extractor**
  - Pulls public data fields: name, title, company, location, profile URL, etc.
- **Company enricher**
  - Adds company headcount range, industry, growth indicators from enrichment providers.
- **Post collector (30-day window)**
  - Pulls recent public posts and metadata (date, reactions/comments if available).
- **NLP scoring engine**
  - Sentiment scoring
  - Topical match to your product problem space
  - Buying-intent cues (tool-change, hiring, pain keywords)
- **Ranking model**
  - Weighted score + confidence score + explanation text.
- **CSV exporter**
  - Writes standardized output schema.

### 3) Data model (CSV columns)
Recommended columns:
- `prospect_id`
- `full_name`
- `title`
- `seniority`
- `department`
- `company_name`
- `company_headcount`
- `headcount_fit` (boolean)
- `location`
- `linkedin_url`
- `icp_fit_score` (0-100)
- `sentiment_30d` (-1.0 to 1.0)
- `topic_relevance_30d` (0-1)
- `intent_signal_score` (0-1)
- `conversion_likelihood` (0-100)
- `score_explanation`
- `last_post_date`
- `source_timestamp_utc`

### 4) Scoring formula (first-pass baseline)
Example deterministic baseline before ML tuning:

```text
conversion_likelihood =
  0.35 * role_fit +
  0.25 * company_fit +
  0.20 * topic_relevance_30d +
  0.10 * sentiment_component +
  0.10 * intent_signal
```

### Interactive mode
After installation, run `prospector` with no subcommand and answer prompts:

1) What product are we looking for prospects for?
2) What is the target client?
3) What is the target company size?
4) Where should Prospect look? (Web, LinkedIn)
5) How many prospects do I want returned?
6) How many days should be searched? (1-180 days)

```bash
prospector
```

---

## CLI scaffold (ready for dry run)

### Project structure
- `pyproject.toml`
- `src/prospector/cli.py`
- `src/prospector/pipeline.py`
- `src/prospector/scoring.py`
- `src/prospector/config.py`
- `tests/test_scoring.py`

### Quick start
```bash
prospector run \
  --product "AI-first SOC automation platform" \
  --icp "Seed-Series B B2B SaaS companies" \
  --filters "decision makers, <100 employees, US" \
  --target-company-size "1-100" \
  --sources "web,linkedin" \
  --lookback-days 30 \
  --max-prospects 50 \
  --out prospects.csv
```

## Source selection behavior
- `--sources web` uses only the web adapter.
- `--sources linkedin` uses only the LinkedIn-targeted adapter.
- `--sources web,linkedin` uses both adapters.

## Config model
`RunConfig` currently supports:
- `product: str`
- `icp: str`
- `filters: str`
- `max_prospects: int` (must be non-negative)
- `target_company_size: str`
- `sources: tuple[str, ...]`
- `lookback_days: int` (must be 1-180)

## Project structure
- `prospector/cli.py` — interactive and batch CLI entrypoints
- `prospector/config.py` — run configuration model and validation
- `prospector/sources.py` — source adapters and adapter factory
- `prospector/pipeline.py` — candidate fetch orchestration, scoring, CSV write
- `prospector/scoring.py` — conversion scoring utilities
- `tests/` — unit tests for CLI, pipeline, scoring, sources

## Testing
```bash
python -m pytest -q
```
