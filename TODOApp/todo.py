from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from models import Todo
from database import SessionLocal
from pydantic import BaseModel, Field



router =APIRouter()




# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for request
class TodoCreate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=200)
    completed: bool 


db_dependency = Annotated[Session, Depends(get_db)]





@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    return db.query(Todo).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, todo_create: TodoCreate):
    todo_model = Todo(**todo_create.model_dump())
    db.add(todo_model)
    db.commit()
    
@router.put("/todo{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, todo_id: int, todo_create: TodoCreate):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
   
    todo_model.title = todo_create.title
    todo_model.description = todo_create.description
    todo_model.completed = todo_create.completed
    
    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.query(Todo).filter(Todo.id == todo_id).delete()
    
    db.commit()
