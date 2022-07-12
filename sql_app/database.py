from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# just need to declare db name like below, and run the app, it will auto create db for you
# because in main.py, there's a line to run migrate db
# search for this line in main.py: models.Base.metadata.create_all(bind=engine)

# sqlite db
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# postgres db
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
