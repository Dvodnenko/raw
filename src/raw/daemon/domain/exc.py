class Exc(Exception):
    """
    Base class for all my custom exceptions
    """
    ...


class UniquenessError(Exc):
    def __str__(self):
        return f"Unique constraint violated: {
            ", ".join([arg for arg in self.args])}"

class MissingIdentifierError(Exc):
    def __str__(self):
        return "Missing required identifier"

class EntryNotFoundError(Exc):
    def __str__(self):
        return "Entry not found"

class OperationNotFoundError(Exc):
    def __str__(self):
        return f"Operation not found: {self.args[0]}"
