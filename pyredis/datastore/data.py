from dataclasses import dataclass
from datetime import datetime


@dataclass
class Data:
    value: str
    expiry: datetime = None
