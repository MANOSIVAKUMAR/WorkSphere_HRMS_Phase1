# WorkSphere – HR Management System (HRMS)

Phase 1 – Core HR Management System

Modules: Authentication & Roles, Employees, Attendance, Leaves, Payroll, Dashboard & Analytics, Notifications.

## Backend
FastAPI + SQLAlchemy + SQLite + JWT + Pydantic

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## Frontend
React + Vite + Axios + React Router

```powershell
cd frontend
npm install
npm run dev
```
Frontend: http://localhost:5173

Demo accounts:
- admin / Admin@123
- hr / Hr@123
- employee / Employee@123

Change demo passwords before production use.
