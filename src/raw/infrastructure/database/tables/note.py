note_table = """
CREATE TABLE IF NOT EXISTS note (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    content TEXT,

    FOREIGN KEY (id) REFERENCES identity(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES identity(id) ON DELETE CASCADE
)
"""
