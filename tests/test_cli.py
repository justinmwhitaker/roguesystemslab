from pathlib import Path

from prospector.cli import main, prompt_for_run_config, run_interactive


def test_prompt_for_run_config_collects_answers():
    answers = iter([
        "AI copilot",
        "Seed B2B SaaS CTO",
        "1-100",
        "web,linkedin",
        "25",
        "30",
    ])

    config = prompt_for_run_config(lambda _q: next(answers))

    assert config.product == "AI copilot"
    assert config.icp == "Seed B2B SaaS CTO"
    assert config.target_company_size == "1-100"
    assert config.sources == ("web", "linkedin")
    assert config.max_prospects == 25
    assert config.lookback_days == 30


def test_run_interactive_launches_prompt_and_run_function():
    answers = iter([
        "AI copilot",
        "Seed B2B SaaS CTO",
        "1-100",
        "web",
        "10",
        "14",
    ])
    captured = {}

    def fake_run(config, out_path):
        captured["config"] = config
        captured["out_path"] = out_path
        return Path(out_path)

    written = run_interactive(lambda _q: next(answers), "prospects.csv", fake_run)

    assert written == Path("prospects.csv")
    assert captured["out_path"] == "prospects.csv"
    assert captured["config"].sources == ("web",)
    assert captured["config"].lookback_days == 14


def test_main_without_subcommand_starts_interactive(monkeypatch):
    called = {}

    def fake_run_interactive():
        called["interactive"] = True

    monkeypatch.setattr("prospector.cli.run_interactive", fake_run_interactive)

    main([])

    assert called == {"interactive": True}
