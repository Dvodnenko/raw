from sqlalchemy import create_engine, event, Engine


engine = create_engine(
    url="sqlite:///raw.db", # temporare url for tests
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
