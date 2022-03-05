import imp
from re import I
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Set up path to SQLlite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo-app.db"

#Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
)

#Create session instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Declare the Base class from which the model will inherit in next step.
Base = declarative_base()