from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine("postgresql://admin:admin123@localhost:5432/mydb", echo=True)


Base = declarative_base()

Session = sessionmaker(bind=engine)
