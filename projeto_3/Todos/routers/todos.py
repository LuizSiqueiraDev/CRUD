from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal
from pydantic import BaseModel, Field

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    model = db.query(Todos).filter(Todos.id == todo_id).first()
    if model is not None:
        return model
    raise HTTPException(status_code=404, detail='Todo not found')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    model = Todos(**todo_request.model_dump())
    
    db.add(model)
    db.commit()   


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,  todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    model = db.query(Todos).filter(Todos.id == todo_id).first()
    if model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    model.title = todo_request.title
    model.description = todo_request.description
    model.priority = todo_request.priority
    model.complete = todo_request.complete
    
    db.add(model)
    db.commit()
    

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    
    db.commit()
