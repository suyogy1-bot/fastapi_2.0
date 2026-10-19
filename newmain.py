from fastapi import FastAPI ,HTTPException ,Path ,Query
import json
import os
from pydantic import BaseModel , Field

app = FastAPI()

FILE_PATH = 'students.json'

def load_students() -> list:
    if not os.path.exists(FILE_PATH):
        return []                          
    with open(FILE_PATH,"r") as file:
        return json.load(file)
    
def save_students(data:list):
    with open(FILE_PATH,"w") as file:
        json.dump(data,file,indent=4) 
        
class StudentCreate(BaseModel):
    name:str = Field(min_length=2,max_length=50)
    course:str=Field(min_length=2,max_length=50)
    
class StudentResponse(BaseModel):
    id:int
    name:str
    course:str
    
class StudentCreatedResponse(BaseModel):
    message:str
    student :StudentResponse
    
        
@app.get("/health")
def test():
    return {"message":"hey my server is working"}


@app.get("/students",response_model=list[StudentResponse])
def get_all_students(
    course: str | None = Query(default=None, description="Filter by course"),
):
   students = load_students()
   if course:
        students = [s for s in students if s["course"].lower() == course.lower()]
   return students


@app.post("/students",
          status_code=201,
          response_model=StudentCreatedResponse)
def create_student(new_student:StudentCreate):
    students = load_students()
    newId =0
    for student in students:
        newId = max(newId , student["id"])
    student = {
        "id":newId+1,
        "name":new_student.name,
        "course":new_student.course
    }
    students.append(student)
    save_students(students)
    return {"message":"student created",
             "student":student}
    
    
    
@app.get("/students/{student_id}")
def get_student_by_id(student_id:int=Path(ge=0)):
    students = load_students()
    for student in students:
        if student["id"] ==student_id:
            return student
    raise HTTPException(status_code=404,detail="Student Not found")




            
    
    

