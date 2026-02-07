from pydantic import BaseModel, EmailStr
from datetime import date

class Employee(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str

class Attendance(BaseModel):
    employee_id: str
    date: date
    status: str