from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Badge(Base):
    __tablename__ = "badge"
    
    id = Column(Integer, primary_key=True, index=True)
    badge_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="badges")
