task_table = """
CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    deadline TEXT NULLABLE,
    status TEXT,

    FOREIGN KEY (id) REFERENCES entity(id) ON DELETE CASCADE
)
"""
