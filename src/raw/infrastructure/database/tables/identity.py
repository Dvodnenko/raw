identity_table = """
CREATE TABLE identity (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    title TEXT NOT NULL UNIQUE,
    parent_id INTEGER,

    FOREIGN KEY (parent_id) REFERENCES identity(id) ON DELETE CASCADE
)
"""
