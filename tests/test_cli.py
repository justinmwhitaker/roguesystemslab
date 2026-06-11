from prospector.cli import prompt_for_run_config


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
