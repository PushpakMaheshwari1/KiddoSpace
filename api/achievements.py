from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.achievements import Achievement  
from schemas.achievements import AchievementCreate, AchievementResponse
from db.session import get_db
from typing import List,Optional
from models.badge import Badge
from schemas.badge import BadgeResponse


router = APIRouter(
    prefix="/achievements",
    tags=['ACHIEVEMENTS']
)

def award_achievement(db: Session, achievement_data: AchievementCreate):
    db_achievement = Achievement(**achievement_data.dict())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement

@router.post("/achievements/", response_model=AchievementResponse)
def create_achievement(achievement_data: AchievementCreate, db: Session = Depends(get_db)):
    return award_achievement(db=db, achievement_data=achievement_data)

@router.get("/achievements/user/{user_id}", response_model=List[AchievementResponse])
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    achievements = db.query(Achievement).filter(Achievement.user_id == user_id).all()
    return achievements


@router.get("/achievements/user/{user_id}/points", response_model=int)
def get_user_total_achievement_points(user_id: int, db: Session = Depends(get_db)):
    total_points = db.query(func.sum(Achievement.achievement_points)).filter(Achievement.user_id == user_id).scalar()
    
    if total_points is None:
        total_points = 0

    return total_points


@router.post("/badges/award/{user_id}", response_model=Optional[BadgeResponse])
def award_badge(user_id: int, db: Session = Depends(get_db)):
    total_points = db.query(func.sum(Achievement.achievement_points)).filter(Achievement.user_id == user_id).scalar()

    if total_points and total_points >= 1000:
        existing_badge = db.query(Badge).filter(Badge.user_id == user_id).first()
        if not existing_badge:
            new_badge = Badge(badge_id=1, user_id=user_id)  
            db.add(new_badge)
            db.commit()
            db.refresh(new_badge)
            return new_badge

    raise HTTPException(status_code=404, detail="Badge not awarded. Not enough achievement points.")

@router.get("/badges/user/{user_id}", response_model=List[BadgeResponse])
def get_user_badges(user_id: int, db: Session = Depends(get_db)):
    badges = db.query(Badge).filter(Badge.user_id == user_id).all()
    return badges