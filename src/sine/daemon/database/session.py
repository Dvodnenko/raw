from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

from ...common import load_config, drill
from .orm_registry import mapping_registry
from .mappings import map_tables


conf = load_config()
url = drill(conf, ["core", "db_path"], raise_=True)
engine = create_engine(
    url=f"sqlite:///{url}",
    echo=conf.get("echo"),
)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def init_db():
    mapping_registry.metadata.create_all(bind=engine)
    map_tables()

    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = ON;"))
