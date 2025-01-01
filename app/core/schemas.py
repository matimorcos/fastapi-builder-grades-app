#CREACION DE TABLAS EN LA BASE DE DATOS CON SQLALCHEMY PARA INTERACCION CON LA BASE DE DATOS
from sqlalchemy import create_engine, Column, Integer, Table, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from decouple import config

# conexion a la base de datos MariaDB usando decouple, pymysql y mypy que es para evitar errores comprueba estatica de tipos
DATABASE_URL = config('DATABASE_URL') #conexion usando decouple
engine = create_engine(DATABASE_URL)
Base = declarative_base() #esencial para definir modelos orm


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, index=True)
    student_names = Column(String, nullable=False)
    student_username = Column(String, unique=True, nullable=False)
    
    # RELACIONES
    qualifications = relationship("Qualification", back_populates="student")
    subjects = relationship("Subject", secondary='students_subjects', back_populates="students")
class Subject(Base):
    __tablename__ = 'subjects'

    subject_id = Column(String(6), primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    subject_description = Column(String(255), nullable=False)
    period_id = Column(String(2), nullable=False)
    year = Column(Integer, nullable=False)
    teaching = Column(String(50), nullable=False)
    teachers_email = Column(String(50), nullable=False)

    # RELACIONES
    practical_works = relationship("PracticalWork", back_populates="subject")
    students = relationship("Student", secondary='students_subjects', back_populates="subjects")

    students_subjects = Table(     #TABLA INTERMEDIA RESUELVE ERROR 500 INTERNAL SERVER ERROR
    'students_subjects',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id'), primary_key=True),
    Column('subject_id', String(6), ForeignKey('subjects.subject_id'), primary_key=True)
)

class PracticalWork(Base):
    __tablename__ = 'practical_works'

    pw_id = Column(String(3), primary_key=True, index=True)
    
    guideline_1_id = Column(String(2), nullable=False)
    achievement_1_g1_id = Column(String(4), nullable=False)
    achievement_1_g1_description = Column(String(255), nullable=False)
    achievement_1_g1_score = Column(Integer, nullable=False)
    achievement_2_g1_id = Column(String(4), nullable=False)
    achievement_2_g1_description = Column(String(255), nullable=False)
    achievement_2_g1_score = Column(Integer, nullable=False)
    achievement_3_g1_id = Column(String(4), nullable=False)
    achievement_3_g1_description = Column(String(255), nullable=False)
    achievement_3_g1_score = Column(Integer, nullable=False)
    
    guideline_2_id = Column(String(2), nullable=False)
    achievement_1_g2_id = Column(String(4), nullable=False)
    achievement_1_g2_description = Column(String(255), nullable=False)
    achievement_1_g2_score = Column(Integer, nullable=False)
    achievement_2_g2_id = Column(String(4), nullable=False)
    achievement_2_g2_description = Column(String(255), nullable=False)
    achievement_2_g2_score = Column(Integer, nullable=False)
    achievement_3_g2_id = Column(String(4), nullable=False)
    achievement_3_g2_description = Column(String(255), nullable=False)
    achievement_3_g2_score = Column(Integer, nullable=False)
    
    guideline_3_id = Column(String(2), nullable=False)
    achievement_1_g3_id = Column(String(4), nullable=False)
    achievement_1_g3_description = Column(String(255), nullable=False)
    achievement_1_g3_score = Column(Integer, nullable=False)
    achievement_2_g3_id = Column(String(4), nullable=False)
    achievement_2_g3_description = Column(String(255), nullable=False)
    achievement_2_g3_score = Column(Integer, nullable=False)
    achievement_3_g3_id = Column(String(4), nullable=False)
    achievement_3_g3_description = Column(String(255), nullable=False)
    achievement_3_g3_score = Column(Integer, nullable=False)

    # FKS
    subject_id = Column(String(6), ForeignKey('subjects.subject_id'))

    # RELACIONES
    subject = relationship("Subject", back_populates="practical_works")
    qualifications = relationship("Qualification", back_populates="practical_work")

class Qualification(Base):
    __tablename__ = 'qualifications'

    qualification_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    pw_id = Column(String(3), ForeignKey('practical_works.pw_id'))
    achievements_description = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False)
    
    student = relationship("Student", back_populates="qualifications")
    practical_work = relationship("PracticalWork", back_populates="qualifications")

Base.metadata.create_all(engine) #siempre al finalizar de definir los modelos, esenciales
print ("base de datos creada")