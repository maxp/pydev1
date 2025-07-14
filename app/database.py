from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import conf

engine = create_engine(conf.database_url, echo=conf.database_debug)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(base):
    base.metadata.create_all(engine)
