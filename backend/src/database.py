from sqlalchemy import create_engine
from .security.config import settings
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(settings.database_url, pool_pre_ping=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
