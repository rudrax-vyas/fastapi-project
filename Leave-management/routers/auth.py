from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from models import Employees
from utils import verify_password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

SECRET_KEY = "f7baa6218d4693ead9a7947f407b4f61dd800fa825c960c780ac7f75b36793d4392aeedba25062582b42ba1f230e9397a7adb6fbc2071b70c3fb878a53bd52bc"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

    
class Token(BaseModel):
    access_token: str
    token_type: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

def create_access_token(username: str, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(db: db_dependency, token: str=Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        role: str = payload.get('role')
        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    user = db.query(Employees).filter(Employees.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    return user



def manager_only(current_user: Employees=Depends(get_current_user)):
    if current_user.role != 'manager':
        raise HTTPException(status_code=401, detail='Only Manager is authorized')
    return current_user


@router.post("/login", response_model=Token)
def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Employees).filter(Employees.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(user.username, user.role, timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}




