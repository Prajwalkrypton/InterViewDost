from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .core_config import get_settings


settings = get_settings()

# For SQLite we need check_same_thread=False; for PostgreSQL it's ignored
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
