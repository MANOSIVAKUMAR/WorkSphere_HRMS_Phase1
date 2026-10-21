from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import Payroll,Notification,Employee
from ..schemas.schemas import PayrollIn
from ..dependencies import current_user,require_roles
router=APIRouter(prefix="/payroll",tags=["Payroll"])
@router.get("/")
def all(db:Session=Depends(get_db),u=Depends(current_user)):return db.query(Payroll).order_by(Payroll.id.desc()).all()
@router.post("/")
def create(d:PayrollIn,db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    if d.deductions<0 or d.bonus<0:raise HTTPException(400,"Amounts cannot be negative")
    x=Payroll(**d.model_dump(),net_salary=d.basic_salary-d.deductions+d.bonus);db.add(x)
    emp=db.get(Employee,d.employee_id)
    if emp:db.add(Notification(user_id=emp.user_id,title="Payroll Updated",message=f"Payroll for {d.month} was generated."))
    db.commit();db.refresh(x);return x
