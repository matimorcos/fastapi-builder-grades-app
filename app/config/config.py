#CONFIG DE LA CONEXION y APP
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# URL DE LA CONEXION
DATABASE_URL = config('DATABASE_URL') #conexion usando decouple

# CFG DE LA DB
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CREAR la aplicación FASTAPI
app = FastAPI()

# DEPENDENCIA PARA OBTENER LA SESION DESDE OTRO DIRECTORIO
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

