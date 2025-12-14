import json

from .services.base import Service
from .services.folders import FolderService
from .services.sessions import SessionService
from .services.tags import TagService
from .services.tasks import TaskService
from .services.notes import NoteService
from .repositories.folder import saFolderRepository
from .repositories.session import saSessionRepository
from .repositories.tag import saTagRepository
from .repositories.task import saTaskRepository
from .repositories.note import saNoteRepository
from .database.session import Session
from .funcs import asexc


SERVICES = {
    "folders": FolderService,
    "sessions": SessionService,
    "tags": TagService,
    "tasks": TaskService,
    "notes": NoteService,
}

REPOSITORIES = {
    "folders": saFolderRepository,
    "sessions": saSessionRepository,
    "tags": saTagRepository,
    "tasks": saTaskRepository,
    "notes": saNoteRepository,
}


def format_response_json(
    message: str,
    status_code: int
) -> str:
    return json.dumps({
        "message": message,
        "status_code": status_code
    }) + "\n"


def handlecmd(request: str):
    rspd: dict = json.loads(request)
    _, flags, _ = rspd["ps"]["afk"]

    quotes = "q" in flags

    orm_session = Session()
    repository_instance = REPOSITORIES.get(rspd["source"][0])(orm_session)
    service_instance: Service = SERVICES.get(rspd["source"][0])(repository_instance)
    if not service_instance:
        yield format_response_json(f"Service not found: {rspd["source"][0]}", 1)
        return
    
    method = service_instance.execute(rspd)

    try:
        if quotes:
            for row, status_code in method:
                yield format_response_json(f'"{row}"', status_code)
        else:
            for row, status_code in method:
                yield format_response_json(row, status_code)

    except Exception as e:
        method.close()
        yield format_response_json(asexc(e), 1)
    finally:
        orm_session.expunge_all()
        orm_session.close()
        return
