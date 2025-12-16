from sqlalchemy import create_engine

from ...common import config_, drill


engine = create_engine(
    url="sqlite:///" + drill(config_, ["core", "db_path"], raise_=True),
    echo=drill(config_, ["core", "echo"], default=False)
)
