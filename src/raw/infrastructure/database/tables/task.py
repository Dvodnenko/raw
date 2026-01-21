task_table = """
CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    deadline TEXT,
    status TEXT NOT NULL,

    FOREIGN KEY (id) REFERENCES entity(id) ON DELETE CASCADE
)
"""
