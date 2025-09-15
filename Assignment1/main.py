from database import Base, engine, Session
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

Base.metadata.create_all(engine)

session = Session()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    company = relationship("Company", back_populates="user", uselist=False)
    

class Company(Base):
    __tablename__ = "company"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="company", uselist=False)

user = [User(name="Rudrax", age=22), User(name="Virat", age=38), User(name="Max", age=29)]
# session.add_all(user)
# session.commit()

#Update Record

rudrax = session.query(User).filter(User.id == 4).first()
rudrax.age = 24
print(rudrax)
# session.commit()

rudrax = session.query(User).filter(User.id == 1).delete()
# session.commit()

rudrax = session.query(User).filter(User.id > 4).delete()
# session.commit()

# users = session.query(User).all()

#fetching users 
rudrax = session.query(User).filter_by(name = "Rudrax").first()
virat = session.query(User).filter_by(name = "Virat").first()
max_ = session.query(User).filter_by(name = "Max").first()

#assigning company through relationship
rudrax.company = Company(name="OpenAI")
virat.company = Company(name="Grok")
max_.company = Company(name="Claude")

# session.commit()
records = session.query(User).all()

for record in records:
    print(f"User id: {record.id}, User name: {record.name}, User age: {record.age}, ->, Comapny name: {record.company.name}")

# for user in users:
#     print(f"User id:{user.id}, name: {user.name}, age: {user.age}")



