from prospector.config import RunConfig
from prospector.pipeline import build_rows, dry_run


class DummyAdapter:
    def __init__(self, source_name: str):
        self.source_name = source_name

    def fetch_candidates(self, query: str, limit: int):
        from prospector.sources import Candidate

        return [
            Candidate(
                full_name=f"{self.source_name} lead",
                title="Engineer",
                company_name="Acme",
                company_headcount=50,
                linkedin_url="https://linkedin.com/in/test",
                source=self.source_name,
            )
        ][:limit]


def test_dry_run_with_zero_max_prospects_writes_header_only(tmp_path, monkeypatch):
    monkeypatch.setattr("prospector.pipeline.get_adapters", lambda _sources: [DummyAdapter("web")])
    out = tmp_path / "prospects.csv"
    written = dry_run(RunConfig(product="p", icp="i", filters="f", max_prospects=0), str(out))

    assert written.exists()
    lines = written.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_build_rows_uses_selected_sources(monkeypatch):
    monkeypatch.setattr("prospector.pipeline.get_adapters", lambda _sources: [DummyAdapter("web"), DummyAdapter("linkedin")])
    config = RunConfig(product="p", icp="i", filters="f", max_prospects=10, sources=("web", "linkedin"))

    rows = build_rows(config)

    assert len(rows) == 2


def test_run_config_rejects_negative_max_prospects():
    try:
        RunConfig(product="p", icp="i", filters="f", max_prospects=-1)
    except ValueError as exc:
        assert "non-negative" in str(exc)
    else:
        raise AssertionError("expected ValueError")
