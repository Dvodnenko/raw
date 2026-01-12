from typing import Optional

from sqlalchemy import Connection, select, text

from ...domain import Task, TaskRepository, Spec
from ..database.tables import entity_table, task_table
from .spec_compiler import SpecCompilerSA


class TaskRepositorySA(TaskRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSA()

    def add(self, task: Task):
        stmt1 = entity_table.insert().values(
            title=task.title,
            description=task.description,
            icon=task.icon,
            type="task",
            parent_id=task.parent_id,
        ).returning(entity_table.c.id)

        generated_id = self._conn.execute(stmt1).one().id

        self._conn.execute(
            task_table.insert().values(
                id=generated_id,
                status=task.status,
                deadline=task.deadline,
            )
        )

    def get_by_id(self, id: int) -> Optional[Task]:
        stmt = (
            select(
                entity_table,
                task_table.c.status,
                task_table.c.deadline
            )
            .where(entity_table.c.id == id)
            .join(task_table, task_table.c.id == entity_table.c.id)
        )
        row = self._conn.execute(stmt).fetchone()

        if not row:
            return None

        return Task(
            id=row.id,
            title=row.title,
            description=row.description,
            parent_id=row.parent_id,
            icon=row.icon,
            status=row.status,
            deadline=row.deadline,
        )
    
    def get_by_title(self, title: str) -> Optional[Task]:
        stmt = (
            select(
                entity_table,
                task_table.c.status,
                task_table.c.deadline
            )
            .where(entity_table.c.title == title)
            .join(task_table, task_table.c.id == entity_table.c.id)
        )
        row = self._conn.execute(stmt).fetchone()

        if not row:
            return None

        return Task(
            id=row.id,
            title=row.title,
            description=row.description,
            parent_id=row.parent_id,
            icon=row.icon,
            status=row.status,
            deadline=row.deadline,
        )

    def filter(self, spec: Spec = None):

        stmt = (
            select(
                entity_table,

                task_table.c.status,
                task_table.c.deadline,
            )
            .join(task_table, task_table.c.id == entity_table.c.id)
        )
        if spec:
            where = self._spec_compiler.compile(spec, stmt)
            stmt = select("*").select_from(stmt).where(where)
        
        for row in (
            self._conn
            .execution_options(yield_per=100)
            .execute(
                stmt
            )
        ):
            yield Task(
                id=row.id,
                title=row.title,
                description=row.description,
                icon=row.icon,
                status=row.status,
                deadline=row.deadline,
            )

    def save(self, task: Task):
        self._conn.execute(
            entity_table.update()
            .where(entity_table.c.id == task.id)
            .values(
                title=task.title,
                description=task.description,
                icon=task.icon,
                parent_id=task.parent_id,
            )
        )
        self._conn.execute(
            task_table.update()
            .where(task_table.c.id == task.id)
            .values(
                status=task.status,
                deadline=task.deadline,
            )
        )

    def remove(self, id: int):
        self._conn.execute(
            entity_table.delete().where(entity_table.c.id == id)
        )
    
    def rewrite_subtree_titles(
        self,
        old_prefix: str,
        new_prefix: str,
    ):
        stmt = text("""
            UPDATE entity
            SET title = :new || substr(title, :old_len + 1)
            WHERE title LIKE :old || '/%'
        """)
        self._conn.execute(
            stmt,
            {
                "old": old_prefix,
                "new": new_prefix,
                "old_len": len(old_prefix),
            }
        )
