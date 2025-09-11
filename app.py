from sqlalchemy import Column, Integer, String,  create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, registry
from typing import Optional
from typing_extensions import Annotated
db_url = "postgresql://admin:admin123@host.docker.internal:5432/mydb"

engine = create_engine(db_url, echo=True)

str_20  = Annotated(str, 20)
str_100 = Annotated(str, 100)

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map = {
            str_20: String(20),
            str_100: String(100),
        }
    )
    



class UserLegacy(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str_20]]
    last_name: Mapped[Optional[str_100]] 


