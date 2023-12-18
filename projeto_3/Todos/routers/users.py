from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Users
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user, authenticate_user, bcrypt_context
from starlette import status

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail='Authentication')
    
    model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if model is not None:
        return model
    raise HTTPException(status_code=404, detail='User not found.')


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def password_update(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=404, detail='Authentication')
    
    model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(model)
    db.commit()