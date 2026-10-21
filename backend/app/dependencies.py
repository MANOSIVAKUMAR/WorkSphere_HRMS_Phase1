from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .models.models import User
from .security import decode_token
bearer=HTTPBearer()
def current_user(c:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db)):
    p=decode_token(c.credentials)
    if not p or not p.get("sub"): raise HTTPException(401,"Invalid or expired token")
    u=db.get(User,int(p["sub"]))
    if not u: raise HTTPException(401,"User not found")
    return u
def require_roles(*roles):
    def check(u=Depends(current_user)):
        if u.role not in roles: raise HTTPException(403,"Insufficient permissions")
        return u
    return check
