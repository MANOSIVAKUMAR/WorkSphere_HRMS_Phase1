from datetime import datetime, date, time
from sqlalchemy import String, Integer, Float, Date, DateTime, Time, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    username: Mapped[str]=mapped_column(String(100),unique=True,index=True)
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    hashed_password: Mapped[str]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(20),default="EMPLOYEE")
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class Employee(Base):
    __tablename__="employees"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True)
    full_name: Mapped[str]=mapped_column(String(150))
    designation: Mapped[str]=mapped_column(String(100))
    department: Mapped[str]=mapped_column(String(100))
    joining_date: Mapped[date]=mapped_column(Date)
    salary: Mapped[float]=mapped_column(Float,default=0)
    status: Mapped[str]=mapped_column(String(20),default="ACTIVE")

class Attendance(Base):
    __tablename__="attendance"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    employee_id: Mapped[int]=mapped_column(ForeignKey("employees.id"))
    check_in: Mapped[time|None]=mapped_column(Time,nullable=True)
    check_out: Mapped[time|None]=mapped_column(Time,nullable=True)
    date: Mapped[date]=mapped_column(Date,default=date.today)
    status: Mapped[str]=mapped_column(String(20),default="PRESENT")

class Leave(Base):
    __tablename__="leaves"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    employee_id: Mapped[int]=mapped_column(ForeignKey("employees.id"))
    leave_type: Mapped[str]=mapped_column(String(20))
    start_date: Mapped[date]=mapped_column(Date)
    end_date: Mapped[date]=mapped_column(Date)
    reason: Mapped[str]=mapped_column(String(500))
    status: Mapped[str]=mapped_column(String(20),default="PENDING")

class Payroll(Base):
    __tablename__="payroll"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    employee_id: Mapped[int]=mapped_column(ForeignKey("employees.id"))
    basic_salary: Mapped[float]=mapped_column(Float)
    deductions: Mapped[float]=mapped_column(Float,default=0)
    bonus: Mapped[float]=mapped_column(Float,default=0)
    net_salary: Mapped[float]=mapped_column(Float)
    month: Mapped[str]=mapped_column(String(20))
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class Notification(Base):
    __tablename__="notifications"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    title: Mapped[str]=mapped_column(String(150))
    message: Mapped[str]=mapped_column(String(500))
    is_read: Mapped[bool]=mapped_column(Boolean,default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
