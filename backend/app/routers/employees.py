from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import Employee
from ..schemas.schemas import EmployeeIn,EmployeeOut
from ..dependencies import require_roles
router=APIRouter(prefix="/employees",tags=["Employees"])
@router.get("/",response_model=list[EmployeeOut])
def list_employees(search:str="",db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    q=db.query(Employee)
    if search: q=q.filter((Employee.full_name.contains(search))|(Employee.department.contains(search))|(Employee.designation.contains(search)))
    return q.order_by(Employee.id.desc()).all()
@router.post("/",response_model=EmployeeOut)
def create(d:EmployeeIn,db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    if db.query(Employee).filter(Employee.user_id==d.user_id).first(): raise HTTPException(409,"Employee profile exists")
    e=Employee(**d.model_dump()); db.add(e); db.commit(); db.refresh(e); return e
@router.put("/{id}",response_model=EmployeeOut)
def update(id:int,d:EmployeeIn,db:Session=Depends(get_db),u=Depends(require_roles("HR","ADMIN"))):
    e=db.get(Employee,id)
    if not e: raise HTTPException(404,"Employee not found")
    for k,v in d.model_dump().items(): setattr(e,k,v)
    db.commit(); db.refresh(e); return e
