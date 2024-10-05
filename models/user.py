from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base
from .activity import Activity

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String(100), unique=True, index=True)
    username = Column(String(20), unique=True, index=True)
    password = Column(String(225))
    created_date = Column(DateTime, default=func.now())
    modified_date = Column(DateTime, default=func.now(), onupdate=func.now())
    
    activities = relationship("Activity", back_populates="user")
    projects = relationship("Project", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
    streaks = relationship("Streak", back_populates="user")
    