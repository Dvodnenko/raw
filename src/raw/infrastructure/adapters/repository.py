from typing import Optional
from sqlite3 import Connection

from ...domain import Task, TaskRepository, Spec
from .spec_compiler import SpecCompilerSQL


class TaskRepositorySQL(TaskRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSQL()

    def add(self, task: Task):

        stmt1 = """
            INSERT INTO entity (type, parent_id, title, description, icon)
            VALUES (:type, :parent_id, :title, :description, :icon)
            RETURNING id
        """

        generated_id = self._conn.execute(
            stmt1,
            {
                "type": "task",
                "parent_id": task.parent_id,
                "title": task.title,
                "description": task.description,
                "icon": task.icon,
            }
        ).fetchone()["id"]

        stmt2 = """
            INSERT INTO task (id, deadline, status)
            VALUES (:id, :deadline, :status)
        """

        self._conn.execute(
            stmt2,
            {
                "id": generated_id,
                "deadline": task.deadline.isoformat(),
                "status": task.status.value,
            }
        )

    def get_by_id(self, id: int) -> Optional[Task]:
        ...
    
    def get_by_title(self, title: str) -> Optional[Task]:
        ...

    def filter(self, spec: Spec = None):
        ...

    def save(self, task: Task):
        ...

    def remove(self, id: int):
        ...
    
    def rewrite_subtree_titles(
        self,
        old_prefix: str,
        new_prefix: str,
    ):
        ...
