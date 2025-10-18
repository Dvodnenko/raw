import json

from .services.folders import FolderService
from .services.sessions import SessionService


SERVICES = {
    "folders": FolderService(),
    "sessions": SessionService(),
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
    
    service_instance = SERVICES[args[0]]
    method = service_instance.__getattribute__(args[1])

    response = method(
        args=args[2:],
        flags=flags,
        **kwargs
    )

    return format_response_json(*response)
