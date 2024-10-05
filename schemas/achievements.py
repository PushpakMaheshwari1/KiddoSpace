from pydantic import BaseModel

class AchievementBase(BaseModel):
    achievement_name: str
    achievement_points: int
    user_id: int

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: int

    class Config:
        orm_mode = True  # Allow reading SQLAlchemy models
