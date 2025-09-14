from enum import Enum
from datetime import datetime, timezone

class Mode(Enum):
    OPEN_ALL = 1
    DIRECT_ONLY = 2
    IN_PRODUCTION = 3
    BLOCK_ONSITE = 4
    def __int__(self): return self.value

def now_utc():
    return datetime.now(timezone.utc).isoformat()

STORE = {
    "mode": Mode.OPEN_ALL,
    "mode_version": 1,
    "orders": {},
    "timeslots": set(),
    "presence": {},
    "labels": {},
    "inventory": {"PZ001": 50, "PZ002": 50},
    "idem": {},
}
