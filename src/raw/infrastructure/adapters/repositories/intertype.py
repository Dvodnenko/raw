from sqlite3 import Connection

from ....domain import IntertypeRepository, EntityType, EntityType


class IntertypeRepositorySQL(IntertypeRepository):
    def __init__(self, conn: Connection):
        self._conn = conn

    def resolve_type(self, id: int) -> EntityType | None:
        row = self._conn.execute(
            "SELECT type FROM identity WHERE id = :id",
            {"id": id}
        ).fetchone()

        if not row:
            return None
        return EntityType(row["type"])
    
    def resolve_type_by_title(self, title: str) -> EntityType | None:
        row = self._conn.execute(
            "SELECT type FROM identity WHERE title = :title",
            {"title": title}
        ).fetchone()

        if not row:
            return None
        return EntityType(row["type"])
    
    def resolve_id_by_title(self, title: str) -> int | None:
        row = self._conn.execute(
            "SELECT id FROM identity WHERE title = :title",
            {"title": title}
        ).fetchone()

        if not row:
            return None
        return row["id"]

    def remove(self, id: int):
        stmt = """
            DELETE FROM identity
            WHERE id = :id    
        """
        self._conn.execute(
            stmt,
            {"id": id}
        )
    
    def rewrite_subtree_titles(
        self,
        old_prefix: str,
        new_prefix: str,
    ):
        tables = ["identity", "task", "note", "session", "folder"]
        
        for table in tables:
            stmt = f"""
                UPDATE {table}
                SET title = replace(title, :old_prefix, :new_prefix)
                WHERE title LIKE :old_prefix || '/%';
            """
            self._conn.execute(stmt, {"old_prefix": old_prefix, "new_prefix": new_prefix})
