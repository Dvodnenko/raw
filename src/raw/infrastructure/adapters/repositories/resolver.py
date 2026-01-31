from sqlite3 import Connection

from ....domain import (
    EntityTypeResolver, EntityType, NotFound,
    EntityRef, EntityType
)


class EntityTypeResolverSQL(EntityTypeResolver):
    def __init__(self, conn: Connection):
        self._conn = conn

    def resolve(self, id: int) -> EntityType:
        row = self._conn.execute(
            "SELECT type FROM identity WHERE id = :id",
            {"id": id}
        ).fetchone()

        if not row:
            raise NotFound(EntityRef(id))
        return EntityType(row["type"])
