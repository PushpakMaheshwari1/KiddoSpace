from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base

class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    activity_completed = Column(String(50))
    module_completed = Column(String(50))
    created_date = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="activities")  
