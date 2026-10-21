from datetime import date,time,datetime
from pydantic import BaseModel,EmailStr,Field,ConfigDict
class RegisterIn(BaseModel):
    username:str=Field(min_length=3); email:EmailStr; password:str=Field(min_length=6); role:str="EMPLOYEE"
class LoginIn(BaseModel): username:str; password:str
class TokenOut(BaseModel): token:str; role:str
class EmployeeIn(BaseModel):
    user_id:int; full_name:str; designation:str; department:str; joining_date:date; salary:float=Field(ge=0); status:str="ACTIVE"
class EmployeeOut(EmployeeIn):
    id:int; model_config=ConfigDict(from_attributes=True)
class AttendanceIn(BaseModel):
    employee_id:int; check_in:time|None=None; check_out:time|None=None; date:date; status:str="PRESENT"
class LeaveIn(BaseModel):
    employee_id:int; leave_type:str; start_date:date; end_date:date; reason:str
class PayrollIn(BaseModel):
    employee_id:int; basic_salary:float; deductions:float=0; bonus:float=0; month:str
