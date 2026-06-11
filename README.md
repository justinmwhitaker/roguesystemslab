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

### Install once
Install the project in editable mode so the `prospector` command is available from Bash, PowerShell, or any terminal on your Python environment's `PATH`:

```bash
python -m pip install -e .
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
