from prospector.sources import LinkedInSourceAdapter, WebSourceAdapter, get_adapters


def test_get_adapters_returns_expected_types():
    adapters = get_adapters(("web", "linkedin"))
    assert len(adapters) == 2
    assert isinstance(adapters[0], WebSourceAdapter)
    assert isinstance(adapters[1], LinkedInSourceAdapter)
