from sqlite3 import Connection

from ....domain import (
    IntertypeRepository, EntityType, NotFound,
    EntityRef, EntityType
)


class IntertypeRepositorySQL(IntertypeRepository):
    def __init__(self, conn: Connection):
        self._conn = conn

    def resolve_type(self, id: int) -> EntityType:
        row = self._conn.execute(
            "SELECT type FROM identity WHERE id = :id",
            {"id": id}
        ).fetchone()

        if not row:
            raise NotFound(EntityRef(id))
        return EntityType(row["type"])
