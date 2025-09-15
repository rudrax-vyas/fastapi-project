from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Simple User model
class User(Base):
    __tablename__ = "demo"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

# Database setup
engine = create_engine("postgresql://admin:admin123@localhost:5432/mydb", echo=True)  
Session = sessionmaker(bind=engine, autoflush=True)  # <-- only autoflush enabled
session = Session()

Base.metadata.create_all(engine)

# Add new user
new_user = User(name="Rudrax", age=22)
session.add(new_user)

# No commit yet, but autoflush kicks in before query
print("Users inside session:", session.query(User).all())

# ❌ If you open test.db in another tool, this row will not be there yet
# ✅ Only after session.commit(), it will be visible permanently
