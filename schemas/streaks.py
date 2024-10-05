from pydantic import BaseModel
from datetime import datetime

class StreakBase(BaseModel):
    current_streak: int
    max_streak: int
    last_activity_date: datetime
    user_id: int

class StreakCreate(StreakBase):
    pass

class StreakResponse(StreakBase):
    id: int

    class Config:
        orm_mode = True  # This tells Pydantic to read data even if it's in SQLAlchemy's format
