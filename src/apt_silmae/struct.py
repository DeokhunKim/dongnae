from dataclasses import dataclass, astuple

# definition
@dataclass
class ApiData:
    price: int
    construction_date: int
    trade_date: int
    net_leasable_area: float
    region_code: int
    dong: str
    jibun: str
    apt: str


