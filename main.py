from fastapi import FastAPI
import json
import os
from pydantic import BaseModel

app = FastAPI()

class StudentCreate


@app.get("/test")
def test():
    print("This is get test endpoint")

@app.post("/students")
def create_student(new_student: dict):
    students = load_student()

@app.get("/test")
def test():
    return {"hello server is working"}


@app.get("/students")
def get_students():
    return load_student()




@app.get("/students/{student_id}")
def get_student(student_id:int):
    students = load_student()
    for student in students:
        if student["id"] == student_id:
            return student 
    return {"error": "student not found"}
