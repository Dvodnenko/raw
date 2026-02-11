from sqlite3 import Connection
from datetime import datetime

from sqlglot import exp

from ....domain import (
    IntertypeRepository, EntityType, EntityType, Spec,
    Task, Note, Session, Folder, And, FieldSpec, Operator
)
from ..spec_compiler import SpecCompilerSQL


class IntertypeRepositorySQL(IntertypeRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSQL()

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
    
    def filter(self, types, spec = None, order_by = None, reverse = False):
        # mix user's specification with types
        if spec is None:
            spec = FieldSpec("type", Operator.IN, types)
        else:
            spec = And(
                spec,
                FieldSpec("type", Operator.IN, types)
            )
        query = self._build_task_select(spec, order_by, reverse)
        cursor = self._conn.cursor()
        cursor.execute(query.sql("sqlite"))

        for row in cursor:
            match row["type"]:
                case "task":
                    yield Task(
                        id=row["id"],
                        parent_id=row["parent_id"],
                        title=row["title"],
                        description=row["description"],
                        icon=row["icon"],
                        status=row["status"],
                        deadline=(
                            datetime.fromisoformat(row["deadline"])
                            if row["deadline"]
                            else None
                        )
                    )
                case "note":
                    yield Note(
                        id=row["id"],
                        parent_id=row["parent_id"],
                        title=row["title"],
                        description=row["description"],
                        icon=row["icon"],
                        content=row["content"],
                    )
                case "session":
                    yield Session(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        icon=row["icon"],
                        parent_id=row["parent_id"],
                        message=row["message"],
                        summary=row["summary"],
                        started_at=datetime.fromisoformat(row["started_at"]),
                        ended_at=(datetime.fromisoformat(row["ended_at"])
                            if row["ended_at"]
                            else None)
                    )
                case "folder":
                    yield Folder(
                        id=row["id"],
                        parent_id=row["parent_id"],
                        title=row["title"],
                        description=row["description"],
                        icon=row["icon"],
                    )

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

    def _build_task_select(
        self,
        spec: Spec | None,
        order_by: str = None,
        reverse: bool = False
    ) -> exp.Select:
        query = (
            exp.select(
                "identity.*",
                
                "COALESCE(task.description, note.description, session.description, folder.description, '') AS description", 
                "COALESCE(task.icon, note.icon, session.icon, folder.icon, '') AS icon", 

                "task.deadline",
                "task.status",

                "note.content",

                "session.message",
                "session.summary",
                "session.started_at",
                "session.ended_at",
            )
            .from_("identity")
            .join("task", "identity.id = task.id", join_type="left")
            .join("note", "identity.id = note.id", join_type="left")
            .join("session", "identity.id = session.id", join_type="left")
            .join("folder", "identity.id = folder.id", join_type="left")
        )
        
        if spec:
            query = query.where(self._spec_compiler.compile(spec))

        if order_by:
            query = query.order_by(order_by)

            if reverse: # cannot be reversed if order_by isn't provided
                query = query.desc()

        # it will raise sqlglot.ParseError if syntax is invalid.
        # CLI will show it as "unexpected error"
        query.sql("sqlite")

        return query
