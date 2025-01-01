from fastapi import FastAPI
from solution.routers.qs_routers import router as qs_routers
from config.config import app
from fastapi.middleware.cors import CORSMiddleware

PREFIX_APP = "/app-sq-gen"
app = FastAPI()

@app.get("/") # root route definition
def read_root():
    return {"message": "Welcome to the API"}

# Middleware
#app.middleware("http")(middleware_general)

# CORS para autorizar solicitudes de otros origenes o servicios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # allow todos los metodos HTTP
    allow_headers=["*"],  # allow todos los headers HTTP
)

# Routers (no se si puede ir otro dentro de app)
app.include_router(qs_routers, prefix=PREFIX_APP)
