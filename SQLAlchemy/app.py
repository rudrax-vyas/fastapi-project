from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, sessionmaker, Mapped
from typing import Optional
db_url = "postgresql://admin:admin123@host.docker.internal:5432/mydb"

engine = create_engine(db_url)
session = sessionmaker(bind=engine)()

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    
class Address(Base):
    __tablename__ = 'addresses'
    
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    data: Mapped[str]
    
    def __repr__(self)->str:
        return f"<Address:{self.data}"
    
class User(Base):
    __tablename__ = 'users'
    
    first_name: Mapped[str]
    last_name: Mapped[str]
    address: Mapped[Address] = relationship()
    
    def __repr__(self)->str:
        return f"<User: {self.first_name} {self.last_name}>"


Base.metadata.create_all(engine)


# # this address is used
# address_1 = Address(data="1234 Random Address")

# # this address are not used

# address_2 = Address(data="Non existant address")
# address_3 = Address(data="Extra Address")

# # user with an address

# user_1 = User(first_name="Rudrax", last_name="Vyas", address=address_1,)

# # user without an address

# user_2 = User(first_name="Banana", last_name="Man", address=None)

# session.add_all([address_1, address_2, address_3, user_1, user_2])
# session.commit()


# inner join

# result = (
#     session.query(User, Address)
#     .join(Address, full=True).
#     filter(User.address == None, Address.user_id == None)
#     .all()
# )
# print('\nInner Join Inverse')
# print(result)

# result = session.query(User).outerjoin(Address).all()
# print('\nLeft Outer Join')
# print(result)

# result = session.query(Address, User).outerjoin(User).filter(Address.user_id==None).all()
# print('\nRight Outer Join')
# print(result)

left_join = session.query(User, Address).outerjoin(Address)
right_join = session.query(User, Address).outerjoin(User)
full_outer_join = left_join.union(right_join)
print('\nFull Outer Join')
print(full_outer_join.all())

