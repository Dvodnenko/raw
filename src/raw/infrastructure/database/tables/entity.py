entity_table = """
CREATE TABLE entity (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    parent_id INTEGER,
    title TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,

    FOREIGN KEY (parent_id) REFERENCES entity(id) ON DELETE CASCADE
)
"""
