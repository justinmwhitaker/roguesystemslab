from prospector.scoring import conversion_score


def test_conversion_score_bounds():
    assert conversion_score(200, 200, 200, 200, 200) == 100.0
    assert conversion_score(-10, -10, -10, -10, -10) == 0.0
