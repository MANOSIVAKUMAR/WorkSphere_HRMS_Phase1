from datetime import datetime,date
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import Attendance
from ..schemas.schemas import AttendanceIn
from ..dependencies import current_user,require_roles
router=APIRouter(prefix="/attendance",tags=["Attendance"])
@router.get("/")
def history(employee_id:int|None=None,db:Session=Depends(get_db),u=Depends(current_user)):
    q=db.query(Attendance)
    if employee_id:q=q.filter(Attendance.employee_id==employee_id)
    return q.order_by(Attendance.date.desc()).all()
@router.post("/")
def mark(d:AttendanceIn,db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    x=Attendance(**d.model_dump()); db.add(x); db.commit(); db.refresh(x); return x
@router.post("/check-in/{employee_id}")
def checkin(employee_id:int,db:Session=Depends(get_db),u=Depends(current_user)):
    x=db.query(Attendance).filter(Attendance.employee_id==employee_id,Attendance.date==date.today()).first()
    if x and x.check_in: raise HTTPException(400,"Already checked in today")
    if not x:x=Attendance(employee_id=employee_id,date=date.today(),status="PRESENT");db.add(x)
    x.check_in=datetime.now().time();db.commit();db.refresh(x);return x
@router.post("/check-out/{employee_id}")
def checkout(employee_id:int,db:Session=Depends(get_db),u=Depends(current_user)):
    x=db.query(Attendance).filter(Attendance.employee_id==employee_id,Attendance.date==date.today()).first()
    if not x or not x.check_in:raise HTTPException(400,"Check in first")
    x.check_out=datetime.now().time();db.commit();db.refresh(x);return x
