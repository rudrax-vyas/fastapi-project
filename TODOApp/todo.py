from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from models import Todos
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user 



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
    complete: bool 


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]




@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo_create: TodoCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_create.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    
@router.put("/todo{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, db: db_dependency, todo_id: int, todo_create: TodoCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
   
    todo_model.title = todo_create.title
    todo_model.description = todo_create.description
    todo_model.complete = todo_create.complete
    
    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    
    db.commit()