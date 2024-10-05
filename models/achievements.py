from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True, index=True)
    achievement_name = Column(String(50)) 
    achievement_points = Column(Integer)  
    user_id = Column(Integer, ForeignKey("user.id"))  
    user = relationship("User", back_populates="achievements") 

    def __init__(self, achievement_name, achievement_points, user_id):
        self.achievement_name = achievement_name
        self.achievement_points = achievement_points
        self.user_id = user_id
    