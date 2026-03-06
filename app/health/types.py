from dataclasses import dataclass
from typing import Optional

@dataclass
class HealthStatus:
    bot: bool = False
    db: bool = False
    error: Optional[str] = None
