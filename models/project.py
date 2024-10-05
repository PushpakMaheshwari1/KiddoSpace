from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_description = Column(String(1000))  
    created_date = Column(DateTime, default=func.now())  
    modified_date = Column(DateTime, default=func.now(), onupdate=func.now())  
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="projects")