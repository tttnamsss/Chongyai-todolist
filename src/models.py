from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid


class Priority(Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    details: str = ""
    priority: Priority = Priority.MID
    status: Status = Status.PENDING
    owner: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z"
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TodoItem":
        return TodoItem(
            id=d.get("id", str(uuid.uuid4())),
            title=d.get("title", ""),
            details=d.get("details", ""),
            priority=Priority(d.get("priority", Priority.MID.value)),
            status=Status(d.get("status", Status.PENDING.value)),
            owner=d.get("owner"),
            created_at=d.get(
                "created_at", datetime.now(timezone.utc).isoformat() + "Z"
            ),
            updated_at=d.get(
                "updated_at", datetime.now(timezone.utc).isoformat() + "Z"
            ),
        )
