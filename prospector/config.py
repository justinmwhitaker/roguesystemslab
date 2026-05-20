from dataclasses import dataclass


@dataclass
class RunConfig:
    product: str
    icp: str
    filters: str
    max_prospects: int = 50
    target_company_size: str = ""
    sources: tuple[str, ...] = ("web", "linkedin")
    lookback_days: int = 30

    def __post_init__(self) -> None:
        if self.max_prospects < 0:
            raise ValueError("max_prospects must be non-negative")
        if not 1 <= self.lookback_days <= 180:
            raise ValueError("lookback_days must be between 1 and 180")
