from database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


ANNUAL_LEAVE_DAYS = 30
SICK_LEAVE_DAYS = 10
CASUAL_LEAVE_DAYS = 7

class Employees(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    
    leave_requests = relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    leave_balances = relationship("LeaveBalance", back_populates="employee", cascade="all, delete-orphan")

    
class LeaveTypes(Base):
    __tablename__ = 'leave_types'
    
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True)
    max_days_per_year = Column(Integer)
    
    leave_requests = relationship("LeaveRequest", back_populates="leave_type")
    leave_balances = relationship("LeaveBalance", back_populates="leave_type")
    
class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    leave_type_id = Column(Integer, ForeignKey('leave_types.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship('Employees', back_populates='leave_requests')
    leave_type = relationship('LeaveTypes', back_populates='leave_requests')
    
class LeaveBalance(Base):
    __tablename__ = 'leave_balances'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    leave_type_id = Column(Integer, ForeignKey('leave_types.id'))
    remaining_days = Column(Integer)
    
    employee = relationship('Employees', back_populates='leave_balances')
    leave_type = relationship('LeaveTypes', back_populates='leave_balances')
    