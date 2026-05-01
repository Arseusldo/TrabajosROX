from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password:str, hashed:str)->bool:
    return pwd_context.verify(password, hashed)

def authenticate(db:Session, email:str, password:str):
    user = db.query(User).filter(User.email==email, User.activo==True).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None
