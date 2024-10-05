from pydantic import BaseModel

class BadgeBase(BaseModel):
    badge_id: int

class BadgeCreate(BadgeBase):
    user_id: int

class BadgeResponse(BadgeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
