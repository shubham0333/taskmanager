from fastapi import FastAPI
from src.routers import task
from src.routers import user
from src.database import engine, Base
from src.model import Task, User
from src.security.config import settings
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [origin.strip() for origin in settings.frontend_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}

app.include_router(task.router)
app.include_router(user.router)
