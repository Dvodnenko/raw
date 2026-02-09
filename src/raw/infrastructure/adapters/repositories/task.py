from typing import Optional
from sqlite3 import Connection, OperationalError, IntegrityError
from datetime import datetime

from sqlglot import exp

from ....domain import Task, TaskRepository, Spec
from ..spec_compiler import SpecCompilerSQL
from ...exc import ConstraintViolated, StorageUnavailable


class TaskRepositorySQL(TaskRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSQL()

    def add(self, task: Task):

        stmt1 = """
            INSERT INTO identity (type, title, parent_id)
            VALUES (:type, :title, :parent_id)
            RETURNING id
        """

        stmt2 = """
            INSERT INTO task (id, parent_id, title, description, icon, deadline, status)
            VALUES (:id, :parent_id, :title, :description, :icon, :deadline, :status)
        """
        try:
            generated_id = self._conn.execute(
                stmt1,
                {
                    "type": "task",
                    "title": task.title,
                    "parent_id": task.parent_id,
                }
            ).fetchone()["id"]

            self._conn.execute(
                stmt2,
                {
                    "id": generated_id,
                    "parent_id": task.parent_id,
                    "title": task.title,
                    "description": task.description,
                    "icon": task.icon,
                    "deadline": task.deadline.isoformat(sep=" ") if task.deadline else None,
                    "status": task.status,
                }
            )
        except OperationalError as exc:
            raise StorageUnavailable("storage unavailable") from exc
        except IntegrityError as exc:
            raise ConstraintViolated() from exc

    def get_by_id(self, id: int) -> Optional[Task]:
        query = """
            SELECT * FROM task
            WHERE id = :id
        """

        result = self._conn.execute(
            query, {"id": id}
        ).fetchone()

        if not result:
            return None

        return Task(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
            status=result["status"],
            deadline=(
                datetime.fromisoformat(result["deadline"])
                if result["deadline"]
                else None
            )
        )
    
    def get_by_title(self, title: str) -> Optional[Task]:
        query = """
            SELECT * FROM task
            WHERE title = :title
        """

        result = self._conn.execute(
            query, {"title": title}
        ).fetchone()

        if not result:
            return None

        return Task(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
            status=result["status"],
            deadline=(
                datetime.fromisoformat(result["deadline"])
                if result["deadline"]
                else None
            )
        )

    def filter(self, spec: Spec = None, order_by: str = None, reverse: bool = False):
        query = self._build_task_select(spec, order_by, reverse)

        cursor = self._conn.cursor()
        cursor.execute(query.sql("sqlite"))

        for row in cursor:
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

    def save(self, task: Task):
        stmt1 = """
            UPDATE identity
            SET title = :title,
                parent_id = :parent_id
            WHERE id = :id
        """

        stmt2 = """
            UPDATE task
            SET parent_id = :parent_id,
                title = :title,
                description = :description,
                icon = :icon,
                deadline = :deadline,
                status = :status
            WHERE id = :id
        """
        try:
            self._conn.execute(
                stmt1,
                {
                    "id": task.id,
                    "title": task.title,
                    "parent_id": task.parent_id,
                }
            )

            self._conn.execute(
                stmt2,
                {
                    "id": task.id,
                    "parent_id": task.parent_id,
                    "title": task.title,
                    "description": task.description,
                    "icon": task.icon,
                    "deadline": task.deadline.isoformat(sep=" ") if task.deadline else None,
                    "status": task.status,
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
        query = exp.select("*").from_("task")
        
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
