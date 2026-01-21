task_table = """
CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    deadline TEXT,
    status TEXT NOT NULL,

    FOREIGN KEY (id) REFERENCES identity(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES identity(id) ON DELETE CASCADE
)
"""
