identity_table = """
CREATE TABLE identity (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    title TEXT NOT NULL UNIQUE
)
"""
