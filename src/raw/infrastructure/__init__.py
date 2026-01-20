from .adapters.repository import TaskRepositorySQL
from .adapters.spec_compiler import SpecCompilerSQL
from .adapters.uow import UnitOfWorkSQL

from .database.tables import create_tables
