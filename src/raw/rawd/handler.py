import json

from .services.folders import FolderService
from .services.sessions import SessionService
from .services.tags import TagService
from .repositories.folder import saFolderRepository
from .repositories.session import saSessionRepository
from .repositories.tag import saTagRepository
from .database.session import Session


SERVICES = {
    "folders": FolderService,
    "sessions": SessionService,
    "tags": TagService,
}

REPOSITORIES = {
    "folders": saFolderRepository,
    "sessions": saSessionRepository,
    "tags": saTagRepository,
}


def format_response_json(
    message: str,
    status_code: int
) -> str:
    return json.dumps({
        "message": message,
        "status_code": status_code
    })


def handlecmd(request: str):
    data: dict = json.loads(request)

    args = data["args"]
    kwargs = data["kwargs"]
    flags = data["flags"]

    orm_session = Session()
    repository_instance = REPOSITORIES.get(args[0])(orm_session)
    service_instance = SERVICES.get(args[0])(repository_instance)
    if not service_instance:
        return format_response_json(f"Service not found: {args[0]}", 1)
    if not hasattr(service_instance, args[1]):
        return format_response_json(f"Method not found: {args[0]}.{args[1]}", 1)
    method = service_instance.__getattribute__(args[1])

    try:
        response = method(
            args=args[2:],
            flags=flags,
            **kwargs
        )
    except Exception as e:
        if "v" in flags:
            response = f"An error occurred: {e}", 1
        else:
            response = "An error occurred", 1
    finally:
        orm_session.close()
        return format_response_json(*response)
