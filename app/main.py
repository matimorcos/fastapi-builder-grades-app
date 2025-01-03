from fastapi import FastAPI
from solution.routers.grades import router as grades_routers
from config.config import app
from fastapi.middleware.cors import CORSMiddleware

PREFIX_APP = "/app-sq-gen"
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(grades_routers, prefix=PREFIX_APP)
