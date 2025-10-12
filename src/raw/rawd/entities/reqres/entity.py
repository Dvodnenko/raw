import dataclasses
import json
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar


T = TypeVar("T")

@dataclass
class Response(Generic[T]):
    message: Optional[str] = None
    status_code: int = 0
    data: Optional[T] = None

    @property
    def success(self) -> bool:
        return self.status_code == 0
    
    def to_bytes(self) -> "Response":
        return json.dumps(dataclasses.asdict(self)).encode("utf-8")
    
    @staticmethod
    def from_bytes(data: bytes) -> "Response":
        return Response(**json.loads(data.decode("utf-8")))


@dataclass
class Request(Generic[T]):
    group: str
    command: str
    args: list[str]
    options: dict[str, str]

    def to_bytes(self) -> "Request":
        return json.dumps(dataclasses.asdict(self)).encode("utf-8")
    
    @staticmethod
    def from_bytes(data: bytes) -> "Request":
        return Request(**json.loads(data.decode("utf-8")))
