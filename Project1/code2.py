from fastapi import FastAPI, HTTPException, Path
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, Field, EmailStr
import dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50),unique=True)
    course: Mapped[str] = mapped_column(String(100))


app = FastAPI()

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    course: str = Field(min_length=2, max_length=50)

class StudentResponse(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    course: str = Field(min_length=2, max_length=50)

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = Field(default=None)
    course: str | None = Field(default=None, min_length=2, max_length=50)

@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student_data: StudentCreate):
    db = SessionLocal()
    try:
        query = select(Student).where(Student.email == student_data.email)
        result = db.execute(query)
        existing_student = result.scalar_one_or_none()
        if existing_student:
            raise HTTPException(status_code = 409, detail = "Email already exist")
        
        new_student = Student(
            name = student_data.name,
            email = student_data.email,
            course = student_data.course
            )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student

    finally:
        db.close()


@app.get("/students", response_model = list[StudentResponse])
def get_all_students():
    db = SessionLocal()
    try:
        query = select(Student)
        result = db.execute(query)
        students = result.scalars().all()
        return students
    finally:
        db.close()


@app.get("/students/{student_id}")
def get_student_by_id(student_id: int = Path(ge=0)):
    db = SessionLocal()
    try:
        query = select(Student).where(Student.id == student_id)
        result = db.execute(query)
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    finally:
        db.close()

@app.get("/students", response_model = list[StudentResponse])
def get_all_students():
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=10)
    db = SessionLocal()
    try:
        query = select(Student).offset(skip).limit(limit)
        result = db.execute(query)
        students = result.scalars().all()
        return students
    finally:
        db.close()

@app.put("/students/{student_id}")
def replace_student(student_id: int, student_data: StudentCreate):
    db = SessionLocal()
    try:
        query = select(Student).where(Student.id == student_id)
        student = db.execute(query).scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        if student_data.email != student.email:
            query2 = select(Student).where(Student.email == student_data.email)
            existing_student = db.execute(query2).scalar_one_or_none()
            if not existing_student:
                raise HTTPException(status_code=409, detail="Student with this email already exist.")

        student.name = student_data.name
        student.email = student_data.email
        student.course = student_data.course
        db.commit()
        db.refresh(student)
        return student
    finally:
        db.close()

@app.patch("/students/{student_id}")
def update_student(student_id: int, student_data: StudentUpdate):
    db = SessionLocal()
    try:
        query = select(Student).where(Student.id == student_id)
        student = db.execute(query).scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        if student_data.email is not None and student_data.email != student.email:
            query2 = select(Student).where(Student.email)
            existing_student = db.execute(query2).scalar_one_or_none()
            if not existing_student:
                raise HTTPException(status_code=409, detail="Student with this email already exist.")
            if student_data.name is not None:
                student.name = student_data.name
            if student_data.email is not None:
                student.email = student_data.email
            if student_data.course is not None:
                student.course = student_data.course

            db.commit()
            db.refresh(student)
            return student
    finally:
        db.close()

@app.delete("/student/{student_id}")
def delete_student_by_id(student_id: int):
    db = SessionLocal()
    try:
        query = select(Student).where(Student.id == student_id)
        student = db.execute(query).scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete(student)
        db.commit()
        return {"message": "Student deleted successfully"}
    finally:
        db.close()
        