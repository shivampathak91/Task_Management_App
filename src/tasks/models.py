from sqlalchemy import Column,Integer,String,Boolean
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100))
    description = Column(String(200))
    is_completed = Column(Boolean,default=False)