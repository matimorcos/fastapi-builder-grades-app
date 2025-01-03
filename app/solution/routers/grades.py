from fastapi import  APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from typing import List
from solution.models.models import StudentCreate, StudentResponse, SubjectCreate, SubjectResponse, PracticalWorkCreate, PracticalWorkResponse, QualificationRequest, QualificationBase, QualificationCreate, QualificationResponse  # Importa las clases del modelo
from core.schemas import Student, Subject, PracticalWork, Qualification
from config.config import get_db, DATABASE_URL 
from decouple import config
import sys 
import os

DIR_PATH = config("DIR_PATH")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'solution')))
sys.path.append(DIR_PATH)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/students/", response_model=StudentResponse)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/student/", response_model=StudentResponse)
async def create_student(student_names: str = Form(...), student_username: str = Form(...)):
    student = StudentCreate(student_names=student_names, student_username=student_username)
    return student

@router.post("/students/batch/", response_model=List[StudentResponse])
def create_students_endpoint(students: List[StudentCreate], db: Session = Depends(get_db)):
    try:
        db_students = []
        for student in students:
            db_student = Student(**student.dict())
            db.add(db_student)
            db.commit()
            db.refresh(db_student)
            db_students.append(db_student)
        return db_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")    

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/subjects/", response_model=SubjectResponse)
def create_subject_endpoint(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/subjects/", response_model=List[SubjectResponse])
def get_subjects_endpoint(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.post("/practicalworks/", response_model=PracticalWorkResponse)
def create_practical_work_endpoint(practical_work: PracticalWorkCreate, db: Session = Depends(get_db)):
    try:
        db_practical_work = PracticalWork(**practical_work.dict())
        db.add(db_practical_work)
        db.commit()
        db.refresh(db_practical_work)
        return db_practical_work
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/practicalworks/", response_model=List[PracticalWorkResponse])
def get_practical_works_endpoint(db: Session = Depends(get_db)):
    return db.query(PracticalWork).all()

@router.get("/practicalwork/{pw_id}/guidelines/")
def get_guidelines_and_achievements_endpoint(pw_id: str, db: Session = Depends(get_db)):
    practical_work = db.query(PracticalWork).filter(PracticalWork.pw_id == pw_id).first()
    if not practical_work:
        raise HTTPException(status_code=404, detail="Practical work not found")

    guidelines = {
        "guideline_1": {
            "guideline_id": practical_work.guideline_1_id,
            "achievements": [
                {
                    "achievement_id": practical_work.achievement_1_g1_id,
                    "description": practical_work.achievement_1_g1_description,
                    "score": practical_work.achievement_1_g1_score,
                },
                {
                    "achievement_id": practical_work.achievement_2_g1_id,
                    "description": practical_work.achievement_2_g1_description,
                    "score": practical_work.achievement_2_g1_score,
                },
                {
                    "achievement_id": practical_work.achievement_3_g1_id,
                    "description": practical_work.achievement_3_g1_description,
                    "score": practical_work.achievement_3_g1_score,
                }
            ]
        },
        "guideline_2": {
            "guideline_id": practical_work.guideline_2_id,
            "achievements": [
                {
                    "achievement_id": practical_work.achievement_1_g2_id,
                    "description": practical_work.achievement_1_g2_description,
                    "score": practical_work.achievement_1_g2_score,
                },
                {
                    "achievement_id": practical_work.achievement_2_g2_id,
                    "description": practical_work.achievement_2_g2_description,
                    "score": practical_work.achievement_2_g2_score,
                },
                {
                    "achievement_id": practical_work.achievement_3_g2_id,
                    "description": practical_work.achievement_3_g2_description,
                    "score": practical_work.achievement_3_g2_score,
                }
            ]
        },
        "guideline_3": {
            "guideline_id": practical_work.guideline_3_id,
            "achievements": [
                {
                    "achievement_id": practical_work.achievement_1_g3_id,
                    "description": practical_work.achievement_1_g3_description,
                    "score": practical_work.achievement_1_g3_score,
                },
                {
                    "achievement_id": practical_work.achievement_2_g3_id,
                    "description": practical_work.achievement_2_g3_description,
                    "score": practical_work.achievement_2_g3_score,
                },
                {
                    "achievement_id": practical_work.achievement_3_g3_id,
                    "description": practical_work.achievement_3_g3_description,
                    "score": practical_work.achievement_3_g3_score,
                }
            ]
        }
    }

    return {"pw_id": pw_id, "guidelines": guidelines}

@router.post("/qualify/", response_model=QualificationResponse)
def qualify_student_endpoint(
    request: QualificationRequest,
    db: Session = Depends(get_db)
):
    student_id = request.student_id
    pw_id = request.pw_id
    guidelines = request.guidelines
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    practical_work = db.query(PracticalWork).filter(PracticalWork.pw_id == pw_id).first()
    if not practical_work:
        raise HTTPException(status_code=404, detail="Practical work not found")
    
    scores = {
        practical_work.achievement_1_g1_id: practical_work.achievement_1_g1_score,
        practical_work.achievement_2_g1_id: practical_work.achievement_2_g1_score,
        practical_work.achievement_3_g1_id: practical_work.achievement_3_g1_score,
        practical_work.achievement_1_g2_id: practical_work.achievement_1_g2_score,
        practical_work.achievement_2_g2_id: practical_work.achievement_2_g2_score,
        practical_work.achievement_3_g2_id: practical_work.achievement_3_g2_score,
        practical_work.achievement_1_g3_id: practical_work.achievement_1_g3_score,
        practical_work.achievement_2_g3_id: practical_work.achievement_2_g3_score,
        practical_work.achievement_3_g3_id: practical_work.achievement_3_g3_score,
    }

    final_score = 0
    achievements_description = []

    for guideline in guidelines:
        for achievement in guideline.achievements:
            if achievement.achievement_id not in scores:
                raise HTTPException(status_code=400, detail=f"Achievement ID {achievement.achievement_id} not valid")
            
            final_score += scores[achievement.achievement_id]
            achievements_description.append(achievement.description)

    new_qualification = Qualification(
        student_id=student_id,
        pw_id=pw_id,
        score=final_score,
        achievements_description=" | ".join(achievements_description)
    )

    db.add(new_qualification)
    db.commit()
    db.refresh(new_qualification)

    return QualificationResponse(
        student_id=new_qualification.student_id,
        pw_id=new_qualification.pw_id,
        score=new_qualification.score,
        achievements_description=new_qualification.achievements_description
    )