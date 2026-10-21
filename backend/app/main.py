from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base,engine,SessionLocal
from .models.models import User
from .security import hash_password
from .routers import auth,employees,attendance,leaves,payroll,notifications,dashboard
Base.metadata.create_all(bind=engine)
app=FastAPI(title="WorkSphere HRMS API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for r in [auth.router,employees.router,attendance.router,leaves.router,payroll.router,notifications.router,dashboard.router]:app.include_router(r)
def seed():
    db=SessionLocal()
    for u,e,p,r in [("admin","admin@worksphere.local","Admin@123","ADMIN"),("hr","hr@worksphere.local","Hr@123","HR"),("employee","employee@worksphere.local","Employee@123","EMPLOYEE")]:
        if not db.query(User).filter(User.username==u).first():db.add(User(username=u,email=e,hashed_password=hash_password(p),role=r))
    db.commit();db.close()
seed()
@app.get("/")
def root():return {"message":"WorkSphere HRMS API is running"}
@app.get("/health")
def health():return {"status":"ok"}
