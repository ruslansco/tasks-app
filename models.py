#import DB
from sqlalchemy import Boolean, Column, Integer, String

#import Base class from database.py
from database import Base

#Create a todo class that inherits from Base class.
class Todo(Base):
    #Create table name
    __tablename__ = "todos"
    #Create fields
    id = Column(Integer, primary_key=True, index=False)
    #UUID = Column(Integer, index=True)
    title = Column(String)
    datetime = Column(String)
    complete = Column(Boolean, default=False)
