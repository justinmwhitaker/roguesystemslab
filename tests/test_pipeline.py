from prospector.config import RunConfig
from prospector.pipeline import dry_run


def test_dry_run_with_zero_max_prospects_writes_header_only(tmp_path):
    out = tmp_path / "prospects.csv"
    written = dry_run(RunConfig(product="p", icp="i", filters="f", max_prospects=0), str(out))

    assert written.exists()
    lines = written.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_run_config_rejects_negative_max_prospects():
    try:
        RunConfig(product="p", icp="i", filters="f", max_prospects=-1)
    except ValueError as exc:
        assert "non-negative" in str(exc)
    else:
        raise AssertionError("expected ValueError")
