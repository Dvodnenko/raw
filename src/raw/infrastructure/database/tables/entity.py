entity_table = """
CREATE TABLE entity (
    id INTEGER PRIMARY KEY,
    type TEXT,
    parent_id INTEGER NULLABLE,
    title TEXT,
    description TEXT,
    icon TEXT,

    FOREIGN KEY (parent_id) REFERENCES entity(id) ON DELETE CASCADE
)
"""
