from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base

class Todo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  
    user_id = Column(Integer, ForeignKey('users.id'))               
    description = Column(String, index=True)
    tags = Column(ARRAY(String))  
    done = Column(Boolean, default=False)
    

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement = True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    invited_todo_ids = Column(ARRAY(Integer), default=[])  
