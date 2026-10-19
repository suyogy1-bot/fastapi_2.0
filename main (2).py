from fastapi import FastAPI
import json
import os
from pydantic import BaseModel , Field

app = FastAPI()

FILE_PATH = 'students.json'

def load_student() -> list:
    if not os.path.exists(FILE_PATH):
        return []                          
    with open(FILE_PATH,"r") as file:
        return json.load(file)
    
def save_students(data:list):
    with open(FILE_PATH,"w") as file:
        json.dump(data,file,indent=4) 
    
    
class StudentCreate(BaseModel):
    id:int 
    name:str = Field(min_length=3, max_length=50, description="Student name")
    course:str   
     
    
@app.get("/test")
def test():
    return {"helloo sever is working"}


@app.get("/students")
def get_students():
    return load_student()

@app.post("/students")
def create_student(student :StudentCreate):
    students = load_student()
    new_student  ={
        'id':student.id,
        'name':student.name,
        'course':student.course
    }
    students.append(new_student)
    save_students(students)
    return {
        "message":"Student created Success",
        "data":new_student
    }






@app.get("/students/{student_id}")
def get_student(student_id:int):
    students = load_student()
    for student in students:
        if student["id"] == student_id:
            return student
    return {"error":"student not found"}



  
