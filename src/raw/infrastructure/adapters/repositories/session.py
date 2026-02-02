from typing import Optional
from sqlite3 import Connection, OperationalError, IntegrityError
from datetime import datetime

from sqlglot import exp

from ....domain import Session, SessionRepository, Spec, FieldSpec, Operator
from ..spec_compiler import SpecCompilerSQL
from ...exc import ConstraintViolated, StorageUnavailable


class SessionRepositorySQL(SessionRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSQL()

    def add(self, session: Session):

        stmt1 = """
            INSERT INTO identity (type, title, parent_id)
            VALUES (:type, :title, :parent_id)
            RETURNING id
        """

        stmt2 = """
            INSERT INTO session (
                id, parent_id, title, description, icon, message, summary, started_at, ended_at)
            VALUES (:id, :parent_id, :title, :description, :icon, :message, :summary, :started_at, :ended_at)
        """
        try:
            generated_id = self._conn.execute(
                stmt1,
                {
                    "type": "session",
                    "title": session.title,
                    "parent_id": session.parent_id,
                }
            ).fetchone()["id"]

            self._conn.execute(
                stmt2,
                {
                    "id": generated_id,
                    "parent_id": session.parent_id,
                    "title": session.title,
                    "description": session.description,
                    "icon": session.icon,
                    "message": session.message,
                    "summary": session.summary,
                    "started_at": session.started_at.isoformat(sep=" "),
                    "ended_at": (
                        session.ended_at.isoformat(sep=" ")
                        if session.ended_at
                        else None),
                }
            )
        except OperationalError as exc:
            raise StorageUnavailable("storage unavailable") from exc
        except IntegrityError as exc:
            raise ConstraintViolated() from exc

    def get_by_id(self, id: int) -> Optional[Session]:
        query = """
            SELECT * FROM session
            WHERE id = :id
        """

        result = self._conn.execute(
            query, {"id": id}
        ).fetchone()

        if not result:
            return None

        return Session(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
            message=result["message"],
            summary=result["summary"],
            started_at=datetime.fromisoformat(result["started_at"]),
            ended_at=(datetime.fromisoformat(result["ended_at"])
                if result["ended_at"]
                else None)
            )
    
    def get_by_title(self, title: str) -> Optional[Session]:
        query = """
            SELECT * FROM session
            WHERE title = :title
        """

        result = self._conn.execute(
            query, {"title": title}
        ).fetchone()

        if not result:
            return None

        return Session(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
            message=result["message"],
            summary=result["summary"],
            started_at=datetime.fromisoformat(result["started_at"]),
            ended_at=(datetime.fromisoformat(result["ended_at"])
                if result["ended_at"]
                else None)
            )

    def get_active_sessions(self, order_by: str = None, reverse: bool = False):
        spec = FieldSpec("ended_at", Operator.EQ, None)
        yield from self.filter(spec, order_by, reverse)

    def filter(self, spec: Spec = None, order_by: str = None, reverse: bool = False):
        query = self._build_task_select(spec, order_by, reverse)

        cursor = self._conn.cursor()
        cursor.execute(query.sql("sqlite"))

        for row in cursor:
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

    def save(self, session: Session):
        stmt1 = """
            UPDATE identity
            SET title = :title,
                parent_id = :parent_id
            WHERE id = :id
        """

        stmt2 = """
            UPDATE session
            SET parent_id = :parent_id,
                title = :title,
                description = :description,
                icon = :icon,
                message = :message,
                summary = :summary,
                started_at = :started_at,
                ended_at = :ended_at
            WHERE id = :id
        """
        try:
            self._conn.execute(
                stmt1,
                {
                    "id": session.id,
                    "title": session.title,
                    "parent_id": session.parent_id,
                }
            )

            self._conn.execute(
                stmt2,
                {
                    "id": session.id,
                    "parent_id": session.parent_id,
                    "title": session.title,
                    "description": session.description,
                    "icon": session.icon,
                    "message": session.message,
                    "summary": session.summary,
                    "started_at": session.started_at.isoformat(sep=" "),
                    "ended_at": (
                        session.ended_at.isoformat(sep=" ")
                        if session.ended_at
                        else None),
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
        query = exp.select("*").from_("session")
        
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
