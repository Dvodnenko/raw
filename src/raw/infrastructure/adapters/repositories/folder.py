from typing import Optional
from sqlite3 import Connection, OperationalError, IntegrityError

from sqlglot import exp

from ....domain import Folder, FolderRepository, Spec
from ..spec_compiler import SpecCompilerSQL
from ...exc import ConstraintViolated, StorageUnavailable


class FolderRepositorySQL(FolderRepository):
    def __init__(self, conn: Connection):
        self._conn = conn
        self._spec_compiler = SpecCompilerSQL()

    def add(self, folder: Folder):

        stmt1 = """
            INSERT INTO identity (type, title, parent_id)
            VALUES (:type, :title, :parent_id)
            RETURNING id
        """

        stmt2 = """
            INSERT INTO folder (id, parent_id, title, description, icon)
            VALUES (:id, :parent_id, :title, :description, :icon)
        """
        try:
            generated_id = self._conn.execute(
                stmt1,
                {
                    "type": "folder",
                    "title": folder.title,
                    "parent_id": folder.parent_id,
                }
            ).fetchone()["id"]

            self._conn.execute(
                stmt2,
                {
                    "id": generated_id,
                    "parent_id": folder.parent_id,
                    "title": folder.title,
                    "description": folder.description,
                    "icon": folder.icon,
                }
            )
        except OperationalError as exc:
            raise StorageUnavailable("storage unavailable") from exc
        except IntegrityError as exc:
            raise ConstraintViolated() from exc

    def get_by_id(self, id: int) -> Optional[Folder]:
        query = """
            SELECT * FROM folder
            WHERE id = :id
        """

        result = self._conn.execute(
            query, {"id": id}
        ).fetchone()

        if not result:
            return None

        return Folder(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
        )
    
    def get_by_title(self, title: str) -> Optional[Folder]:
        query = """
            SELECT * FROM folder
            WHERE title = :title
        """

        result = self._conn.execute(
            query, {"title": title}
        ).fetchone()

        if not result:
            return None

        return Folder(
            id=result["id"],
            title=result["title"],
            description=result["description"],
            icon=result["icon"],
            parent_id=result["parent_id"],
        )

    def filter(self, spec: Spec = None, order_by: str = None, reverse: bool = False):
        query = self._build_task_select(spec, order_by, reverse)

        cursor = self._conn.cursor()
        cursor.execute(query.sql("sqlite"))

        for row in cursor:
            yield Folder(
                id=row["id"],
                parent_id=row["parent_id"],
                title=row["title"],
                description=row["description"],
                icon=row["icon"],
            )

    def save(self, folder: Folder):
        stmt1 = """
            UPDATE identity
            SET title = :title,
                parent_id = :parent_id
            WHERE id = :id
        """

        stmt2 = """
            UPDATE folder
            SET parent_id = :parent_id,
                title = :title,
                description = :description,
                icon = :icon
            WHERE id = :id
        """
        try:
            self._conn.execute(
                stmt1,
                {
                    "id": folder.id,
                    "title": folder.title,
                    "parent_id": folder.parent_id,
                }
            )

            self._conn.execute(
                stmt2,
                {
                    "id": folder.id,
                    "parent_id": folder.parent_id,
                    "title": folder.title,
                    "description": folder.description,
                    "icon": folder.icon,
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
        query = exp.select("*").from_("folder")
        
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
