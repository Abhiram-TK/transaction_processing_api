from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.database.connection import get_db

from app.models.user import User

from app.schemas.auth_schema import (UserRegister, UserLogin, TokenResponse)

from app.services.jwt_service import create_access_token

from app.core.logger import logger


router = APIRouter(tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = (db.query(User).filter(User.username == user.username).first())

    if existing_user:

        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=user.username, password=user.password, role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User registered: {new_user.username}")

    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    db_user = (db.query(User).filter(User.username == user.username).first())

    if not db_user:

        raise HTTPException(status_code=401, detail="Invalid credentials")

    if db_user.password != user.password:

        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.username, "role": db_user.role})
    
    logger.info(f"User logged in: {db_user.username}")

    return {"access_token": access_token, "token_type": "bearer"}