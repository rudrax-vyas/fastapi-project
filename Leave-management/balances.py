from models import LeaveBalance, Employees, ANNUAL_LEAVE_DAYS, SICK_LEAVE_DAYS, CASUAL_LEAVE_DAYS
from database import SessionLocal




db = SessionLocal()
all_employees = db.query(Employees).all()

for emp in all_employees:
    balances = [
        LeaveBalance(employee_id=emp.id, leave_type_id=1, remaining_days=ANNUAL_LEAVE_DAYS),
        LeaveBalance(employee_id=emp.id, leave_type_id=2, remaining_days=SICK_LEAVE_DAYS),
        LeaveBalance(employee_id=emp.id, leave_type_id=3, remaining_days=CASUAL_LEAVE_DAYS),
    ]
    db.add_all(balances)

db.commit()
db.close()
