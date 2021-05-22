
from dataclasses import dataclass, field


@dataclass
class ConnectResponse:
    error_code: int = 0


@dataclass
class RequestResponse:
    has_next: bool = False
    error: bool = False
    rows: list = field(default_factory=list)
