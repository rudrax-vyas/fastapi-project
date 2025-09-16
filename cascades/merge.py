from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import create_engine, ForeignKey

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    
class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(back_populates='parent', cascade="save-update, merge")
    
    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'
    
class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'))
    parent: Mapped['Parent'] = relationship(back_populates='children')
    
    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'
    
engine = create_engine('postgresql://admin:admin123@localhost:5432/mydb')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()
print(f"Original committed parent: {parent}")
session.close()

# Since the session was closed, the parent is now detached
# Add a new child while detached
parent.children.append(Child())

# Merge back into a new session
session = SessionLocal()
merged = session.merge(parent) #merges the updated object
print(f"Merged parent is session: {merged}")
session.commit()


# Query to confire children were merged
fetched = session.query(Parent).first()
print(f"Fetched from DB: {fetched}")
session.close()


