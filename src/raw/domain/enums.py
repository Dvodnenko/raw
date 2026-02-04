from enum import Enum


class TaskStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DONE = "done"
    CANCELLED = "cancelled"

class EntityType(Enum):
    ENTITY = "entity" # general entity type for all cases
    
    TASK = "task"
    NOTE = "note"
    SESSION = "session"
    FOLDER = "folder"
