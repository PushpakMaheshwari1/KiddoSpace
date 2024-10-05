from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import User
from utils.hashing import get_password_hash, verify_password
from utils.tokens import create_access_token

auth_router = APIRouter(
    prefix="/auth",
    tags=['AUTHENTICATION']
)

@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(email: str, username: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email_id == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(password)
    new_user = User(email_id=email, username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

@auth_router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_id == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}