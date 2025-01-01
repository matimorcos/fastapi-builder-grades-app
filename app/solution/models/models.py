# pydantic models para validacion de datos
from pydantic import BaseModel
from typing import List

# models, bases, requests, creates y responses

class StudentBase(BaseModel):
    student_names: str
    student_username: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    student_id: int

    class Config:
        orm_mode = True

class SubjectCreate(BaseModel):
    subject_id: str
    subject: str
    subject_description: str
    period_id: str
    year: int
    teaching: str
    teachers_email: str

    class Config:
        orm_mode = True

class SubjectResponse(BaseModel):
    subject_id: str
    subject: str
    subject_description: str
    period_id: str
    year: int
    teaching: str
    teachers_email: str

    class Config:
        orm_mode = True
        
class Achievement(BaseModel):
    achievement_id: str
    description: str
    score: int

class Guideline(BaseModel):
    guideline_id: str
    achievements: List[Achievement]


class PracticalWorkCreate(BaseModel):
    pw_id: str
    guideline_1_id: str
    achievement_1_g1_id: str
    achievement_1_g1_description: str
    achievement_1_g1_score: int
    achievement_2_g1_id: str
    achievement_2_g1_description: str
    achievement_2_g1_score: int
    achievement_3_g1_id: str
    achievement_3_g1_description: str
    achievement_3_g1_score: int
    guideline_2_id: str
    achievement_1_g2_id: str
    achievement_1_g2_description: str
    achievement_1_g2_score: int
    achievement_2_g2_id: str
    achievement_2_g2_description: str
    achievement_2_g2_score: int
    achievement_3_g2_id: str
    achievement_3_g2_description: str
    achievement_3_g2_score: int
    guideline_3_id: str
    achievement_1_g3_id: str
    achievement_1_g3_description: str
    achievement_1_g3_score: int
    achievement_2_g3_id: str
    achievement_2_g3_description: str
    achievement_2_g3_score: int
    achievement_3_g3_id: str
    achievement_3_g3_description: str
    achievement_3_g3_score: int
    subject_id: str

    class Config:
        orm_mode = True

class PracticalWorkResponse(BaseModel):
    pw_id: str
    guideline_1_id: str
    achievement_1_g1_id: str
    achievement_1_g1_description: str
    achievement_1_g1_score: int
    achievement_2_g1_id: str
    achievement_2_g1_description: str
    achievement_2_g1_score: int
    achievement_3_g1_id: str
    achievement_3_g1_description: str
    achievement_3_g1_score: int
    guideline_2_id: str
    achievement_1_g2_id: str
    achievement_1_g2_description: str
    achievement_1_g2_score: int
    achievement_2_g2_id: str
    achievement_2_g2_description: str
    achievement_2_g2_score: int
    achievement_3_g2_id: str
    achievement_3_g2_description: str
    achievement_3_g2_score: int
    guideline_3_id: str
    achievement_1_g3_id: str
    achievement_1_g3_description: str
    achievement_1_g3_score: int
    achievement_2_g3_id: str
    achievement_2_g3_description: str
    achievement_2_g3_score: int
    achievement_3_g3_id: str
    achievement_3_g3_description: str
    achievement_3_g3_score: int
    subject_id: str

    class Config:
        orm_mode = True

class QualificationBase(BaseModel):
    qualification_id: int
    student_id: str
    pw_id: str
    achievements_description: str 
    score: int
    
    class Config:
        orm_mode = True

class QualificationCreate(QualificationBase):
    pass

class QualificationUpdate(QualificationBase):
    pass

class QualificationResponse(QualificationBase):
    qualification_id: int
        
class CalificarRequest(BaseModel):
    student_id: int
    pw_id: str
    guidelines: List[Guideline]  # lista de guidelines con sus achievements

    class Config:
        orm_mode = True