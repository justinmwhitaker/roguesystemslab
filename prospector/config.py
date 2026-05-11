from dataclasses import dataclass


@dataclass
class RunConfig:
    product: str
    icp: str
    filters: str
    max_prospects: int = 50
