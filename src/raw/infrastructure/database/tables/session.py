session_table = """
CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    message TEXT NOT NULL,
    summary TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,

    FOREIGN KEY (id) REFERENCES identity(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES identity(id) ON DELETE CASCADE
)
"""
