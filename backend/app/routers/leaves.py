from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import Leave,Notification,Employee
from ..schemas.schemas import LeaveIn
from ..dependencies import current_user,require_roles
router=APIRouter(prefix="/leaves",tags=["Leaves"])
@router.get("/")
def all(db:Session=Depends(get_db),u=Depends(current_user)):return db.query(Leave).order_by(Leave.id.desc()).all()
@router.post("/")
def apply(d:LeaveIn,db:Session=Depends(get_db),u=Depends(current_user)):
    if d.end_date<d.start_date:raise HTTPException(400,"Invalid date range")
    x=Leave(**d.model_dump());db.add(x);db.commit();db.refresh(x);return x
@router.patch("/{id}/status")
def status(id:int,status:str,db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    if status not in {"APPROVED","REJECTED"}:raise HTTPException(400,"Invalid status")
    x=db.get(Leave,id)
    if not x:raise HTTPException(404,"Leave not found")
    x.status=status;emp=db.get(Employee,x.employee_id)
    if emp:db.add(Notification(user_id=emp.user_id,title=f"Leave {status.title()}",message=f"Your leave request was {status.lower()}."))
    db.commit();db.refresh(x);return x
