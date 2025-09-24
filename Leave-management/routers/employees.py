from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Employees
from .auth import manager_only, get_db
from sqlalchemy.orm import Session
from utils import hash_password
from starlette import status


router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def list_employees(db: Session = Depends(get_db), current_user: Employees = Depends(manager_only)):
    return db.query(Employees).all()

class EmployeeCreate(BaseModel):
    name: str
    username: str
    password: str
    role: str
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: Employees = Depends(manager_only)):
    
    new_emp = Employees(
        name = employee.name,
        username = employee.username,
        role = employee.role,
        password = hash_password(employee.password)
             
    )
    
    return new_emp
    
    

    