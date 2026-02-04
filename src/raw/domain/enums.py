from enum import Enum


class EntityType(Enum):
    ENTITY = "entity" # general entity type for all cases
    
    TASK = "task"
    NOTE = "note"
    SESSION = "session"
    FOLDER = "folder"
