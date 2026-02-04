from typing import Optional
from datetime import datetime

from .entities import Task, Note, Session, Folder
from ..shared import MISSING


class TaskEditor:
    def __init__(
        self,
        title: Optional[str] = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[str] = MISSING,
        status: Optional[str] = MISSING,
        deadline: Optional[datetime] = MISSING,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.status = status
        self.deadline = deadline

    def apply(self, task: Task) -> Task:
        return Task(
            id=task.id,
            title=self.title if self.title is not MISSING else task.title,
            description=(
                self.description
                if self.description is not MISSING
                else task.description
            ),
            icon=self.icon if self.icon is not MISSING else task.icon,
            parent_id=task.parent_id, # it cannot be changed here
            status=self.status if self.status is not MISSING else task.status,
            deadline=self.deadline if self.deadline is not MISSING else task.deadline,
        )

class NoteEditor:
    def __init__(
        self,
        title: Optional[str] = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[str] = MISSING,
        content: Optional[str] = MISSING,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.content = content

    def apply(self, note: Note) -> Note:
        return Note(
            id=note.id,
            title=self.title if self.title is not MISSING else note.title,
            description=(
                self.description
                if self.description is not MISSING
                else note.description
            ),
            icon=self.icon if self.icon is not MISSING else note.icon,
            parent_id=note.parent_id, # it cannot be changed here
            content=self.content if self.content is not MISSING else note.content,
        )

class SessionEditor:
    def __init__(
        self,
        title: Optional[str] = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[str] = MISSING,
        message: Optional[str] = MISSING,
        summary: Optional[str] = MISSING,
        started_at: Optional[datetime] = MISSING,
        ended_at: Optional[datetime] = MISSING,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.message = message
        self.summary = summary
        self.started_at = started_at
        self.ended_at = ended_at

    def apply(self, session: Session) -> Session:
        return Session(
            id=session.id,
            title=self.title if self.title is not MISSING else session.title,
            description=(
                self.description
                if self.description is not MISSING
                else session.description
            ),
            icon=self.icon if self.icon is not MISSING else session.icon,
            parent_id=session.parent_id, # it cannot be changed here
            message=self.message if self.message is not MISSING else session.message,
            summary=self.summary if self.summary is not MISSING else session.summary,
            started_at=self.started_at if self.started_at is not MISSING else session.started_at,
            ended_at=self.ended_at if self.ended_at is not MISSING else session.ended_at
        )

class FolderEditor:
    def __init__(
        self,
        title: Optional[str] = MISSING,
        description: Optional[str] = MISSING,
        icon: Optional[str] = MISSING,
    ):
        self.title = title
        self.description = description
        self.icon = icon

    def apply(self, folder: Folder) -> Folder:
        return Folder(
            id=folder.id,
            title=self.title if self.title is not MISSING else folder.title,
            description=(
                self.description
                if self.description is not MISSING
                else folder.description
            ),
            icon=self.icon if self.icon is not MISSING else folder.icon,
            parent_id=folder.parent_id, # it cannot be changed here
        )
