from database import SessionLocal, Base, engine
from models import Employees, LeaveTypes, ANNUAL_LEAVE_DAYS, SICK_LEAVE_DAYS, CASUAL_LEAVE_DAYS
from utils import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

leave_types = [
    LeaveTypes(type_name="Annual Leave", max_days_per_year=ANNUAL_LEAVE_DAYS),
    LeaveTypes(type_name="Sick Leave", max_days_per_year=SICK_LEAVE_DAYS),
    LeaveTypes(type_name="Casual Leave", max_days_per_year=CASUAL_LEAVE_DAYS),
]

db.add_all(leave_types)
db.commit()

employees = [
    Employees(name="Smithjoshi", email="smith@gmail.com", password=hash_password("smith123"), username="smith", role="employee"),
    Employees(name="Rudraxvyas", email="rudrax@gmail.com", password=hash_password("rudrax123"), username="rudrax", role="employee"),
    Employees(name="Devanshtrivedi", email="devansh@gmail.com", password=hash_password("devansh123"), username="devansh", role="employee"),
    Employees(name="Devjoshi", email="dev@gmail.com", password=hash_password("dev123"), username="dev", role="employee"),
    Employees(name="Admin", email="admin@gmail.com", password=hash_password("admin123"), username="adminmanager", role="manager"),
]

db.add_all(employees)
db.commit()
db.close()