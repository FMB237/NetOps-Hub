# This is the file where we gonna connect our DB file 
# Note our DB is a Portgres Db inside a Docker container

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
