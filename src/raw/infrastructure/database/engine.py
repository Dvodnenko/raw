from sqlalchemy import create_engine, event, Engine


engine = create_engine(
    url="sqlite:///raw.db", # temporare url for tests
)
