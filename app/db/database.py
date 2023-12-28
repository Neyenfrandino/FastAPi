from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Neyen1995@localhost:5432/fastapi-database"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False )
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db   
    finally:   
        db.close()