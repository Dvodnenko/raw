from typing import Optional
from sqlite3 import Connection, OperationalError, IntegrityError

from sqlglot import exp

from ....domain import Note, NoteRepository, Spec
from ..spec_compiler import SpecCompilerSQL
from ...exc import ConstraintViolated, StorageUnavailable


class NoteRepositorySQL(NoteRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSQL()

    def add(self, note: Note):

        stmt1 = """
            INSERT INTO identity (type, title, parent_id)
            VALUES (:type, :title, :parent_id)
            RETURNING id
        """

        stmt2 = """
            INSERT INTO note (id, parent_id, title, description, icon, content)
            VALUES (:id, :parent_id, :title, :description, :icon, :content)
        """
        try:
            generated_id = self._conn.execute(
                stmt1,
                {
                    "type": "note",
                    "title": note.title,
                    "parent_id": note.parent_id,
                }
            ).fetchone()["id"]

            self._conn.execute(
                stmt2,
                {
                    "id": generated_id,
                    "parent_id": note.parent_id,
                    "title": note.title,
                    "description": note.description,
                    "icon": note.icon,
                    "content": note.content,
                }
            )
        except OperationalError as exc:
            raise StorageUnavailable("storage unavailable") from exc
        except IntegrityError as exc:
            raise ConstraintViolated() from exc

    def get_by_id(self, id: int) -> Optional[Note]:
        query = """
            SELECT * FROM note
            WHERE id = :id
        """

        result = self._conn.execute(
            query, {"id": id}
        ).fetchone()

        if not result:
            return None

        return Note(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
            content=result["content"],
        )
    
    def get_by_title(self, title: str) -> Optional[Note]:
        query = """
            SELECT * FROM note
            WHERE title = :title
        """

        result = self._conn.execute(
            query, {"title": title}
        ).fetchone()

        if not result:
            return None

        return Note(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
            content=result["content"],
        )

    def filter(self, spec: Spec = None, order_by: str = None, reverse: bool = False):
        query = self._build_task_select(spec, order_by, reverse)

        cursor = self._conn.cursor()
        cursor.execute(query.sql("sqlite"))

        for row in cursor:
            yield Note(
                id=row["id"],
                parent_id=row["parent_id"],
                title=row["title"],
                description=row["description"],
                icon=row["icon"],
                content=row["content"],
            )

    def save(self, note: Note):
        stmt1 = """
            UPDATE identity
            SET title = :title,
                parent_id = :parent_id
            WHERE id = :id
        """

        stmt2 = """
            UPDATE note
            SET parent_id = :parent_id,
                title = :title,
                description = :description,
                icon = :icon,
                content = :content
            WHERE id = :id
        """
        try:
            self._conn.execute(
                stmt1,
                {
                    "id": note.id,
                    "title": note.title,
                    "parent_id": note.parent_id,
                }
            )

            self._conn.execute(
                stmt2,
                {
                    "id": note.id,
                    "parent_id": note.parent_id,
                    "title": note.title,
                    "description": note.description,
                    "icon": note.icon,
                    "content": note.content,
                }
            )
        except OperationalError as exc:
            raise StorageUnavailable("storage unavailable") from exc
        except IntegrityError as exc:
            raise ConstraintViolated() from exc

    def _build_task_select(
        self,
        spec: Spec | None,
        order_by: str = None,
        reverse: bool = False
    ) -> exp.Select:
        query = exp.select("*").from_("note")
        
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
