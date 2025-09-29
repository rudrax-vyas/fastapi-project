from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
from starlette import status
from .auth import get_current_user
from models import LeaveTypes, LeaveRequest, LeaveBalance
from datetime import date, datetime
import pytz

router = APIRouter(
    prefix='/leaves',
    tags=['leaves']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

class LeaveAppy(BaseModel):
    leave_type_id: int
    start_date: date
    end_date: date

# Employyes apply leave
@router.post("/apply", status_code=status.HTTP_201_CREATED)
def apply_leave(leave: LeaveAppy, db: db_dependency, user=Depends(get_current_user)):
    leave_type = db.query(LeaveTypes).filter(LeaveTypes.id == leave.leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Leave type not found')
    
    if leave.start_date < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be in the past")

    
    if leave.end_date < leave.start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="End date cannot be before start date")
    
    overlap = db.query(LeaveRequest).filter(LeaveRequest.employee_id == user.id, LeaveRequest.status != 'rejected', LeaveRequest.start_date <= leave.end_date, LeaveRequest.end_date >= leave.start_date).first()
    if overlap:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Leave request overlaps with an existing leave request')
    
    requested_days = (leave.end_date - leave.start_date).days + 1
    balance = db.query(LeaveBalance).filter(LeaveBalance.employee_id == user.id, LeaveBalance.leave_type_id == leave.leave_type_id).first()
    if balance.remaining_days < requested_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough leave balance')
    
    
    leave_request = LeaveRequest(
        employee_id = user.id,
        leave_type_id = leave.leave_type_id,
        start_date = leave.start_date,
        end_date = leave.end_date,
        status = 'pending'
        
    )
    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)
    return leave_request

class ViewRequest(BaseModel):
    id: int
    leave_type_id: int
    start_date: date
    end_date: date
    status: str
    created_at: str
    
    class Config:
        orm_mode = True

# Employees view leave request  
@router.get("/my", response_model=List[ViewRequest], status_code=status.HTTP_200_OK)
def get_my_leaves(db: db_dependency, user=Depends(get_current_user)):
    leaves = db.query(LeaveRequest).filter(LeaveRequest.employee_id == user.id).all()
    
    
    ist = pytz.timezone("Asia/Kolkata")
    for leave in leaves:
        leave.created_at = leave.created_at.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%Y-%m-%d %H:%M:%S") 
    return leaves


class PendingRequest(BaseModel):
    id: int
    leave_type_id: int
    start_date: date
    end_date: date
    status: str
    created_at: str
    
    class Config:
        orm_mode=True
        
# Manager check pending request     
@router.get("/pending", response_model=List[PendingRequest], status_code=status.HTTP_200_OK)
def get_pending_leaves(db: db_dependency, user=Depends(get_current_user)):
    if user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    pending_leaves = db.query(LeaveRequest).filter(LeaveRequest.status == 'pending').all()
    
    ist = pytz.timezone("Asia/Kolkata")
    for leave in pending_leaves:
        leave.created_at = leave.created_at.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
        
    return pending_leaves
        
class LeaveUpdate(BaseModel):
    status: str

# Manager approve or reject leave   
@router.put("/{id}/approve", status_code=status.HTTP_200_OK)
def approve_leave(id: int, leave_update: LeaveUpdate, db: db_dependency, user=Depends(get_current_user)):
    if user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only manager is authorized')
        
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == id).first()
    if not leave_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Leave request not found')
        
    if leave_request.status != 'pending':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Leave already proceed')
    
    if leave_update.status not in['approved', 'rejected']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid status')
    
    if leave_update.status == 'approved':
        leave_days = (leave_request.end_date - leave_request.start_date).days+1
        balance = db.query(LeaveBalance).filter(LeaveBalance.employee_id == leave_request.employee_id, LeaveBalance.leave_type_id == leave_request.leave_type_id).first()
        if not balance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Leave balance not found')
        if balance.remaining_days < leave_days:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough leave balance')
                
        balance.remaining_days -= leave_days
    
    leave_request.status = leave_update.status
    db.commit()
    db.refresh(leave_request)
      
    
    ist = pytz.timezone("Asia/Kolkata")
    leave_request.created_at = leave_request.created_at.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
    return leave_request


        
        
class LeaveBalanceResponse(BaseModel):
    leave_type: str
    remaining_days: int

    class Config:
        orm_mode = True
        
# Employee checks leave balance
@router.get("/balance", response_model=List[LeaveBalanceResponse], status_code=status.HTTP_200_OK)
def get_leave_balance(db: db_dependency, user=Depends(get_current_user)):
    balances = db.query(LeaveBalance).filter(LeaveBalance.employee_id == user.id).all()
    
    if not balances:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Leave balance not found')
    
    
    response = []
    for b in balances:
        response.append(LeaveBalanceResponse(
            leave_type=b.leave_type.type_name,   
            remaining_days=b.remaining_days
        ))
    
    return response
   
    
