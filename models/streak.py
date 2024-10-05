from sqlalchemy import Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base

class Streak(Base):
    __tablename__ = "streak"

    id = Column(Integer, primary_key=True, index=True)
    current_streak = Column(Integer, default=0)  
    max_streak = Column(Integer, default=0)  
    last_activity_date = Column(DateTime)
    created_date = Column(DateTime, default=func.now()) 
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="streaks")