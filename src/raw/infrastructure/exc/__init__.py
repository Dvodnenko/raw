from .integrity import ConstraintKind, resolve_integrity_error


class InfrastructureError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class StorageUnavailable(InfrastructureError):
    ...

class ConstraintViolated(InfrastructureError):
    ...
