from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from ...config import load_config


conf = load_config()
engine = create_engine(
    conf.get("data_file_path"), 
    echo=conf.get("echo")
)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def transaction(func):

    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            self.session.commit()
            return result
        except Exception:
            self.session.rollback()
            raise

    return wrapper
