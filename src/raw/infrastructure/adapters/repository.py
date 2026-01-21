from typing import Optional
from sqlite3 import Connection
from datetime import datetime

from ...domain import Task, TaskStatus, TaskRepository, Spec
from .spec_compiler import SpecCompilerSQL


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

        generated_id = self._conn.execute(
            stmt1,
            {
                "type": "task",
                "title": task.title,
                "parent_id": task.parent_id,
            }
        ).fetchone()["id"]

        stmt2 = """
            INSERT INTO task (id, title, description, icon, deadline, status)
            VALUES (:id, :title, :description, :icon, :deadline, :status)
        """

        self._conn.execute(
            stmt2,
            {
                "id": generated_id,
                "title": task.title,
                "description": task.description,
                "icon": task.icon,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "status": task.status.value,
            }
        )

    def get_by_id(self, id: int) -> Optional[Task]:
        query = """
            SELECT * FROM identity
            JOIN task ON identity.id = task.id
            WHERE identity.id = :id
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
            status=TaskStatus(result["status"]),
            deadline=(
                datetime.fromisoformat(result["deadline"])
                if result["deadline"]
                else None
            )
        )
    
    def get_by_title(self, title: str) -> Optional[Task]:
        query = """
            SELECT * FROM identity
            JOIN task ON identity.id = task.id
            WHERE identity.title = :title
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
            status=TaskStatus(result["status"]),
            deadline=(
                datetime.fromisoformat(result["deadline"])
                if result["deadline"]
                else None
            )
        )

    def filter(self, spec: Spec = None):
        ...

    def save(self, task: Task):
        stmt = """
            UPDATE identity
            SET title = :title,
                parent_id = :parent_id
            WHERE id = :id
        """

        self._conn.execute(
            stmt,
            {
                "id": task.id,
                "title": task.title,
                "parent_id": task.parent_id,
            }
        )

        stmt = """
            UPDATE task
            SET title = :title,
                description = :description,
                icon = :icon,
                deadline = :deadline,
                status = :status
            WHERE id = :id
        """

        self._conn.execute(
            stmt,
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "icon": task.icon,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "status": task.status.value,
            }
        )

    def remove(self, id: int):
        ...
    
    def rewrite_subtree_titles(
        self,
        old_prefix: str,
        new_prefix: str,
    ):
        stmt = """
            UPDATE identity
            SET title = replace(title, :old_prefix, :new_prefix)
            WHERE title LIKE :old_prefix || '/%';
        """

        self._conn.execute(
            stmt,
            {"old_prefix": old_prefix, "new_prefix": new_prefix}
        )

        stmt = """
            UPDATE task
            SET title = replace(title, :old_prefix, :new_prefix)
            WHERE title LIKE :old_prefix || '/%';
        """

        self._conn.execute(
            stmt,
            {"old_prefix": old_prefix, "new_prefix": new_prefix}
        )
