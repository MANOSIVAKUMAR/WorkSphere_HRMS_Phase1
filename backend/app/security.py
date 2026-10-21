import os
from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
SECRET_KEY=os.getenv("SECRET_KEY","worksphere-development-secret")
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_token(data):
    d=data.copy(); d["exp"]=datetime.utcnow()+timedelta(hours=1)
    return jwt.encode(d,SECRET_KEY,algorithm="HS256")
def decode_token(t):
    try: return jwt.decode(t,SECRET_KEY,algorithms=["HS256"])
    except JWTError: return None
