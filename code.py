from fastapi import FastAPI

# 1. Initialize the FastAPI app instance
app = FastAPI()

# 2. Local in-memory data (a simple list of dictionaries)
students = [
    {"id": 1, "name": "Aman Sharma", "course": "Computer Science"},
    {"id": 2, "name": "Priya Patel", "course": "Data Science"}
]

# 3. Root endpoint (Health Check)
@app.get("/")
def home():
    return {"message": "Welcome to the Student API!"}

# 4. READ: Get all students
@app.get("/students")
def get_all_students():
	    return students




# 5. READ: Get a single student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return {"error": "Student not found"}

# 6. CREATE: Add a new student to local data
@app.post("/students")
def create_student(new_student: dict):
    students.append(new_student)
    return {
        "message": "Student added successfully",
        "data": new_student
    }