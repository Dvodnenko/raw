from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...config import load_config


conf = load_config()
engine = create_engine(
    conf.get("data_file_path"), 
    echo=conf.get("echo")
)
Session = sessionmaker(bind=engine)
