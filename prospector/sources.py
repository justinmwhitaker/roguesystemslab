from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus
from urllib.request import urlopen
import re


@dataclass
class Candidate:
    full_name: str
    title: str
    company_name: str
    company_headcount: int
    linkedin_url: str
    source: str


class SourceAdapter:
    source_name: str

    def fetch_candidates(self, query: str, limit: int) -> list[Candidate]:
        raise NotImplementedError


class WebSourceAdapter(SourceAdapter):
    source_name = "web"

    def fetch_candidates(self, query: str, limit: int) -> list[Candidate]:
        # Public search endpoint (no API key) for MVP experimentation.
        url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
        with urlopen(url, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html)
        cleaned = [re.sub(r"<[^>]+>", "", t).strip() for t in titles if t.strip()]

        rows: list[Candidate] = []
        for idx, title in enumerate(cleaned[:limit], start=1):
            rows.append(
                Candidate(
                    full_name=f"Web Lead {idx}",
                    title=title[:80] or "Unknown title",
                    company_name="Unknown",
                    company_headcount=0,
                    linkedin_url="",
                    source=self.source_name,
                )
            )
        return rows


class LinkedInSourceAdapter(SourceAdapter):
    source_name = "linkedin"

    def fetch_candidates(self, query: str, limit: int) -> list[Candidate]:
        # Search public pages containing LinkedIn profiles.
        search_query = f"site:linkedin.com/in {query}"
        url = f"https://duckduckgo.com/html/?q={quote_plus(search_query)}"
        with urlopen(url, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")

        links = re.findall(r'href="(https?://[^"]+)"', html)
        linkedin_links = []
        for link in links:
            if "linkedin.com/in/" in link and link not in linkedin_links:
                linkedin_links.append(link)

        rows: list[Candidate] = []
        for idx, link in enumerate(linkedin_links[:limit], start=1):
            handle = link.rstrip("/").split("/")[-1].replace("-", " ").title()
            rows.append(
                Candidate(
                    full_name=handle or f"LinkedIn Lead {idx}",
                    title="Unknown",
                    company_name="Unknown",
                    company_headcount=0,
                    linkedin_url=link,
                    source=self.source_name,
                )
            )
        return rows


def get_adapters(sources: tuple[str, ...]) -> list[SourceAdapter]:
    adapters: list[SourceAdapter] = []
    for source in sources:
        if source == "web":
            adapters.append(WebSourceAdapter())
        elif source == "linkedin":
            adapters.append(LinkedInSourceAdapter())
    return adapters
