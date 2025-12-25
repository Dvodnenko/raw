from sqlalchemy import create_engine, event, Engine

from ...common import config_, drill


engine = create_engine(
    url="sqlite:///" + drill(config_, ["core", "db_path"], raise_=True),
    echo=drill(config_, ["core", "echo"], default=False)
)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
