from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import Notification
from ..dependencies import current_user
router=APIRouter(prefix="/notifications",tags=["Notifications"])
@router.get("/")
def all(db:Session=Depends(get_db),u=Depends(current_user)):return db.query(Notification).filter(Notification.user_id==u.id).order_by(Notification.id.desc()).all()
@router.patch("/{id}/read")
def read(id:int,db:Session=Depends(get_db),u=Depends(current_user)):
    x=db.query(Notification).filter(Notification.id==id,Notification.user_id==u.id).first()
    if x:x.is_read=True;db.commit()
    return {"message":"ok"}
