from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = "postgresql+psycopg2://postgres:postgres@localhost/Event_Coordination_Engine"

engine = create_engine(URL)

Base = declarative_base()

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)