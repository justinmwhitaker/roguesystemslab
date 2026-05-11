from __future__ import annotations


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def conversion_score(role_fit: float, company_fit: float, topic_relevance: float, sentiment_component: float, intent_signal: float) -> float:
    score = (
        0.35 * role_fit
        + 0.25 * company_fit
        + 0.20 * topic_relevance
        + 0.10 * sentiment_component
        + 0.10 * intent_signal
    )
    return round(clamp(score), 2)
