from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from models import Employee, Attendance
from database import db
from datetime import datetime ,date


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://hrms-frontend-pi-peach.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/employees")
async def add_employee(emp: Employee):
    if await db.employees.find_one({"employee_id": emp.employee_id}):
        raise HTTPException(status_code=400, detail="Duplicate employee ID")
    await db.employees.insert_one(emp.dict())
    return {"message": "Employee added"}

@app.get("/employees")
async def list_employees():
    employees = await db.employees.find({}, {"_id": 0}).to_list(100)
    return employees

@app.delete("/employees/{emp_id}")
async def delete_employee(emp_id: str):
    result = await db.employees.delete_one({"employee_id": emp_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@app.post("/attendance")
async def mark_attendance(att: Attendance):
    data = att.dict()

    # Convert date -> datetime (Mongo compatible)
    data["date"] = datetime.combine(att.date, datetime.min.time())

    await db.attendance.insert_one(data)
    return {"message": "Attendance marked"}

@app.get("/attendance")
async def get_attendance():
    records = await db.attendance.aggregate([
        {
            "$lookup": {
                "from": "employees",          # collection name
                "localField": "employee_id",
                "foreignField": "employee_id",
                "as": "employee"
            }
        },
        {
            "$unwind": {
                "path": "$employee",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "employee_id": 1,
                "employee_name": "$employee.full_name",
                "department": "$employee.department",
                "date": 1,
                "status": 1
            }
        }
    ]).to_list(1000)

    # datetime → string
    for r in records:
        if isinstance(r["date"], datetime):
            r["date"] = r["date"].date().isoformat()
        elif isinstance(r["date"], date):
            r["date"] = r["date"].isoformat()

    return records

@app.get("/dashboard")
async def dashboard_summary():
    today = datetime.combine(date.today(), datetime.min.time())

    total_employees = await db.employees.count_documents({})

    total_attendance = await db.attendance.count_documents({})

    present_today = await db.attendance.count_documents({
        "date": today,
        "status": "Present"
    })

    absent_today = await db.attendance.count_documents({
        "date": today,
        "status": "Absent"
    })

    return {
        "total_employees": total_employees,
        "total_attendance": total_attendance,
        "present_today": present_today,
        "absent_today": absent_today
    }