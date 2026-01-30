from enum import Enum


class TaskStatus(Enum):
    ACTIVE = "active"
    DONE = "done"
    CANCELLED = "cancelled"

class EntityType(Enum):
    ENTITY = "entity" # general entity type for all cases
    
    TASK = "task"
