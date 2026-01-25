from enum import Enum


class TaskStatus(Enum):
    ACTIVE = "active"
    DONE = "done"
    CANCELLED = "cancelled"

class EntityType(Enum):
    TASK = "task"
