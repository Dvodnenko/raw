task_table = """
CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    deadline TEXT,
    status TEXT NOT NULL,

    FOREIGN KEY (id) REFERENCES identity(id) ON DELETE CASCADE
)
"""
