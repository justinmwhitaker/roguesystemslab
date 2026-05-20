from __future__ import annotations

import csv
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from pathlib import Path

from .config import RunConfig
from .scoring import conversion_score
from .sources import Candidate, get_adapters


@dataclass
class ProspectRow:
    full_name: str
    title: str
    company_name: str
    company_headcount: int
    headcount_fit: bool
    linkedin_url: str
    sentiment_30d: float
    topic_relevance_30d: float
    intent_signal_score: float
    conversion_likelihood: float
    source_timestamp_utc: str


def _score_candidate(candidate: Candidate, target_company_size: str) -> ProspectRow:
    sentiment = 0.0
    topic = 0.6
    intent = 0.5
    role_fit = 75
    company_fit = 70

    if target_company_size and candidate.company_headcount > 0:
        company_fit = 85

    sentiment_component = (sentiment + 1) * 50
    score = conversion_score(role_fit, company_fit, topic * 100, sentiment_component, intent * 100)

    return ProspectRow(
        full_name=candidate.full_name,
        title=candidate.title,
        company_name=candidate.company_name,
        company_headcount=candidate.company_headcount,
        headcount_fit=candidate.company_headcount < 100 if candidate.company_headcount else False,
        linkedin_url=candidate.linkedin_url,
        sentiment_30d=sentiment,
        topic_relevance_30d=topic,
        intent_signal_score=intent,
        conversion_likelihood=score,
        source_timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )


def build_rows(config: RunConfig) -> list[ProspectRow]:
    query = f"{config.product} {config.icp} {config.filters} last {config.lookback_days} days"
    adapters = get_adapters(config.sources)
    if not adapters:
        return []

    per_source_limit = max(1, config.max_prospects // len(adapters))
    candidates: list[Candidate] = []
    for adapter in adapters:
        candidates.extend(adapter.fetch_candidates(query, per_source_limit))

    rows = [_score_candidate(c, config.target_company_size) for c in candidates[: config.max_prospects]]
    return rows


def write_csv(rows: list[ProspectRow], out_path: str) -> Path:
    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [field.name for field in fields(ProspectRow)]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return output


def dry_run(config: RunConfig, out_path: str) -> Path:
    rows = build_rows(config)
    return write_csv(rows, out_path)
