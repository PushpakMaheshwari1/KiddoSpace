from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.session import get_db
from models.streak import Streak 
from schemas.streaks import StreakCreate, StreakResponse  

router = APIRouter(
    prefix="/streak",
    tags=['STREAKS']
)
def record_activity(db: Session, user_id: int):
    streak = db.query(Streak).filter(Streak.user_id == user_id).first()

    # Get the current date
    today = datetime.now()

    if streak:
        if streak.last_activity_date and streak.last_activity_date.date() == (today - timedelta(days=1)).date():
            streak.current_streak += 1  
        elif streak.last_activity_date and streak.last_activity_date.date() != today.date():
            streak.current_streak = 1 
        else:
            return

        streak.max_streak = max(streak.max_streak, streak.current_streak)

        streak.last_activity_date = today

    else:
        new_streak = Streak(user_id=user_id, current_streak=1, max_streak=1, last_activity_date=today)
        db.add(new_streak)

    db.commit()

@router.post("/activity/{user_id}", response_model=dict)
def record_user_activity(user_id: int, db: Session = Depends(get_db)):
    record_activity(db, user_id)
    return {"message": "Activity recorded and streak updated."}

@router.get("/streak/{user_id}", response_model=StreakResponse)  # Use StreakResponse here
def get_streak(user_id: int, db: Session = Depends(get_db)):
    streak = db.query(Streak).filter(Streak.user_id == user_id).first()
    if not streak:
        raise HTTPException(status_code=404, detail="Streak not found")
    return streak
