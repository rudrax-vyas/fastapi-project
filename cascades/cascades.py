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

parent = Parent()
child = Child()
parent.children.append(child)

# Only add the parent to session
session.add(parent)


print('Before committing')
print(parent)
print(child)
session.commit()

print('\nAfter committing')
print(parent)
print(child)

