from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship, sessionmaker

"<dialect>+<driver>://<username>:<password>@host>:<port>/<database>"

postgre_db_url = "postgresql://admin:admin123@host.docker.internal:5432/mydb"

engine = create_engine(postgre_db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


    
class User(Base):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True)
   
        
    username = Column(String)
    
    following_id = Column(Integer, ForeignKey('users.id'))
    following = relationship('User', remote_side=[id], uselist=True)
       
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}, following={self.following}')>"
    
    

Base.metadata.create_all(engine)
