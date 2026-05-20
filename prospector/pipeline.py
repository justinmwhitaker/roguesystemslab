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


MOCK_PROSPECTS = [
    ("Alex Carter", "CTO", "Nebula Labs", 78, -0.1, 0.82, 0.71, 90, 88),
    ("Priya Shah", "VP Engineering", "OrbitForge", 54, 0.2, 0.75, 0.66, 86, 84),
    ("Jordan Lee", "Head of Security", "SignalPeak", 112, -0.05, 0.64, 0.59, 80, 72),
]


def build_mock_rows(config: RunConfig) -> list[ProspectRow]:
    now = datetime.now(timezone.utc).isoformat()
    rows: list[ProspectRow] = []
    for full_name, title, company, headcount, sentiment, topic, intent, role_fit, company_fit in MOCK_PROSPECTS[: config.max_prospects]:
        sentiment_component = (sentiment + 1) * 50
        score = conversion_score(role_fit, company_fit, topic * 100, sentiment_component, intent * 100)
        rows.append(
            ProspectRow(
                full_name=full_name,
                title=title,
                company_name=company,
                company_headcount=headcount,
                headcount_fit=headcount < 100,
                linkedin_url=f"https://www.linkedin.com/in/{full_name.lower().replace(' ', '-')}",
                sentiment_30d=sentiment,
                topic_relevance_30d=round(topic, 2),
                intent_signal_score=round(intent, 2),
                conversion_likelihood=score,
                source_timestamp_utc=now,
            )
        )
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
