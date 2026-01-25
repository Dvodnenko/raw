from .integrity import ConstraintKind, resolve_integrity_error


class InfrastructureError(Exception):
    ...


class StorageUnavailable(InfrastructureError):
    ...

class ConstraintViolated(InfrastructureError):
    ...
