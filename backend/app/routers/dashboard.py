from fastapi import APIRouter,Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import Employee,Attendance,Leave,Payroll
from ..dependencies import require_roles
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/summary")
def summary(db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    return {"total_employees":db.query(Employee).count(),"present_records":db.query(Attendance).filter(Attendance.status=="PRESENT").count(),"pending_leaves":db.query(Leave).filter(Leave.status=="PENDING").count(),"payroll_records":db.query(Payroll).count(),"total_payroll":float(db.query(func.coalesce(func.sum(Payroll.net_salary),0)).scalar() or 0)}
