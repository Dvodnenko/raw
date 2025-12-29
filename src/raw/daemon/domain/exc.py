class Exc(Exception):
    """
    Base class for all my custom exceptions
    """
    ...


class UniquenessError(Exc):
    
    def __str__(self):
        return f"Unique constraint failed: {
            ", ".join([arg for arg in self.args])}"
