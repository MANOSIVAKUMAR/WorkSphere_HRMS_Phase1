from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..schemas.schemas import RegisterIn,LoginIn,TokenOut
from ..security import hash_password,verify_password,create_token
from ..dependencies import current_user
router=APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/register",response_model=TokenOut)
def register(d:RegisterIn,db:Session=Depends(get_db)):
    if d.role not in {"EMPLOYEE","HR","ADMIN"}: raise HTTPException(400,"Invalid role")
    if db.query(User).filter((User.username==d.username)|(User.email==d.email)).first(): raise HTTPException(409,"Username or email exists")
    u=User(username=d.username,email=d.email,hashed_password=hash_password(d.password),role=d.role); db.add(u); db.commit(); db.refresh(u)
    return {"token":create_token({"sub":str(u.id),"role":u.role}),"role":u.role}
@router.post("/login",response_model=TokenOut)
def login(d:LoginIn,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.username==d.username).first()
    if not u or not verify_password(d.password,u.hashed_password): raise HTTPException(401,"Invalid username or password")
    return {"token":create_token({"sub":str(u.id),"role":u.role}),"role":u.role}
@router.get("/me")
def me(u=Depends(current_user)): return {"id":u.id,"username":u.username,"email":u.email,"role":u.role}
