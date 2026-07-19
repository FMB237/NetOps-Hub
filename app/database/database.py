# This is the file where we gonna connect our DB file 
# Note our DB is a Portgres Db inside a Docker container

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.config import settings

engine = create_engine(
    settings.database_url,
    echo=True,
)

SessionLocal =sessionmaker(
    autoflush=False,
    bind=engine,
    autocommit=False
)

# Here i will used the Vscode extension to generate the yield db fonction

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
