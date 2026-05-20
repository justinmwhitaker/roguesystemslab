from dataclasses import dataclass


@dataclass
class RunConfig:
    product: str
    icp: str
    filters: str
    max_prospects: int = 50

    def __post_init__(self) -> None:
        if self.max_prospects < 0:
            raise ValueError("max_prospects must be non-negative")
