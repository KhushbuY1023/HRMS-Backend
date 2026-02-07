HRMS Lite – Backend

Backend service for HRMS Lite, built with FastAPI and MongoDB.
Provides APIs to manage employees, attendance, and dashboard data.

Tech Stack

FastAPI (Python)

MongoDB

Motor (Async MongoDB driver)

Pydantic

Uvicorn

Features

Add, list, delete employees

Mark and view attendance

Dashboard summary API

Input validation and error handling

CORS enabled for frontend

API Endpoints
Employees

POST /employees – Add employee

GET /employees – Get all employees

DELETE /employees/{employee_id} – Delete employee

Attendance

POST /attendance – Mark attendance

GET /attendance – Get all attendance records

Dashboard

GET /dashboard – Dashboard summary

Environment Variables

Create a .env file:

MONGO_URI=your_mongodb_connection_string

Run Locally
git clone https://github.com/KhushbuY1023/HRMS-Backend.git
cd HRMS-Backend
pip install -r requirements.txt
uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000


API Docs:

http://127.0.0.1:8000/docs
