folder_table = """
CREATE TABLE IF NOT EXISTS folder (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,

    FOREIGN KEY (id) REFERENCES identity(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES identity(id) ON DELETE CASCADE
)
"""
